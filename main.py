# Changes to imports:
import os
import telebot
import time
import threading
import random
import json
from datetime import datetime
from dotenv import load_dotenv
import signal
import sys
from collections import OrderedDict
from collections import defaultdict
# Ajouter ces imports
from gtts import gTTS
from io import BytesIO
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
# Ajouter ces lignes au début de votre code
import time
from collections import defaultdict

# Import courses from the separate file
from portuguese_courses import PORTUGUESE_COURSES, PORTUGUESE_LEVELS, EXERCISE_THEMES, THEME_CATEGORIES, TEXT_TO_SPEECH_EXERCISES


# Protection contre les abus
message_counters = defaultdict(lambda: {"count": 0, "reset_time": time.time()})
MAX_MESSAGES_PER_MINUTE = 10  # Ajustez selon vos besoins
COOLDOWN_SECONDS = 60

# State tracking variables remain the same
user_theme_progress = {}
current_exercise = {}
user_answers = {}
user_exercise_history = defaultdict(list)


# Load environment variables
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
# USER_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Initialize the bot
bot = telebot.TeleBot(API_TOKEN)



def is_rate_limited(message):
    print("is called")
    user_id = message.from_user.id
    current_time = time.time()
    
    # Réinitialiser le compteur après une minute
    if current_time - message_counters[user_id]["reset_time"] > COOLDOWN_SECONDS:
        message_counters[user_id] = {"count": 0, "reset_time": current_time}
    
    # Incrémenter le compteur
    message_counters[user_id]["count"] += 1
    
    # Vérifier si la limite est dépassée
    if message_counters[user_id]["count"] > MAX_MESSAGES_PER_MINUTE:
        bot.send_message(message.chat.id, "Por favor, aguarde um pouco antes de enviar mais mensagens.")
        return True
    return False

@bot.message_handler(commands=['clear'])
def clear_command(message):

    if is_rate_limited(message):
        return

    """Send multiple messages to clear the chat visually"""
    # Send 5 messages with many newlines each
    for i in range(5):
        clear_text = '\n' * 100
        bot.send_message(message.chat.id, clear_text)
    
    # Final message indicating clearing is complete
    bot.send_message(message.chat.id, "Chat cleared!")

# Fonction pour envoyer un exercice audio généré
def send_tts_exercise(chat_id, tts_id):
    print(f"Trying to access audio exercise with ID: {tts_id}")
    print(f"Available IDs: {list(TEXT_TO_SPEECH_EXERCISES.keys())}")
    
    if tts_id in TEXT_TO_SPEECH_EXERCISES:
        exercise = TEXT_TO_SPEECH_EXERCISES[tts_id]
        current_exercise[chat_id] = exercise
        
        # Générer et envoyer l'audio
        success = generate_and_send_audio(
            chat_id, 
            exercise['text'], 
            caption=f"🎧 {exercise['title']}"
        )
        
        if success:
            # Envoyer la question après l'audio
            time.sleep(1)
            markup = telebot.types.InlineKeyboardMarkup()
            for option in exercise['options']:
                markup.add(telebot.types.InlineKeyboardButton(
                    option, callback_data=f"tts_answer_{option}"
                ))
            
            bot.send_message(chat_id, exercise['question'], reply_markup=markup)
    else:
        bot.send_message(chat_id, f"Exercício de áudio não encontrado. ID: {tts_id}")


# Fonction pour traiter les réponses aux exercices audio générés
def process_tts_answer(chat_id, answer):
    if chat_id in current_exercise:
        exercise = current_exercise[chat_id]
        correct_answer = exercise['correct']
        
        if answer == correct_answer:
            result = "✅ Correct! Muito bem!"
            explanation = exercise.get('explanation', '')
            if explanation:
                result += f"\n\n{explanation}"
        else:
            result = f"❌ Incorrect. La bonne réponse est: {correct_answer}"
            explanation = exercise.get('explanation', '')
            if explanation:
                result += f"\n\n{explanation}"
        
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            "Outro exercício de áudio", callback_data="tts_list"
        ))
        
        bot.send_message(chat_id, result, reply_markup=markup)
        
        # Update user stats
        if chat_id not in user_answers:
            user_answers[chat_id] = {'correct': 0, 'total': 0}
        
        user_answers[chat_id]['total'] += 1
        if answer == correct_answer:
            user_answers[chat_id]['correct'] += 1
    else:
        bot.send_message(chat_id, "Nenhum exercício ativo. Use /audio para começar.")

