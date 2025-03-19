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
import requests
import json
from bs4 import BeautifulSoup
import random

# Import courses from the separate file
from portuguese_courses import PORTUGUESE_COURSES

# Import courses from the separate file
from portuguese_courses import PORTUGUESE_LEVELS


# Load environment variables
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
USER_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Initialize the bot
bot = telebot.TeleBot(API_TOKEN)

# Dictionary to store user responses
user_answers = {}
current_exercise = {}

user_exercise_history = defaultdict(list)


# Afficher les niveaux disponibles
@bot.message_handler(commands=['courses'])
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
    
    bot.send_message(chat_id, "📚 Available Portuguese Courses:", reply_markup=markup)

# Handle course content display
def send_course_content(chat_id, course_id):
    if course_id in PORTUGUESE_COURSES:
        course = PORTUGUESE_COURSES[course_id]
        
        # Send course content - this might be long, so you might need to split it
        bot.send_message(chat_id, course['content'], parse_mode="Markdown")
        
        # Add button to practice exercises
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            "Practice Exercises", callback_data=f"exercises_{course_id}"
        ))
        markup.add(telebot.types.InlineKeyboardButton(
            "Back to Courses", callback_data="list_courses"
        ))
        
        bot.send_message(
            chat_id, 
            f"Ready to practice what you've learned in {course['title']}?",
            reply_markup=markup
        )
    else:
        bot.send_message(chat_id, "Course not found.")

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
            
            question = f"🇵🇹 Exercise ({PORTUGUESE_COURSES[course_id]['title']}):\n\n{exercise['question']}"
            
            # Check if this is a typing exercise
            if exercise.get('type') == 'typing':
                bot.send_message(chat_id, question)
                # Register next message as answer
                bot.register_next_step_handler(bot.send_message(chat_id, "Type your answer:"), 
                                             process_typed_answer, course_id)
            else:
                # Multiple choice as before
                markup = telebot.types.InlineKeyboardMarkup()
                for option in exercise['options']:
                    markup.add(telebot.types.InlineKeyboardButton(
                        option, callback_data=option
                    ))
                
                bot.send_message(chat_id, question, reply_markup=markup)
        else:
            bot.send_message(chat_id, "No exercises available for this course.")
    else:
        bot.send_message(chat_id, "Course not found.")

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
            result = f"❌ Incorrect. The correct answer is: {correct_answer}"
            explanation = current_exercise[chat_id].get('explanation', '')
            if explanation:
                result += f"\n\n{explanation}"
        
        # Add "Next Exercise" button
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(
            "Next Exercise", callback_data=f"exercises_{course_id}"
        ))
        markup.add(telebot.types.InlineKeyboardButton(
            "Back to Course", callback_data=f"course_{course_id}"
        ))
        
        bot.send_message(chat_id, result, reply_markup=markup)
        
        # Update user stats
        if chat_id not in user_answers:
            user_answers[chat_id] = {'correct': 0, 'total': 0}
        
        user_answers[chat_id]['total'] += 1
        if user_answer.lower() == correct_answer.lower():
            user_answers[chat_id]['correct'] += 1
    else:
        bot.send_message(chat_id, "Sorry, I can't find your exercise. Try again with /courses.")


# Update callback handler to handle course and exercise callbacks
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    callback_data = call.data
        # Gestion de la sélection de niveau
    if callback_data.startswith("level_") and not callback_data.startswith("level_page_"):
        level_id = callback_data.replace("level_", "")
        send_level_courses(chat_id, level_id)
    
    # Gestion de la pagination des cours d'un niveau
    elif callback_data.startswith("level_page_"):
        parts = callback_data.split('_')
        level_id = parts[2]
        page = int(parts[3])
        send_level_courses(chat_id, level_id, page)
    
    # Retour à la liste des niveaux
    elif callback_data == "list_levels":
        bot.delete_message(chat_id, call.message.message_id)
        levels_command(call.message)


    # Check for course selection
    if callback_data.startswith("course_"):
        course_id = callback_data.replace("course_", "")
        send_course_content(chat_id, course_id)
    
    # Check for exercise request
    elif callback_data.startswith("exercises_"):
        course_id = callback_data.replace("exercises_", "")
        send_course_exercise(chat_id, course_id)
    
    # Handle "Back to courses" action
    elif callback_data == "list_courses":
        bot.delete_message(chat_id, call.message.message_id)
        courses_command(call.message)
    
    # Handle answer checking (from existing code)
    elif chat_id in current_exercise:
        selected_option = callback_data
        correct_answer = current_exercise[chat_id]['correct']
        
        if selected_option == correct_answer:
            result = "✅ Correct! Muito bem!"
            explanation = current_exercise[chat_id].get('explanation', '')
            if explanation:
                result += f"\n\n{explanation}"
        else:
            result = f"❌ Incorrect. The correct answer is: {correct_answer}"
            explanation = current_exercise[chat_id].get('explanation', '')
            if explanation:
                result += f"\n\n{explanation}"
        
        # Get course_id from current exercise if it exists
        course_id = None
        for cid, course in PORTUGUESE_COURSES.items():
            if current_exercise[chat_id] in course['exercises']:
                course_id = cid
                break
        
        # Add "Next Exercise" button if course_id is found
        markup = telebot.types.InlineKeyboardMarkup()
        if course_id:
            markup.add(telebot.types.InlineKeyboardButton(
                "Next Exercise", callback_data=f"exercises_{course_id}"
            ))
            markup.add(telebot.types.InlineKeyboardButton(
                "Back to Course", callback_data=f"course_{course_id}"
            ))
        
        bot.send_message(chat_id, result, reply_markup=markup)
        
        # Update user stats
        if chat_id not in user_answers:
            user_answers[chat_id] = {'correct': 0, 'total': 0}
        
        user_answers[chat_id]['total'] += 1
        if selected_option == correct_answer:
            user_answers[chat_id]['correct'] += 1

