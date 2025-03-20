# Changes to imports:
import os
import telebot
import schedule
import time
import threading
import random
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
import signal
import sys
from collections import OrderedDict
from collections import defaultdict
from bs4 import BeautifulSoup

# Import courses from the separate file
from portuguese_courses import PORTUGUESE_COURSES, PORTUGUESE_LEVELS, EXERCISE_THEMES

# State tracking variables remain the same
user_theme_progress = {}
current_exercise = {}
user_answers = {}
user_exercise_history = defaultdict(list)


# Load environment variables
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
USER_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Initialize the bot
bot = telebot.TeleBot(API_TOKEN)

# Fonction pour commencer un thème
def start_themed_exercises(chat_id, theme_id):
    if theme_id in EXERCISE_THEMES:
        theme = EXERCISE_THEMES[theme_id]
        
        # Initialiser ou réinitialiser la progression
        user_theme_progress[chat_id] = {
            'theme_id': theme_id,
            'current_question': 0,
            'correct_answers': 0,
            'total_questions': len(theme['exercises'])
        }
        
        # Envoyer une introduction
        intro_message = f"📝 *{theme['title']}*\n\n{theme['description']}\n\nVous allez répondre à {len(theme['exercises'])} questions sur ce thème."
        bot.send_message(chat_id, intro_message, parse_mode="Markdown")
        
        # Envoyer la première question
        send_themed_question(chat_id)
    else:
        bot.send_message(chat_id, "Thème non trouvé.")

# Fonction pour envoyer une question du thème
def send_themed_question(chat_id):
    if chat_id not in user_theme_progress:
        bot.send_message(chat_id, "Aucun thème en cours. Utilisez /themes pour commencer.")
        return
    
    progress = user_theme_progress[chat_id]
    theme_id = progress['theme_id']
    question_index = progress['current_question']
    
    # Vérifier si on a terminé toutes les questions
    if question_index >= progress['total_questions']:
        complete_theme(chat_id)
        return
    
    # Obtenir l'exercice actuel
    exercise = EXERCISE_THEMES[theme_id]['exercises'][question_index]
    
    # Stocker l'exercice courant
    current_exercise[chat_id] = exercise
    
    # Construire le message de question
    question_number = question_index + 1
    total_questions = progress['total_questions']
    question_message = f"Question {question_number}/{total_questions}:\n\n{exercise['question']}"
    
    # Créer les boutons pour les options
    markup = telebot.types.InlineKeyboardMarkup()
    for option in exercise['options']:
        markup.add(telebot.types.InlineKeyboardButton(
            option, callback_data=f"theme_answer_{option}"
        ))
    
    bot.send_message(chat_id, question_message, reply_markup=markup)

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

# Fonction pour terminer un thème
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
    result_message = f"🎉 Vous avez terminé le thème *{theme['title']}*!\n\n"
    result_message += f"Score: {correct}/{total} ({percentage:.1f}%)\n\n"
    
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
        "Recommencer ce thème", callback_data=f"theme_{theme_id}"
    ))
    markup.add(telebot.types.InlineKeyboardButton(
        "Choisir un autre thème", callback_data="list_themes"
    ))
    
    bot.send_message(chat_id, result_message, reply_markup=markup, parse_mode="Markdown")
    
    # Nettoyer la progression
    del user_theme_progress[chat_id]

# Handler pour commencer un thème d'exercices
@bot.message_handler(commands=['themes'])
def themes_command(message):
    chat_id = message.chat.id
    
    markup = telebot.types.InlineKeyboardMarkup()
    for theme_id, theme in EXERCISE_THEMES.items():
        markup.add(telebot.types.InlineKeyboardButton(
            theme['title'], callback_data=f"theme_{theme_id}"
        ))
    
    bot.send_message(chat_id, "📚 Choisissez un thème d'exercices:", reply_markup=markup)

# Afficher les niveaux disponibles
@bot.message_handler(commands=['levels'])
def levels_command(message):
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

def process_typed_answer(message, course_id):
    chat_id = message.chat.id
    if chat_id in current_exercise:
        user_answer = message.text.strip()
        correct_answer = current_exercise[chat_id]['correct']
        
        # Case-insensitive comparison for typed answers
        if user_answer.lower() == correct_answer.lower():
            result = "✅ Correct! Muito bem!"
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
        if user_answer.lower() == correct_answer.lower():
            user_answers[chat_id]['correct'] += 1
    else:
        bot.send_message(chat_id, "Désolé, je ne retrouve pas votre exercice. Essayez à nouveau avec /courses.")

# Update callback handler to handle all types of callbacks
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    callback_data = call.data
    
    # Handle theme selection and answers
    if callback_data.startswith("theme_"):
        if callback_data == "list_themes":
            # Retour à la liste des thèmes
            bot.delete_message(chat_id, call.message.message_id)
            themes_command(call.message)  # This line calls the themes_command function
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
    
    # Handle exercise requests
    elif callback_data.startswith("exercises_"):
        course_id = callback_data.replace("exercises_", "")
        send_course_exercise(chat_id, course_id)

# Handle the /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Bienvenue sur votre bot d'apprentissage du portugais!")
    # Send help menu immediately after start
    help_command(message)

# Help command
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
    🤖 Commandes du Bot d'Apprentissage du Portugais:
    
    /start - Démarrer le bot
    /help - Afficher ce message d'aide
    /courses - Parcourir les cours disponibles
    /levels - Voir les niveaux d'apprentissage
    /themes - Exercices par thèmes
    /stats - Voir vos statistiques d'exercices
    """
    bot.send_message(message.chat.id, help_text)

# Handle typing exercises
@bot.message_handler(commands=['typing'])
def typing_command(message):
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

# Send help menu when bot starts
def send_initial_help():
    if USER_CHAT_ID:
        try:
            bot.send_message(int(USER_CHAT_ID), "🤖 Bot d'apprentissage du portugais démarré!")
            help_command_msg = telebot.types.Message(
                message_id=1, 
                from_user=telebot.types.User(id=int(USER_CHAT_ID), is_bot=False, first_name='User'),
                date=int(time.time()),
                chat=telebot.types.Chat(id=int(USER_CHAT_ID), type='private'),
                content_type='text',
                options={},
                json_string=''
            )
            help_command(help_command_msg)
        except Exception as e:
            print(f"Erreur lors de l'envoi du message initial: {e}")

if __name__ == "__main__":
    # Signal handler for graceful shutdown
    signal.signal(signal.SIGINT, lambda sig, frame: sys.exit(0))
    
    print("Bot démarré!")
    
    # Send initial help menu
    if USER_CHAT_ID:
        threading.Thread(target=send_initial_help).start()
    
    try:
        # Start the bot
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Erreur de polling du bot: {e}")
    finally:
        print("Bot arrêté")