# Fonction pour générer et envoyer un audio à partir de texte
def generate_and_send_audio(chat_id, text, caption=""):
    try:
        # Créer l'objet gTTS
        tts = gTTS(text=text, lang='pt-br', slow=False)
        
        # Utiliser BytesIO pour ne pas avoir à sauvegarder de fichier
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)  # Retour au début du buffer
        
        # Envoyer l'audio
        bot.send_voice(chat_id, audio_bytes, caption=caption)
        
        return True
    except Exception as e:
        bot.send_message(chat_id, f"Erro ao gerar o áudio: {e}")
        return False
    

# Modification de la fonction start_themed_exercises pour initialiser une liste aléatoire d'indices
def start_themed_exercises(chat_id, theme_id):
    if theme_id in EXERCISE_THEMES:
        theme = EXERCISE_THEMES[theme_id]
        
        # Créer une liste d'indices de questions dans un ordre aléatoire
        total_questions = len(theme['exercises'])
        random_question_indices = list(range(total_questions))
        random.shuffle(random_question_indices)
        
        # Initialiser ou réinitialiser la progression
        user_theme_progress[chat_id] = {
            'theme_id': theme_id,
            'current_question': 0,
            'correct_answers': 0,
            'total_questions': total_questions,
            'question_order': random_question_indices  # Stocker l'ordre aléatoire
        }
        
        # Envoyer une introduction
        intro_message = f"📝 *{theme['title']}*\n\n{theme['description']}\n\nVocê vai responder a {total_questions} perguntas sobre este tema."
        bot.send_message(chat_id, intro_message, parse_mode="Markdown")
        
        # Envoyer la première question
        send_themed_question(chat_id)
    else:
        bot.send_message(chat_id, "Tema não encontrado.")

# Ajouter un nouveau type d'exercice dans la fonction send_themed_question
def send_themed_question(chat_id):
    if chat_id not in user_theme_progress:
        bot.send_message(chat_id, "Aucun thème en cours. Utilisez /themes pour commencer.")
        return
    
    progress = user_theme_progress[chat_id]
    theme_id = progress['theme_id']
    question_index_position = progress['current_question']
    
    # Vérifier si on a terminé toutes les questions
    if question_index_position >= progress['total_questions']:
        complete_theme(chat_id)
        return
    
    # Obtenir l'index réel de la question à partir de l'ordre aléatoire
    if 'question_order' in progress:
        actual_question_index = progress['question_order'][question_index_position]
    else:
        actual_question_index = question_index_position
    
    # Obtenir l'exercice actuel
    exercise = EXERCISE_THEMES[theme_id]['exercises'][actual_question_index]
    
    # Stocker l'exercice courant
    current_exercise[chat_id] = exercise
    
    # Construire le message de question
    question_number = question_index_position + 1
    total_questions = progress['total_questions']
    question_message = f"Question {question_number}/{total_questions}:\n\n{exercise['question']}"
    
    # Vérifier le type d'exercice
    exercise_type = exercise.get('type', 'multiple_choice')  # par défaut: choix multiple
    
    if exercise_type == 'fill_in_blank':
        # Exercice à trous où l'utilisateur doit taper la réponse
        bot.send_message(chat_id, question_message)
        # Enregistrer la prochaine réponse de l'utilisateur
        bot.register_next_step_handler(
            bot.send_message(chat_id, "Escreva sua resposta:"), 
            process_fill_in_blank_answer
        )
    else:
        # Exercice à choix multiples (comportement actuel)
        markup = telebot.types.InlineKeyboardMarkup()
        
        # Mélanger les options si désiré
        options = exercise['options'].copy()
        random.shuffle(options)
        
        for option in options:
            markup.add(telebot.types.InlineKeyboardButton(
                option, callback_data=f"theme_answer_{option}"
            ))
        
        bot.send_message(chat_id, question_message, reply_markup=markup)