# Update help command to include course information
@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
    Portuguese Learning Bot Commands:
    /start - Start receiving exercises
    /now - Get a random exercise immediately
    /courses - Browse available Portuguese courses
    /reading - Reading exercice
    /stats - View your exercise statistics
    /generate [number] - Generate new exercises (default: 5)
    /help - Show this help message
    """
    bot.send_message(message.chat.id, help_text)

# Add this handler for a new command
@bot.message_handler(commands=['typing'])
def typing_command(message):
    chat_id = message.chat.id
    
    # Get all typing exercises from all courses
    typing_exercises = []
    for course_id, course in PORTUGUESE_COURSES.items():
        for exercise in course['exercises']:
            if exercise.get('type') == 'typing':
                typing_exercises.append((course_id, exercise))
    
    if typing_exercises:
        course_id, exercise = random.choice(typing_exercises)
        current_exercise[chat_id] = exercise
        
        question = f"🇵🇹 Typing Exercise ({PORTUGUESE_COURSES[course_id]['title']}):\n\n{exercise['question']}"
        
        # Register next message as answer
        bot.register_next_step_handler(bot.send_message(chat_id, question), 
                                     process_typed_answer, course_id)
    else:
        bot.send_message(chat_id, "No typing exercises available yet.")


# Function to fetch translations using LibreTranslate API
def translate_text(text, source_lang="en", target_lang="pt"):
    """Use LibreTranslate API to translate text"""
    # List of alternative LibreTranslate instances
    servers = [
        "https://translate.argosopentech.com/translate",
        "https://libretranslate.de/translate", 
        "https://translate.terraprint.co/translate"
    ]
    
    for url in servers:
        try:
            payload = {
                "q": text,
                "source": source_lang,
                "target": target_lang,
                "format": "text"
            }
            
            print(f"Attempting to translate using {url}")
            response = requests.post(url, data=payload, timeout=3)
            
            if response.status_code == 200:
                result = response.json()["translatedText"]
                print(f"Translation successful: '{text}' -> '{result}'")
                return result
        except Exception as e:
            print(f"Translation error with {url}: {e}")
    
    # If all servers fail, use built-in fallback dictionary
    fallback_dict = {
        "happy": "feliz", "sad": "triste", "tired": "cansado", "hungry": "com fome",
        "school": "escola", "work": "trabalho", "beach": "praia", "store": "loja",
        "many": "muitos", "few": "poucos", "some": "alguns", "no": "nenhum",
        "study": "estudar", "travel": "viajar", "sleep": "dormir",
        "working": "trabalhando", "studying": "estudando", "living": "morando",
        "teaching": "ensinando", "house": "casa", "food": "comida", "water": "água",
        "friend": "amigo", "time": "tempo", "day": "dia"
    }
    
    # Try direct word translation first
    if text.lower() in fallback_dict:
        return fallback_dict[text.lower()]
        
    # For sentences, use a template response
    if " " in text:
        return f"[Translation for: '{text}']"
        
    # return f"[{text} em português]"    """Use LibreTranslate API to translate text"""
    try:
        url = "https://libretranslate.de/translate"
        payload = {
            "q": text,
            "source": source_lang,
            "target": target_lang,
            "format": "text"
        }
        
        print(f"Attempting to translate: '{text}'")
        response = requests.post(url, data=payload, timeout=5)
        
        if response.status_code == 200:
            result = response.json()["translatedText"]
            print(f"Translation successful: '{text}' -> '{result}'")
            return result
        else:
            print(f"Translation API error: {response.status_code}, {response.text}")
            # Use a predefined translation dictionary for common words
            common_translations = {
                "house": "casa", "car": "carro", "book": "livro", 
                # Add more common translations here
            }
            if text.lower() in common_translations:
                return common_translations[text.lower()]
            return f"[{text} em português]"  # Better fallback
            
    except Exception as e:
        print(f"Translation error: {e}")
        return f"[{text} em português]"  # Better fallback


# Function to fetch random words using Random Word API
def get_random_english_words(count=5):
    """Get random English words to use for vocabulary exercises"""
    try:
        url = f"https://random-word-api.herokuapp.com/word?number={count}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Random word API error: {response.status_code}")
            return ["house", "food", "water", "friend", "day"]  # Fallback words
    except Exception as e:
        print(f"Random word error: {e}")
        return ["house", "food", "water", "friend", "day"]  # Fallback words

# Function to fetch word definitions using Free Dictionary API
def get_word_definition(word, language="en"):
    """Get word definition to use in explanations"""
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/{language}/{word}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0 and "meanings" in data[0]:
                for meaning in data[0]["meanings"]:
                    if "definitions" in meaning and len(meaning["definitions"]) > 0:
                        return meaning["definitions"][0]["definition"]
        return None
    except Exception as e:
        print(f"Definition API error: {e}")
        return None


# Function to send a random exercise
def send_exercise(chat_id=None):
    if chat_id is None:
        chat_id = USER_CHAT_ID
    
    question = f"🇵🇹 Portuguese Exercise:\n\n{exercise['question']}"
    
    markup = telebot.types.InlineKeyboardMarkup()
    for option in exercise['options']:
        markup.add(telebot.types.InlineKeyboardButton(
            option, callback_data=option
        ))
    
    bot.send_message(chat_id, question, reply_markup=markup)
    print(f"Exercise sent to {chat_id} at {datetime.now().strftime('%H:%M:%S')}")

# Handle the /start command
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Welcome to your Portuguese learning bot! You'll receive exercises every 2 hours.")
    
    # Send first exercise immediately
    send_exercise(chat_id)
    
    # If this is not the predefined USER_CHAT_ID, add it to scheduled exercises
    if str(chat_id) != str(USER_CHAT_ID):
        schedule_exercises(chat_id)

# Handle callback from inline buttons
@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    chat_id = call.message.chat.id
    selected_option = call.data
    
    # Check if there's a current exercise for this chat
    if chat_id not in current_exercise:
        bot.send_message(chat_id, "Sorry, I can't find your exercise. Please use /start to get a new one.")
        return
    
    correct_answer = current_exercise[chat_id]['correct']
    
    if selected_option == correct_answer:
        result = "✅ Correct! Muito bem!"
        explanation = current_exercise[chat_id].get('explanation', '')
        if explanation:
            result += f"\n\n{explanation}"
    else:
        result = f"❌ Incorrect. The correct answer is: {correct_answer}"
        explanation = current_exercise[chat_id].get('explanation', '')
        if explanation:
            result += f"\n\n{explanation}"
    
        
    bot.send_message(chat_id, result)
    
    # Update user stats
    if chat_id not in user_answers:
        user_answers[chat_id] = {'correct': 0, 'total': 0}
    
    user_answers[chat_id]['total'] += 1
    if selected_option == correct_answer:
        user_answers[chat_id]['correct'] += 1

# Handle the /stats command
@bot.message_handler(commands=['stats'])
def stats_command(message):
    chat_id = message.chat.id
    if chat_id in user_answers:
        stats = user_answers[chat_id]
        accuracy = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
        bot.send_message(
            chat_id, 
            f"Your stats:\nCorrect answers: {stats['correct']}\nTotal exercises: {stats['total']}\nAccuracy: {accuracy:.1f}%"
        )
    else:
        bot.send_message(chat_id, "You haven't answered any exercises yet.")


# Schedule exercises every 2 hours for a specific chat
def schedule_exercises(chat_id=None):
    if chat_id is None:
        chat_id = USER_CHAT_ID
    
    # To avoid duplicates, remove any existing jobs for this chat_id
    for job in schedule.get_jobs():
        if hasattr(job, 'chat_id') and job.chat_id == chat_id:
            schedule.cancel_job(job)
    
    # Schedule new job
    job = schedule.every(2).hours.do(send_exercise, chat_id=chat_id)
    job.chat_id = chat_id  # Attach chat_id to the job for identification
    
    print(f"Scheduled exercises every 2 hours for chat ID: {chat_id}")

def signal_handler(sig, frame):
    print('Ctrl+C pressed, exiting gracefully')
    sys.exit(0)

# Run the scheduler in a separate thread
def schedule_checker():
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(f"Scheduler error: {e}")
            time.sleep(5)  # Wait a bit before trying again

if __name__ == "__main__":
    # Test API connectivity before starting
    print("Testing API connectivity...")
    try:
        test_result = translate_text("hello", "en", "pt")
        if test_result and test_result != "[hello em português]":
            print(f"✓ Translation API working: 'hello' -> '{test_result}'")
        else:
            print("✗ Translation API not working properly")
    except Exception as e:
        print(f"✗ Translation API error: {e}")
    # Schedule exercises for the predefined user
    schedule_exercises()
    
    # Send first exercise immediately to the predefined user
    #send_exercise()
    
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=schedule_checker, daemon=True)
    scheduler_thread.start()
    
    print(f"Bot started! Initial exercise sent to {USER_CHAT_ID}")
    print("Listening for responses...")
        

    try:
        print(f"Bot started! Initial exercise sent to {USER_CHAT_ID}")
        print("Listening for responses...")
        # bot.polling(none_stop=True, timeout=60)
        bot.infinity_polling(timeout=10, long_polling_timeout = 5)

    except Exception as e:
        print(f"Bot polling error: {e}")
    finally:
        print("Bot stopped")