# Fonction modifiée pour traiter les réponses aux exercices à trous
def process_fill_in_blank_answer(message):
    chat_id = message.chat.id
    
    if chat_id not in user_theme_progress or chat_id not in current_exercise:
        bot.send_message(chat_id, "Aucun exercice en cours. Utilisez /themes pour commencer.")
        return
    
    progress = user_theme_progress[chat_id]
    exercise = current_exercise[chat_id]
    
    # Récupérer la réponse de l'utilisateur et la réponse correcte
    user_answer = message.text.strip()
    correct_answer = exercise['correct']
    
    # Comparer les réponses avec tolérance pour petites erreurs
    is_correct, error_type = is_similar_text(user_answer, correct_answer, 0.8)
    
    # Mettre à jour le score
    if is_correct:
        progress['correct_answers'] += 1
        
        # Feedback selon le type d'erreur
        if error_type == "exact":
            feedback = "✅ Correct! " + exercise.get('explanation', '')
        elif error_type == "case":
            feedback = "✅ Correct, mais attention aux majuscules! La réponse exacte est: " + correct_answer + "\n" + exercise.get('explanation', '')
        elif error_type == "accent":
            feedback = "✅ Correct, mais attention aux accents! La réponse exacte est: " + correct_answer + "\n" + exercise.get('explanation', '')
        else:  # "typo"
            feedback = "✅ Presque correct (petite erreur)! La réponse exacte est: " + correct_answer + "\n" + exercise.get('explanation', '')
    else:
        feedback = f"❌ Incorrect. A resposta correta é: {correct_answer}\n" + exercise.get('explanation', '')
    
    # Envoyer le feedback
    bot.send_message(chat_id, feedback)
    
    # Passer à la question suivante
    progress['current_question'] += 1
    
    # Attendre un peu avant d'envoyer la prochaine question
    time.sleep(1.5)
    send_themed_question(chat_id)


# Fonction pour traiter les réponses aux questions thématiques
def process_themed_answer(chat_id, answer):
    if chat_id not in user_theme_progress or chat_id not in current_exercise:
        return
    
    progress = user_theme_progress[chat_id]
    exercise = current_exercise[chat_id]
    correct = exercise['correct']
    
    # Vérifier si la réponse est correcte
    is_correct = (answer == correct)
    
    # Mettre à jour le score
    if is_correct:
        progress['correct_answers'] += 1
        feedback = "✅ Correct! " + exercise.get('explanation', '')
    else:
        feedback = f"❌ Incorrect. La bonne réponse est: {correct}\n" + exercise.get('explanation', '')
    
    # Envoyer le feedback
    bot.send_message(chat_id, feedback)
    
    # Passer à la question suivante
    progress['current_question'] += 1
    
    # Attendre un peu avant d'envoyer la prochaine question
    time.sleep(1.5)
    send_themed_question(chat_id)

# Fonction pour terminer un thème - Traduction en portugais
def complete_theme(chat_id):
    if chat_id not in user_theme_progress:
        return
    
    progress = user_theme_progress[chat_id]
    theme_id = progress['theme_id']
    theme = EXERCISE_THEMES[theme_id]
    
    correct = progress['correct_answers']
    total = progress['total_questions']
    percentage = (correct / total) * 100
    
    # Message de résultat
    result_message = f"🎉 Você completou o tema *{theme['title']}*!\n\n"
    result_message += f"Pontuação: {correct}/{total} ({percentage:.1f}%)\n\n"
    
    # Ajouter un message d'encouragement
    if percentage >= 90:
        result_message += "Excelente! Você está dominando este tema! 👏"
    elif percentage >= 70:
        result_message += "Muito bom! Você está progredindo bem! 👍"
    elif percentage >= 50:
        result_message += "Bom trabalho! Continue praticando! 💪"
    else:
        result_message += "Continue praticando! Você vai melhorar! 🙂"
    
    # Ajouter des boutons pour continuer
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(
        "Recomeçar este tema", callback_data=f"theme_{theme_id}"
    ))
    markup.add(telebot.types.InlineKeyboardButton(
        "Escolher outro tema", callback_data="list_categories"
    ))
    
    bot.send_message(chat_id, result_message, reply_markup=markup, parse_mode="Markdown")
    
    # Nettoyer la progression
    del user_theme_progress[chat_id]



# Fonction pour initialiser les catégories automatiquement
def initialize_theme_categories():
    # Assigner chaque thème à une catégorie en fonction d'un attribut 'category' 
    # que vous devrez ajouter à vos thèmes dans EXERCISE_THEMES
    for theme_id, theme in EXERCISE_THEMES.items():
        category = theme.get('category', 'other')  # Valeur par défaut 'other'
        if category in THEME_CATEGORIES:
            THEME_CATEGORIES[category]['themes'].append(theme_id)
    
    # Créer une catégorie "Tous les thèmes" qui contient tous les thèmes
    THEME_CATEGORIES['all'] = {
        "title": "Todos os temas",
        "description": "Todos os exercícios disponíveis",
        "themes": list(EXERCISE_THEMES.keys())
    }

# Appeler cette fonction au démarrage
initialize_theme_categories()

# Commande pour afficher les catégories de thèmes
@bot.message_handler(commands=['themes'])
def themes_categories(message):

    if is_rate_limited(message):
        return

    chat_id = message.chat.id
    
    markup = telebot.types.InlineKeyboardMarkup()
    for category_id, category in THEME_CATEGORIES.items():
        # Ajouter le nombre de thèmes pour plus de clarté
        theme_count = len(category['themes'])
        markup.add(telebot.types.InlineKeyboardButton(
            f"{category['title']} ({theme_count})", callback_data=f"category_{category_id}"
        ))
    
    bot.send_message(chat_id, "📚 Escolha uma categoria de exercícios:", reply_markup=markup)
# Fonction utilitaire pour normaliser le texte (enlever accents, ponctuation, etc.)
def normalize_text(text):
    import unicodedata
    import re
    # Convertir en minuscules
    text = text.lower()
    # Enlever les accents
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    # Enlever la ponctuation et les espaces supplémentaires
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Fonction pour vérifier si deux textes sont similaires
def is_similar_text(user_answer, correct_answer, similarity_threshold=0.8):
    # Si les textes sont identiques (sensible à la casse)
    if user_answer == correct_answer:
        return True, "exact"
    
    # Si les textes sont identiques (insensible à la casse)
    if user_answer.lower() == correct_answer.lower():
        return True, "case"
    
    # Vérifier si la différence est juste des accents
    if normalize_text(user_answer) == normalize_text(correct_answer):
        return True, "accent"
    
    # Calculer la distance de Levenshtein si les modules nécessaires sont disponibles
    try:
        from Levenshtein import ratio
        similarity = ratio(user_answer.lower(), correct_answer.lower())
        if similarity >= similarity_threshold:
            return True, "typo"
    except ImportError:
        # Méthode alternative simple si Levenshtein n'est pas disponible
        normalized_user = normalize_text(user_answer)
        normalized_correct = normalize_text(correct_answer)
        
        # Si les longueurs sont trop différentes, ce n'est pas similaire
        if abs(len(normalized_user) - len(normalized_correct)) > 3:
            return False, None
        
        # Compter les caractères communs
        common_chars = set(normalized_user) & set(normalized_correct)
        if len(common_chars) / max(len(set(normalized_user)), len(set(normalized_correct))) >= similarity_threshold:
            return True, "typo"
    
    return False, None

# Fonction pour afficher les thèmes d'une catégorie avec pagination
def send_category_themes(chat_id, category_id, page=0):
    if category_id in THEME_CATEGORIES:
        category = THEME_CATEGORIES[category_id]
        theme_ids = category['themes']
        
        # Pagination - 5 thèmes par page
        themes_per_page = 5
        total_pages = (len(theme_ids) + themes_per_page - 1) // themes_per_page
        
        # Vérifier les limites de la page
        if page < 0:
            page = 0
        if page >= total_pages:
            page = total_pages - 1
            
        start_idx = page * themes_per_page
        end_idx = min(start_idx + themes_per_page, len(theme_ids))
        
        markup = telebot.types.InlineKeyboardMarkup()
        for theme_id in theme_ids[start_idx:end_idx]:
            if theme_id in EXERCISE_THEMES:
                theme = EXERCISE_THEMES[theme_id]
                # Ajouter info sur nombre d'exercices
                ex_count = len(theme['exercises'])
                markup.add(telebot.types.InlineKeyboardButton(
                    f"{theme['title']} ({ex_count} ex.)", callback_data=f"theme_{theme_id}"
                ))
        
        # Navigation pour pagination
        nav_row = []
        if page > 0:
            nav_row.append(telebot.types.InlineKeyboardButton(
                "⬅️ Anterior", callback_data=f"category_page_{category_id}_{page-1}"
            ))
        if page < total_pages - 1:
            nav_row.append(telebot.types.InlineKeyboardButton(
                "Próximo ➡️", callback_data=f"category_page_{category_id}_{page+1}"
            ))
        if nav_row:
            markup.row(*nav_row)
        
        # Bouton retour aux catégories
        markup.add(telebot.types.InlineKeyboardButton(
            "🔙 Voltar às categorias", callback_data="list_categories"
        ))
        
        # Message avec titre de catégorie, description et indication de page
        message_text = f"📚 {category['title']} - {category['description']}\n"
        message_text += f"Página {page+1}/{total_pages} • {len(theme_ids)} temas disponíveis"
        
        bot.send_message(chat_id, message_text, reply_markup=markup)
    else:
        bot.send_message(chat_id, "Categoria não encontrada.")

# Afficher les niveaux disponibles
@bot.message_handler(commands=['levels'])
def levels_command(message):

    if is_rate_limited(message):
        return

    chat_id = message.chat.id
    
    markup = telebot.types.InlineKeyboardMarkup()
    for level_id, level in PORTUGUESE_LEVELS.items():
        markup.add(telebot.types.InlineKeyboardButton(
            f"{level_id} - {level['title']}", callback_data=f"level_{level_id}"
        ))
    
    bot.send_message(chat_id, "📚 Niveaux de portugais disponibles:", reply_markup=markup)

# Afficher les cours d'un niveau spécifique (avec pagination)
def send_level_courses(chat_id, level_id, page=0):
    if level_id in PORTUGUESE_LEVELS:
        level = PORTUGUESE_LEVELS[level_id]
        courses = list(level['courses'].items())
        
        # Pagination - 5 cours par page
        courses_per_page = 5
        total_pages = (len(courses) + courses_per_page - 1) // courses_per_page
        
        # Vérifier les limites de la page
        if page < 0:
            page = 0
        if page >= total_pages:
            page = total_pages - 1
            
        start_idx = page * courses_per_page
        end_idx = min(start_idx + courses_per_page, len(courses))
        
        markup = telebot.types.InlineKeyboardMarkup()
        for course_id, course in courses[start_idx:end_idx]:
            markup.add(telebot.types.InlineKeyboardButton(
                course['title'], callback_data=f"course_{course_id}"
            ))
        
        # Ajouter navigation pour pagination
        nav_row = []
        if page > 0:
            nav_row.append(telebot.types.InlineKeyboardButton(
                "⬅️ Précédent", callback_data=f"level_page_{level_id}_{page-1}"
            ))
        if page < total_pages - 1:
            nav_row.append(telebot.types.InlineKeyboardButton(
                "Suivant ➡️", callback_data=f"level_page_{level_id}_{page+1}"
            ))
        if nav_row:
            markup.row(*nav_row)
            
        # Bouton retour aux niveaux
        markup.add(telebot.types.InlineKeyboardButton(
            "🔙 Retour aux niveaux", callback_data="list_levels"
        ))
        
        bot.send_message(
            chat_id, 
            f"📚 Cours disponibles ({level_id} - {level['title']}):\nPage {page+1}/{total_pages}",
            reply_markup=markup
        )
    else:
        bot.send_message(chat_id, "Niveau non trouvé.")

# Handle the /courses command to list available courses
@bot.message_handler(commands=['courses'])
def courses_command(message):

    if is_rate_limited(message):
        return

    chat_id = message.chat.id
    
    markup = telebot.types.InlineKeyboardMarkup()
    for course_id, course in PORTUGUESE_COURSES.items():
        markup.add(telebot.types.InlineKeyboardButton(
            course['title'], callback_data=f"course_{course_id}"
        ))
    
    bot.send_message(chat_id, "📚 Cours de portugais disponibles:", reply_markup=markup)

# Handle course content display
def send_course_content(chat_id, course_id):
    if course_id in PORTUGUESE_COURSES:
        course = PORTUGUESE_COURSES[course_id]
        
        # Send course content
        bot.send_message(chat_id, course['content'], parse_mode="Markdown")
        
        # Add button to practice exercises
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            "Faire des exercices", callback_data=f"exercises_{course_id}"
        ))
        markup.add(telebot.types.InlineKeyboardButton(
            "Retour aux cours", callback_data="list_courses"
        ))
        
        bot.send_message(
            chat_id, 
            f"Prêt à pratiquer ce que vous avez appris dans {course['title']}?",
            reply_markup=markup
        )
    else:
        bot.send_message(chat_id, "Cours non trouvé.")

# Send exercise for a specific course
def send_course_exercise(chat_id, course_id):
    if course_id in PORTUGUESE_COURSES:
        exercises = PORTUGUESE_COURSES[course_id]['exercises']
        if exercises:
            # Filter out recently shown exercises for this user
            available_exercises = [ex for ex in exercises if ex not in user_exercise_history.get(chat_id, [])[-5:]]
            
            # If we've gone through most exercises, reset history
            if not available_exercises:
                user_exercise_history[chat_id] = []
                available_exercises = exercises
            
            exercise = random.choice(available_exercises)
            current_exercise[chat_id] = exercise
            
            # Add to user history
            user_exercise_history[chat_id].append(exercise)
            
            question = f"🇵🇹 Exercice ({PORTUGUESE_COURSES[course_id]['title']}):\n\n{exercise['question']}"
            
            # Check if this is a typing exercise
            if exercise.get('type') == 'typing':
                bot.send_message(chat_id, question)
                # Register next message as answer
                bot.register_next_step_handler(bot.send_message(chat_id, "Tapez votre réponse:"), 
                                             process_typed_answer, course_id)
            else:
                # Multiple choice as before
                markup = telebot.types.InlineKeyboardMarkup()
                for option in exercise['options']:
                    markup.add(telebot.types.InlineKeyboardButton(
                        option, callback_data=f"course_answer_{option}"
                    ))
                
                bot.send_message(chat_id, question, reply_markup=markup)
        else:
            bot.send_message(chat_id, "Aucun exercice disponible pour ce cours.")
    else:
        bot.send_message(chat_id, "Cours non trouvé.")

# Mise à jour de process_typed_answer pour utiliser la nouvelle fonction
def process_typed_answer(message, course_id):
    chat_id = message.chat.id
    if chat_id in current_exercise:
        user_answer = message.text.strip()
        correct_answer = current_exercise[chat_id]['correct']
        
        # Vérifier la réponse avec tolérance pour petites erreurs
        is_correct, error_type = is_similar_text(user_answer, correct_answer, 0.8)
        
        if is_correct:
            if error_type == "exact":
                result = "✅ Correct! Muito bem!"
            elif error_type == "case":
                result = "✅ Correct, mais attention aux majuscules! La réponse exacte est: " + correct_answer
            elif error_type == "accent":
                result = "✅ Correct, mais attention aux accents! La réponse exacte est: " + correct_answer
            else:  # "typo"
                result = "✅ Presque correct (petite erreur)! La réponse exacte est: " + correct_answer
            
            explanation = current_exercise[chat_id].get('explanation', '')
            if explanation:
                result += f"\n\n{explanation}"
        else:
            result = f"❌ Incorrect. La bonne réponse est: {correct_answer}"
            explanation = current_exercise[chat_id].get('explanation', '')
            if explanation:
                result += f"\n\n{explanation}"
        
        # Add "Next Exercise" button
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            "Exercice suivant", callback_data=f"exercises_{course_id}"
        ))
        markup.add(telebot.types.InlineKeyboardButton(
            "Retour au cours", callback_data=f"course_{course_id}"
        ))
        
        bot.send_message(chat_id, result, reply_markup=markup)
        
        # Update user stats
        if chat_id not in user_answers:
            user_answers[chat_id] = {'correct': 0, 'total': 0}
        
        user_answers[chat_id]['total'] += 1
        if is_correct:
            user_answers[chat_id]['correct'] += 1
    else:
        bot.send_message(chat_id, "Désolé, je ne retrouve pas votre exercice. Essayez à nouveau avec /courses.")


# Commande pour accéder aux exercices audio générés
@bot.message_handler(commands=['audio'])
def tts_exercises_command(message):

    if is_rate_limited(message):
        return

    chat_id = message.chat.id
    
    markup = telebot.types.InlineKeyboardMarkup()
    for tts_id, exercise in TEXT_TO_SPEECH_EXERCISES.items():
        markup.add(telebot.types.InlineKeyboardButton(
            exercise['title'], callback_data=f"tts_{tts_id}"
        ))
    
    bot.send_message(chat_id, "🎧 Escolha um exercício de compreensão oral:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id  # Get the message ID
    callback_data = call.data
    print(f"Received callback: {callback_data}")

    # First, try to delete or edit the original message with buttons
    try:
        # Option 1: Delete the message with the button
        # bot.delete_message(chat_id, message_id)
        
        # Option 2: Or edit it to remove buttons (often better UX)
        bot.edit_message_reply_markup(chat_id, message_id, reply_markup=None)
    except Exception as e:
        print(f"Couldn't update old message: {e}")

    # Now handle the callback and send a new message with buttons if needed
    # For example, if handling theme selection:
    if callback_data.startswith("theme_"):
        if callback_data == "list_themes":
            themes_categories(call.message)
        elif callback_data.startswith("theme_answer_"):
            answer = callback_data.replace("theme_answer_", "")
            process_themed_answer(chat_id, answer)
        else:
            theme_id = callback_data.replace("theme_", "")
            start_themed_exercises(chat_id, theme_id)

    # Handle "list_categories" directly
    if callback_data == "list_categories":
        bot.delete_message(chat_id, call.message.message_id)
        themes_categories(call.message)
    
    # Handle category selection and pagination
    elif callback_data.startswith("category_"):
        if callback_data.startswith("category_page_"):
            parts = callback_data.split('_')
            category_id = parts[2]
            page = int(parts[3])
            send_category_themes(chat_id, category_id, page)
        else:
            category_id = callback_data.replace("category_", "")
            send_category_themes(chat_id, category_id)
    
    # Handle theme selection and answers
    elif callback_data.startswith("theme_"):
        if callback_data == "list_themes":
            # Retour à la liste des thèmes
            bot.delete_message(chat_id, call.message.message_id)
            themes_categories(call.message)  # Changed to themes_categories
        elif callback_data.startswith("theme_answer_"):
            # Réponse à une question thématique
            answer = callback_data.replace("theme_answer_", "")
            process_themed_answer(chat_id, answer)
        else:
            # Sélection d'un thème
            theme_id = callback_data.replace("theme_", "")
            start_themed_exercises(chat_id, theme_id)
    
    # Handle level selection and pagination
    elif callback_data.startswith("level_"):
        if callback_data == "list_levels":
            bot.delete_message(chat_id, call.message.message_id)
            levels_command(call.message)
        elif callback_data.startswith("level_page_"):
            parts = callback_data.split('_')
            level_id = parts[2]
            page = int(parts[3])
            send_level_courses(chat_id, level_id, page)
        else:
            level_id = callback_data.replace("level_", "")
            send_level_courses(chat_id, level_id)
    
    # Handle course selection and exercises
    elif callback_data.startswith("course_"):
        if callback_data == "list_courses":
            bot.delete_message(chat_id, call.message.message_id)
            courses_command(call.message)
        elif callback_data.startswith("course_answer_"):
            # Answer to a course exercise
            answer = callback_data.replace("course_answer_", "")
            if chat_id in current_exercise:
                correct_answer = current_exercise[chat_id]['correct']
                
                if answer == correct_answer:
                    result = "✅ Correct! Muito bem!"
                    explanation = current_exercise[chat_id].get('explanation', '')
                    if explanation:
                        result += f"\n\n{explanation}"
                else:
                    result = f"❌ Incorrect. La bonne réponse est: {correct_answer}"
                    explanation = current_exercise[chat_id].get('explanation', '')
                    if explanation:
                        result += f"\n\n{explanation}"
                
                # Find course_id
                course_id = None
                for cid, course in PORTUGUESE_COURSES.items():
                    if 'exercises' in course and current_exercise[chat_id] in course['exercises']:
                        course_id = cid
                        break
                
                markup = telebot.types.InlineKeyboardMarkup()
                if course_id:
                    markup.add(telebot.types.InlineKeyboardButton(
                        "Exercice suivant", callback_data=f"exercises_{course_id}"
                    ))
                    markup.add(telebot.types.InlineKeyboardButton(
                        "Retour au cours", callback_data=f"course_{course_id}"
                    ))
                
                bot.send_message(chat_id, result, reply_markup=markup)
                
                # Update user stats
                if chat_id not in user_answers:
                    user_answers[chat_id] = {'correct': 0, 'total': 0}
                
                user_answers[chat_id]['total'] += 1
                if answer == correct_answer:
                    user_answers[chat_id]['correct'] += 1
        else:
            course_id = callback_data.replace("course_", "")
            send_course_content(chat_id, course_id)
            # Dans votre fonction handle_callback, ajoutez ces conditions:

    elif callback_data.startswith("tts_"):
        if callback_data == "tts_list":
            bot.delete_message(chat_id, call.message.message_id)
            tts_exercises_command(call.message)
        elif callback_data.startswith("tts_answer_"):
            answer = callback_data.replace("tts_answer_", "")
            process_tts_answer(chat_id, answer)
        else:
            tts_id = callback_data.replace("tts_", "")
            send_tts_exercise(chat_id, tts_id)
    
    # Handle exercise requests
    elif callback_data.startswith("exercises_"):
        course_id = callback_data.replace("exercises_", "")
        send_course_exercise(chat_id, course_id)

# Modifier les messages d'accueil en portugais brésilien
@bot.message_handler(commands=['start'])
def start_command(message):

    if is_rate_limited(message):
        return

    chat_id = message.chat.id
    bot.send_message(chat_id, "Bem-vindo ao seu bot de aprendizado de português brasileiro!")
    # Send help menu immediately after start
    help_command(message)

# Modification pour la commande help en portugais brésilien
@bot.message_handler(commands=['help'])
def help_command(message):

    if is_rate_limited(message):
        return

    help_text = """
    🤖 Comandos do Bot de Aprendizado de Português:
    
    /start - Iniciar o bot
    /help - Mostrar esta mensagem de ajuda
    /courses - Explorar cursos disponíveis
    /levels - Ver níveis de aprendizado
    /themes - Exercícios por temas
    /stats - Ver suas estatísticas de exercícios
    /typing - Praticar exercícios de digitação
    """
    bot.send_message(message.chat.id, help_text)

# Handle typing exercises
@bot.message_handler(commands=['typing'])
def typing_command(message):

    if is_rate_limited(message):
        return

    chat_id = message.chat.id
    
    # Get all typing exercises from all courses
    typing_exercises = []
    for course_id, course in PORTUGUESE_COURSES.items():
        for exercise in course.get('exercises', []):
            if exercise.get('type') == 'typing':
                typing_exercises.append((course_id, exercise))
    
    if typing_exercises:
        course_id, exercise = random.choice(typing_exercises)
        current_exercise[chat_id] = exercise
        
        question = f"🇵🇹 Exercice de frappe ({PORTUGUESE_COURSES[course_id]['title']}):\n\n{exercise['question']}"
        
        # Register next message as answer
        bot.register_next_step_handler(bot.send_message(chat_id, question), 
                                     process_typed_answer, course_id)
    else:
        bot.send_message(chat_id, "Aucun exercice de frappe disponible pour le moment.")

# Handle the /stats command
@bot.message_handler(commands=['stats'])
def stats_command(message):

    if is_rate_limited(message):
        return

    chat_id = message.chat.id
    if chat_id in user_answers:
        stats = user_answers[chat_id]
        accuracy = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        bot.send_message(
            chat_id, 
            f"Vos statistiques:\nRéponses correctes: {stats['correct']}\nTotal des exercices: {stats['total']}\nPrécision: {accuracy:.1f}%"
        )
    else:
        bot.send_message(chat_id, "Vous n'avez pas encore répondu à des exercices.")

def send_initial_help():
    # Cette fonction n'est plus nécessaire pour un bot public
    # Si vous souhaitez envoyer un message à un admin spécifique, vous pouvez utiliser:
    admin_id = os.getenv('TELEGRAM_ADMIN_ID')  # Optionnel, pour vos propres besoins
    if admin_id:
        try:
            bot.send_message(int(admin_id), "🤖 Bot de aprendizado de português iniciado!")
        except Exception as e:
            print(f"Erro ao enviar mensagem ao admin: {e}")

if __name__ == "__main__":
    # Signal handler for graceful shutdown
    # signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))

    print("Bot démarré!")
    
    # Supprimer le webhook avant de démarrer le polling
    bot.remove_webhook()
    
    # Send initial help menu
    # if USER_CHAT_ID:
    #     threading.Thread(target=send_initial_help).start()
    
    try:
        # Start the bot - il répondra à tous les utilisateurs
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Erreur de polling du bot: {e}")
    finally:
        print("Bot arrêté")