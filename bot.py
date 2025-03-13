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


# Dictionary to store reading passages
PORTUGUESE_READINGS = [
    {
        "title": "Um Dia na Praia",
        "text": """Ontem, fui à praia com minha família. O dia estava ensolarado e quente. Chegamos cedo e encontramos um bom lugar para colocar nossas toalhas. As crianças foram nadar no mar, enquanto os adultos conversavam sob o guarda-sol. Almoçamos sanduíches e frutas que trouxemos de casa. À tarde, fizemos um castelo de areia enorme. Foi um dia muito relaxante e divertido. Voltamos para casa no final da tarde, cansados mas felizes.""",
        "questions": [
            {
                "question": "Onde a família passou o dia?",
                "options": ["Na montanha", "No parque", "Na praia", "No museu"],
                "correct": "Na praia",
                "explanation": "'Ontem, fui à praia com minha família' indica claramente onde passaram o dia."
            },
            {
                "question": "Como estava o clima naquele dia?",
                "options": ["Chuvoso", "Ensolarado e quente", "Nublado", "Ventoso"],
                "correct": "Ensolarado e quente",
                "explanation": "'O dia estava ensolarado e quente' descreve o clima do dia."
            },
            {
                "question": "O que a família comeu no almoço?",
                "options": ["Peixe grelhado", "Sanduíches e frutas", "Pizza", "Não almoçaram"],
                "correct": "Sanduíches e frutas",
                "explanation": "'Almoçamos sanduíches e frutas que trouxemos de casa' menciona o que comeram."
            }
        ]
    },
    {
        "title": "Meu Cachorro Carlos",
        "text": """Tenho um cachorro chamado Carlos. Ele é um labrador preto com cinco anos de idade. Carlos é muito brincalhão e energético. Todas as manhãs, levanto cedo para levá-lo para passear no parque. Ele adora correr atrás da bola e brincar com outros cachorros. Carlos também é muito inteligente. Ele sabe sentar, dar a pata e até fingir de morto quando comando. À noite, Carlos dorme em sua cama ao lado da minha. Ele é meu melhor amigo.""",
        "questions": [
            {
                "question": "Qual é a raça do cachorro?",
                "options": ["Bulldog", "Labrador", "Poodle", "Pastor Alemão"],
                "correct": "Labrador",
                "explanation": "'Ele é um labrador preto' menciona a raça do cachorro."
            },
            {
                "question": "Quantos anos tem Carlos?",
                "options": ["Três", "Quatro", "Cinco", "Seis"],
                "correct": "Cinco",
                "explanation": "'Ele é um labrador preto com cinco anos de idade' indica a idade do cachorro."
            },
            {
                "question": "O que Carlos gosta de fazer no parque?",
                "options": ["Dormir", "Correr atrás da bola", "Comer", "Nadar"],
                "correct": "Correr atrás da bola",
                "explanation": "'Ele adora correr atrás da bola e brincar com outros cachorros' descreve o que ele gosta de fazer."
            }
        ]
    },
    {
        "title": "Uma Visita a São Paulo",
        "text": """No mês passado, visitei São Paulo pela primeira vez. É a maior cidade do Brasil, com muitos prédios altos e ruas movimentadas. Fiquei hospedado em um hotel no centro da cidade. Durante o dia, visitei o Museu de Arte de São Paulo (MASP) e o Parque Ibirapuera. A comida era deliciosa, especialmente a pizza que comi na Bela Vista, um bairro conhecido por restaurantes italianos. Também fui ao Mercado Municipal para experimentar o famoso sanduíche de mortadela. Apesar do trânsito intenso, consegui conhecer muitos lugares interessantes em apenas três dias.""",
        "questions": [
            {
                "question": "Qual cidade foi visitada?",
                "options": ["Rio de Janeiro", "Brasília", "Salvador", "São Paulo"],
                "correct": "São Paulo",
                "explanation": "'No mês passado, visitei São Paulo pela primeira vez' menciona claramente a cidade."
            },
            {
                "question": "Quantos dias durou a visita?",
                "options": ["Dois", "Três", "Quatro", "Uma semana"],
                "correct": "Três",
                "explanation": "'Consegui conhecer muitos lugares interessantes em apenas três dias' indica a duração da visita."
            },
            {
                "question": "O que a pessoa experimentou no Mercado Municipal?",
                "options": ["Pizza", "Churrasco", "Sanduíche de mortadela", "Feijoada"],
                "correct": "Sanduíche de mortadela",
                "explanation": "'Também fui ao Mercado Municipal para experimentar o famoso sanduíche de mortadela' menciona o que foi consumido."
            }
        ]
    }
]



# Add a new command handler for reading exercises
@bot.message_handler(commands=['reading'])
def reading_command(message):
    chat_id = message.chat.id
    
    # Send a message that we're preparing a reading exercise
    bot.send_message(chat_id, "📖 Preparando um exercício de leitura em português... Um momento, por favor.")
    
    try:
        # Fetch and prepare reading material
        reading = fetch_and_prepare_reading()
        
        # Store current reading exercise questions for this user
        if 'reading_questions' not in current_exercise:
            current_exercise['reading_questions'] = {}
        current_exercise['reading_questions'][chat_id] = reading['questions']
        current_exercise['reading_current_question'] = {chat_id: 0}
        
        # Send the reading passage
        reading_message = f"📚 *{reading['title']}*\n\n{reading['text']}"
        
        # If it has source information, add it
        if 'source' in reading and 'link' in reading and reading['link']:
            reading_message += f"\n\nFonte: {reading['source']}"
        
        bot.send_message(chat_id, reading_message, parse_mode="Markdown")
        
        # Send the first question after a short delay
        bot.send_message(chat_id, "Leia o texto acima com atenção. Vou enviar perguntas sobre ele em seguida.")
        
        # Send first question
        send_reading_question(chat_id)
        
    except Exception as e:
        print(f"Error in reading exercise: {e}")
        bot.send_message(
            chat_id, 
            "Desculpe, tive um problema ao preparar o exercício de leitura. Por favor, tente novamente.")
    chat_id = message.chat.id
    
    # Send a message that we're preparing a reading exercise
    bot.send_message(chat_id, "📖 Preparando um exercício de leitura em português... Um momento, por favor.")
    
    try:
        # Fetch and prepare reading material
        reading = fetch_and_prepare_reading()
        
        # Store current reading exercise questions for this user
        if 'reading_questions' not in current_exercise:
            current_exercise['reading_questions'] = {}
        current_exercise['reading_questions'][chat_id] = reading['questions']
        current_exercise['reading_current_question'] = {chat_id: 0}
        
        # Send the reading passage
        reading_message = f"📚 *{reading['title']}*\n\n{reading['text']}"
        
        # If it has source information, add it
        if 'source' in reading and 'link' in reading and reading['link']:
            reading_message += f"\n\nFonte: {reading['source']}"
        
        bot.send_message(chat_id, reading_message, parse_mode="Markdown")
        
        # Send the first question after a short delay
        bot.send_message(chat_id, "Leia o texto acima com atenção. Vou enviar perguntas sobre ele em seguida.")
        
        # Send first question
        send_reading_question(chat_id)
        
    except Exception as e:
        print(f"Error in reading exercise: {e}")
        bot.send_message(
            chat_id, 
            "Desculpe, tive um problema")

def send_reading_question(chat_id):
    """Send a reading comprehension question to the user"""
    if chat_id not in current_exercise.get('reading_current_question', {}):
        bot.send_message(chat_id, "Sorry, I can't find your reading exercise. Please use /reading to get a new one.")
        return
    
    # Get the current question index
    current_idx = current_exercise['reading_current_question'][chat_id]
    
    # Check if we've reached the end of questions
    if current_idx >= len(current_exercise['reading_questions'][chat_id]):
        bot.send_message(chat_id, "✅ You've completed all the questions for this reading exercise!")
        return
    
    # Get the current question
    question_data = current_exercise['reading_questions'][chat_id][current_idx]
    
    # Format the question
    question_text = f"📝 Question {current_idx + 1}: {question_data['question']}"
    
    # Create markup with options
    markup = telebot.types.InlineKeyboardMarkup()
    for option in question_data['options']:
        # Use a special callback format to distinguish from other exercise types
        callback_data = f"reading_{option}"
        markup.add(telebot.types.InlineKeyboardButton(option, callback_data=callback_data))
    
    # Send the question
    bot.send_message(chat_id, question_text, reply_markup=markup)


# Add handler for reading question answers
@bot.callback_query_handler(func=lambda call: call.data.startswith('reading_'))
def handle_reading_answer(call):
    chat_id = call.message.chat.id
    selected_option = call.data.replace('reading_', '')
    
    # Check if there's a current reading exercise for this chat
    if chat_id not in current_exercise.get('reading_current_question', {}):
        bot.send_message(chat_id, "Sorry, I can't find your reading exercise. Please use /reading to get a new one.")
        return
    
    # Get the current question index
    current_idx = current_exercise['reading_current_question'][chat_id]
    
    # Get the current question
    question_data = current_exercise['reading_questions'][chat_id][current_idx]
    correct_answer = question_data['correct']
    
    # Check if the answer is correct
    if selected_option == correct_answer:
        result = "✅ Correct! Muito bem!"
        explanation = question_data.get('explanation', '')
        if explanation:
            result += f"\n\n{explanation}"
    else:
        result = f"❌ Incorrect. The correct answer is: {correct_answer}"
        explanation = question_data.get('explanation', '')
        if explanation:
            result += f"\n\n{explanation}"
    
    # Send result
    bot.send_message(chat_id, result)
    
    # Update user stats
    if chat_id not in user_answers:
        user_answers[chat_id] = {'correct': 0, 'total': 0}
    
    user_answers[chat_id]['total'] += 1
    if selected_option == correct_answer:
        user_answers[chat_id]['correct'] += 1
    
    # Move to the next question
    current_exercise['reading_current_question'][chat_id] += 1
    
    # Check if there are more questions
    if current_exercise['reading_current_question'][chat_id] < len(current_exercise['reading_questions'][chat_id]):
        # Send the next question after a short delay
        time.sleep(1)
        send_reading_question(chat_id)
    else:
        # All questions answered
        bot.send_message(chat_id, "🎉 Congratulations! You've completed all the questions for this reading exercise!")

def fetch_and_prepare_reading():
    """Fetch and prepare reading material for the exercise"""
    # Select a random reading from the list
    reading = random.choice(PORTUGUESE_READINGS)
    return reading

PORTUGUESE_COURSES = OrderedDict([
    ("basics", {
        "title": "Portuguese Basics",
"content": """# Portuguese Basics

## Greetings
- Olá = Hello
- Bom dia = Good morning
- Boa tarde = Good afternoon
- Boa noite = Good evening/night
- Tchau = Goodbye
- Até logo = See you later

## Simple Phrases
- Como você está? = How are you?
- Eu estou bem = I am well
- Obrigado (male) / Obrigada (female) = Thank you
- De nada = You're welcome
- Por favor = Please
- Com licença = Excuse me
        
## Numbers 1-10
1. Um/Uma
2. Dois/Duas
3. Três
4. Quatro
5. Cinco
6. Seis
7. Sete
8. Oito
9. Nove
10. Dez""",        
 "exercises": [
  {
    "question": "Which of the following expressions is a formal greeting in Portuguese?",
    "options": ["Oi", "Alô", "Olá", "Tchau"],
    "correct": "Olá",
    "explanation": "'Olá' is commonly used as a formal greeting, equivalent to 'Hello'."
  },
  {
    "question": "Which Portuguese phrase is used to greet someone in the morning?",
    "options": ["Bom dia", "Boa noite", "Boa tarde", "Até logo"],
    "correct": "Bom dia",
    "explanation": "'Bom dia' is the Portuguese phrase used to wish someone a good morning."
  },
  {
    "question": "Which expression would you use to wish someone a good evening or night in Portuguese?",
    "options": ["Boa noite", "Bom dia", "Boa tarde", "Oi"],
    "correct": "Boa noite",
    "explanation": "'Boa noite' is the phrase used for both 'Good evening' and 'Good night'."
  },
  {
    "question": "What is the masculine form of 'Thank you' in Portuguese?",
    "options": ["Obrigado", "Obrigada", "Desculpe", "Com licença"],
    "correct": "Obrigado",
    "explanation": "Males use 'Obrigado' to express gratitude in Portuguese."
  },
  {
    "question": "What form should a woman use to say 'Thank you' in Portuguese?",
    "options": ["Obrigada", "Obrigado", "Por favor", "Com licença"],
    "correct": "Obrigada",
    "explanation": "Women use 'Obrigada' instead of 'Obrigado' to say 'Thank you'."
  },
  {
    "question": "Which of the following means 'Excuse me' in the context of asking for permission in Portuguese?",
    "options": ["Com licença", "Desculpe", "Oi", "Por favor"],
    "correct": "Com licença",
    "explanation": "'Com licença' is used when asking for permission or excusing oneself."
  },
  {
    "question": "Which phrase is used to politely ask for something in Portuguese?",
    "options": ["Desculpe", "Tchau", "Por favor", "Boa noite"],
    "correct": "Por favor",
    "explanation": "'Por favor' means 'Please' in Portuguese, a polite way to make requests."
  },
  {
    "question": "Which word means 'Good afternoon' in Portuguese?",
    "options": ["Boa noite", "Boa tarde", "Tchau", "Bom dia"],
    "correct": "Boa tarde",
    "explanation": "'Boa tarde' is the correct expression for 'Good afternoon'."
  },
  {
    "question": "Which of the following expressions means 'Goodbye' in Portuguese?",
    "options": ["Tchau", "Adeus", "Oi", "Até logo"],
    "correct": "Tchau",
    "explanation": "'Tchau' is an informal way to say 'Goodbye' in Portuguese."
  },
  {
    "question": "Which phrase means 'See you soon' in Portuguese?",
    "options": ["Até logo", "Tchau", "Até mais", "Bom dia"],
    "correct": "Até mais",
    "explanation": "'Até mais' translates to 'See you soon' or 'See you later'."
  },
  {
    "question": "What is the Portuguese word for 'Yes'?",
    "options": ["Não", "Sim", "Talvez", "Claro"],
    "correct": "Sim",
    "explanation": "'Sim' means 'Yes' in Portuguese."
  },
  {
    "question": "Which word means 'No' in Portuguese?",
    "options": ["Não", "Sim", "Talvez", "Desculpe"],
    "correct": "Não",
    "explanation": "'Não' means 'No' in Portuguese."
  },
  {
    "question": "How do you ask someone 'How are you?' in Portuguese?",
    "options": ["Como vai?", "Onde você está?", "Como você está?", "O que você faz?"],
    "correct": "Como você está?",
    "explanation": "'Como você está?' means 'How are you?' in Portuguese."
  },
  {
    "question": "Which phrase means 'My name is João' in Portuguese?",
    "options": ["Meu nome é João", "Eu sou João", "Como está João?", "Quem é João?"],
    "correct": "Meu nome é João",
    "explanation": "'Meu nome é João' means 'My name is João'."
  },
  {
    "question": "What is the Portuguese word for 'One'?",
    "options": ["Um", "Primeiro", "Único", "Um e meio"],
    "correct": "Um",
    "explanation": "'Um' is the word for 'One' in Portuguese."
  },
  {
    "question": "How do you say 'Two' in Portuguese?",
    "options": ["Cinco", "Dois", "Dois e meio", "Dúzia"],
    "correct": "Dois",
    "explanation": "'Dois' means 'Two' in Portuguese."
  },
  {
    "question": "What is the Portuguese word for 'Three'?",
    "options": ["Três", "Triângulo", "Trilogia", "Treze"],
    "correct": "Três",
    "explanation": "'Três' means 'Three' in Portuguese."
  },
  {
    "question": "How do you say 'Four' in Portuguese?",
    "options": ["Cinco", "Quatro", "Quadrado", "Quarenta"],
    "correct": "Quatro",
    "explanation": "'Quatro' is the Portuguese word for 'Four'."
  },
  {
    "question": "What is the Portuguese word for 'Five'?",
    "options": ["Cinco", "Cinquenta", "Seis", "Seis e meio"],
    "correct": "Cinco",
    "explanation": "'Cinco' means 'Five' in Portuguese."
  },
  {
    "question": "Which number means 'Six' in Portuguese?",
    "options": ["Seis", "Sexta", "Cinco", "Sessenta"],
    "correct": "Seis",
    "explanation": "'Seis' is the Portuguese word for 'Six'."
  },
  {
    "question": "What is the Portuguese word for 'Seven'?",
    "options": ["Sete", "Setenta", "Sétimo", "Sete e meia"],
    "correct": "Sete",
    "explanation": "'Sete' means 'Seven' in Portuguese."
  },
  {
    "question": "How do you say 'Eight' in Portuguese?",
    "options": ["Oito", "Octavo", "Oitava", "Octante"],
    "correct": "Oito",
    "explanation": "'Oito' means 'Eight' in Portuguese."
  },
  {
    "question": "What is the Portuguese word for 'Nine'?",
    "options": ["Nove", "Novenário", "Nonagésimo", "Nona"],
    "correct": "Nove",
    "explanation": "'Nove' means 'Nine' in Portuguese."
  },
  {
    "question": "How do you say 'Ten' in Portuguese?",
    "options": ["Dez", "Década", "Dezena", "Decílio"],
    "correct": "Dez",
    "explanation": "'Dez' means 'Ten' in Portuguese."
  },
  {
    "question": "Which phrase means 'Where are you from?' in Portuguese?",
    "options": ["Onde você mora?", "De onde você é?", "Onde você vai?", "Como está você?"],
    "correct": "De onde você é?",
    "explanation": "'De onde você é?' means 'Where are you from?' in Portuguese."
  },
  {
    "question": "What is the Portuguese phrase for 'I don’t understand'?",
    "options": ["Eu entendi", "Eu sei", "Eu não entendo", "Eu gosto"],
    "correct": "Eu não entendo",
    "explanation": "'Eu não entendo' means 'I don’t understand'."
  },
  {
    "question": "Which word means 'Friend' in Portuguese?",
    "options": ["Amigo", "Amiga", "Amizade", "Amigável"],
    "correct": "Amigo",
    "explanation": "'Amigo' means 'Friend' in Portuguese."
  }
],

    }),
    # Other course sections
     ("ser_estar", {
        "title": "Ser vs. Estar",
        "content": """# Ser vs. Estar

In Portuguese, there are two verbs that translate to "to be" in English:

## Ser
Used for permanent or inherent characteristics:
- Identity: Eu sou brasileiro. (I am Brazilian.)
- Profession: Ela é médica. (She is a doctor.)
- Physical characteristics: Ele é alto. (He is tall.)

Conjugation (Present):
- Eu sou = I am
- Você/Ele/Ela é = You/He/She is
- Nós somos = We are
- Vocês/Eles/Elas são = You all/They are

## Estar
Used for temporary states or conditions:
- Emotions: Eu estou feliz. (I am happy [right now].)
- Location: Ele está em casa. (He is at home [now].)
- Temporary conditions: Ela está doente. (She is sick [currently].)

Conjugation (Present):
- Eu estou = I am
- Você/Ele/Ela está = You/He/She is
- Nós estamos = We are
- Vocês/Eles/Elas estão = You all/They are""",
        "exercises": [
            {
                "question": "Which verb should be used in: 'Eu ____ brasileiro.' (I am Brazilian.)",
                "options": ["sou", "estou", "é", "está"],
                "correct": "sou",
                "explanation": "Use 'ser' (sou) for nationality as it's a permanent characteristic."
            },
            {
                "question": "Which is correct for 'She is at the beach today'?",
                "options": ["Ela é na praia hoje.", "Ela está na praia hoje.", "Ela sou na praia hoje.", "Ela estar na praia hoje."],
                "correct": "Ela está na praia hoje.",
                "explanation": "Use 'estar' (está) for location as it's temporary."
            },
            {
                "question": "Which sentence correctly uses 'ser'?",
                "options": ["Nós estamos professores.", "Nós somos professores.", "Nós está professores.", "Nós é professores."],
                "correct": "Nós somos professores.",
                "explanation": "'Nós somos professores' (We are teachers) uses 'ser' correctly for profession."
            },
            {
                "question": "Choose the correct sentence for 'I am sick today':",
                "options": ["Eu sou doente hoje.", "Eu estou doente hoje.", "Eu é doente hoje.", "Eu estar doente hoje."],
                "correct": "Eu estou doente hoje.",
                "explanation": "Use 'estar' (estou) for temporary conditions like being sick."
            },
            {
                "question": "Which is correct: 'They are tall.'",
                "options": ["Eles estão altos.", "Eles são altos.", "Eles está altos.", "Eles é altos."],
                "correct": "Eles são altos.",
                "explanation": "Use 'ser' (são) for physical characteristics as they're generally permanent."
            }
        ]
    }),
    ("present_tense", {
        "title": "Present Tense Verbs",
        "content": """# Present Tense Verbs

## Regular -AR Verbs
Example: Falar (to speak)
- Eu falo = I speak
- Você/Ele/Ela fala = You/He/She speaks
- Nós falamos = We speak
- Vocês/Eles/Elas falam = You all/They speak

Other common -AR verbs:
- Trabalhar = To work
- Estudar = To study
- Morar = To live
- Gostar = To like

## Regular -ER Verbs
Example: Comer (to eat)
- Eu como = I eat
- Você/Ele/Ela come = You/He/She eats
- Nós comemos = We eat
- Vocês/Eles/Elas comem = You all/They eat

Other common -ER verbs:
- Beber = To drink
- Aprender = To learn
- Vender = To sell
- Ler = To read

## Regular -IR Verbs
Example: Abrir (to open)
- Eu abro = I open
- Você/Ele/Ela abre = You/He/She opens
- Nós abrimos = We open
- Vocês/Eles/Elas abrem = You all/They open

Other common -IR verbs:
- Partir = To leave
- Decidir = To decide
- Assistir = To watch
- Permitir = To permit""",
        "exercises": [
            {
                "question": "How do you conjugate 'falar' (to speak) for 'I speak'?",
                "options": ["Falo", "Fala", "Falamos", "Falam"],
                "correct": "Falo",
                "explanation": "The correct first-person (eu) conjugation for 'falar' is 'falo'."
            },
            {
                "question": "What is 'She works' in Portuguese?",
                "options": ["Ela trabalha", "Ela trabalho", "Ela trabalhamos", "Ela trabalham"],
                "correct": "Ela trabalha",
                "explanation": "The correct third-person (ela) conjugation for 'trabalhar' is 'trabalha'."
            },
            {
                "question": "How do you say 'We eat' in Portuguese?",
                "options": ["Nós come", "Nós como", "Nós comemos", "Nós comem"],
                "correct": "Nós comemos",
                "explanation": "The correct first-person plural (nós) conjugation for 'comer' is 'comemos'."
            },
            {
                "question": "Complete: 'Vocês _____ português.' (You all speak Portuguese.)",
                "options": ["fala", "falo", "falamos", "falam"],
                "correct": "falam",
                "explanation": "The correct third-person plural (vocês) conjugation for 'falar' is 'falam'."
            },
            {
                "question": "Which is correct for 'He opens the door'?",
                "options": ["Ele abre a porta.", "Ele abro a porta.", "Ele abrimos a porta.", "Ele abrem a porta."],
                "correct": "Ele abre a porta.",
                "explanation": "The correct third-person (ele) conjugation for 'abrir' is 'abre'."
            }
        ]
    })
])

# # Define Portuguese course content
# PORTUGUESE_COURSES["ser_estar"]["exercises"].extend([
    
#             {
#                 "question": "Which verb should be used in: 'Eu ____ brasileiro.' (I am Brazilian.)",
#                 "options": ["sou", "estou", "é", "está"],
#                 "correct": "sou",
#                 "explanation": "Use 'ser' (sou) for nationality as it's a permanent characteristic."
#             },
#             {
#                 "question": "Which is correct for 'She is at the beach today'?",
#                 "options": ["Ela é na praia hoje.", "Ela está na praia hoje.", "Ela sou na praia hoje.", "Ela estar na praia hoje."],
#                 "correct": "Ela está na praia hoje.",
#                 "explanation": "Use 'estar' (está) for location as it's temporary."
#             },
#             {
#                 "question": "Which sentence correctly uses 'ser'?",
#                 "options": ["Nós estamos professores.", "Nós somos professores.", "Nós está professores.", "Nós é professores."],
#                 "correct": "Nós somos professores.",
#                 "explanation": "'Nós somos professores' (We are teachers) uses 'ser' correctly for profession."
#             },
#             {
#                 "question": "Choose the correct sentence for 'I am sick today':",
#                 "options": ["Eu sou doente hoje.", "Eu estou doente hoje.", "Eu é doente hoje.", "Eu estar doente hoje."],
#                 "correct": "Eu estou doente hoje.",
#                 "explanation": "Use 'estar' (estou) for temporary conditions like being sick."
#             },
#             {
#                 "question": "Which is correct: 'They are tall.'",
#                 "options": ["Eles estão altos.", "Eles são altos.", "Eles está altos.", "Eles é altos."],
#                 "correct": "Eles são altos.",
#                 "explanation": "Use 'ser' (são) for physical characteristics as they're generally permanent."
#             }
# ])

# # Define Portuguese course content
# PORTUGUESE_COURSES["basics"]["exercises"].extend([
#     {
#         "question": "How do you say 'Hello' in Portuguese?",
#         "options": ["Tchau", "Olá", "Bom dia", "Por favor"],
#         "correct": "Olá",
#         "explanation": "'Olá' means 'Hello' in Portuguese."
#     },
#     {
#         "question": "What is the correct translation for 'Good afternoon'?",
#         "options": ["Bom dia", "Boa tarde", "Boa noite", "Olá tarde"],
#         "correct": "Boa tarde",
#         "explanation": "'Boa tarde' is used for 'Good afternoon' in Portuguese."
#     },
#     {
#         "question": "How do you say 'Thank you' if you are a woman?",
#         "options": ["Obrigado", "Obrigada", "De nada", "Por favor"],
#         "correct": "Obrigada",
#         "explanation": "Women say 'Obrigada' and men say 'Obrigado' for 'Thank you'."
#     },
#     {
#         "question": "What does 'Como você está?' mean?",
#         "options": ["What is your name?", "How are you?", "Where are you from?", "How old are you?"],
#         "correct": "How are you?",
#         "explanation": "'Como você está?' means 'How are you?' in Portuguese."
#     },
#     {
#         "question": "What is the Portuguese word for the number 5?",
#         "options": ["Três", "Quatro", "Cinco", "Seis"],
#         "correct": "Cinco",
#         "explanation": "'Cinco' is the Portuguese word for the number 5."
#     }
# ])

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

# Generate vocabulary exercise using API translations
def generate_vocabulary_exercise():
    """Generate a vocabulary exercise using random words and translations"""
    # Get random English words
    words = get_random_english_words(8)  # Get extra words for options
    
    if not words or len(words) < 4:
        # Fallback if API fails
        words = ["house", "car", "book", "water", "food", "friend", "time", "day"]
    else :
        print(words)
    
    # Select one word for the question
    target_word = random.choice(words[:4])
    
    # Get translation
    translation = translate_text(target_word, "en", "pt")
    if not translation:
        # Fallback translations if API fails
        fallback_translations = {
            "house": "casa", "car": "carro", "book": "livro", "water": "água",
            "food": "comida", "friend": "amigo", "time": "tempo", "day": "dia"
        }
        translation = fallback_translations.get(target_word, "palavra")
    
    # Get definition for explanation
    definition = get_word_definition(target_word)
    if not definition:
        definition = "no definition available"
    
    # Generate wrong answers (other translations)
    wrong_options = []
    for word in [w for w in words if w != target_word][:3]:
        wrong_translation = translate_text(word, "en", "pt")
        if wrong_translation and wrong_translation != translation:
            wrong_options.append(wrong_translation)
    
    # Ensure we have 3 wrong options
    while len(wrong_options) < 3:
        dummy_translations = ["palavra", "coisa", "objeto", "lugar", "pessoa", "tempo"]
        dummy = random.choice(dummy_translations)
        if dummy not in wrong_options and dummy != translation:
            wrong_options.append(dummy)
    
    # Create options list including correct answer
    options = wrong_options + [translation]
    random.shuffle(options)
    
    # Create exercise
    exercise = {
        "question": f"What is the Portuguese word for '{target_word}'?",
        "options": options,
        "correct": translation,
        "explanation": f"'{target_word}' means '{translation}' in Portuguese. Definition: {definition}"
    }
    
    return exercise

# Generate grammar exercise using sentence translation
def generate_grammar_exercise():
    """Generate a grammar exercise using translated sentences"""
    # Template sentences with grammar focus
    templates = [
        "I am {0} today.",  # ser vs estar
        "She went to {0} yesterday.",  # preposition usage
        "They have {0} books.",  # numbers/quantifiers
        "We will {0} tomorrow.",  # future tense
        "He has been {0} for two years."  # present perfect
    ]
    
    # Words to fill in templates
    fill_words = [
        ["happy", "sad", "tired", "hungry"],
        ["school", "work", "the beach", "the store"],
        ["many", "few", "some", "no"],
        ["study", "work", "travel", "sleep"],
        ["working", "studying", "living here", "teaching"]
    ]
    
    # Select template and word
    template_idx = random.randint(0, len(templates) - 1)
    template = templates[template_idx]
    word = random.choice(fill_words[template_idx])
    
    # Create English sentence
    english_sentence = template.format(word)
    
    # Translate sentence
    portuguese_sentence = translate_text(english_sentence, "en", "pt")
    if not portuguese_sentence:
        # Fallback if API fails
        portuguese_sentence = "Frase em português."
    
    # Create modified versions for wrong options
    wrong_options = []
    
    # For ser vs estar exercises
    if template_idx == 0:
        if "estou" in portuguese_sentence.lower():
            wrong_sentence = portuguese_sentence.lower().replace("estou", "sou")
        else:
            wrong_sentence = portuguese_sentence.lower().replace("sou", "estou")
        wrong_options.append(wrong_sentence.capitalize())
    
    # For preposition exercises
    elif template_idx == 1:
        prepositions = ["para", "a", "em", "de"]
        for prep in prepositions:
            if prep in portuguese_sentence.lower():
                continue
            # Replace the preposition
            for existing_prep in prepositions:
                if existing_prep in portuguese_sentence.lower():
                    wrong_sentence = portuguese_sentence.lower().replace(existing_prep, prep)
                    wrong_options.append(wrong_sentence.capitalize())
                    break
    
    # Ensure we have enough wrong options
    while len(wrong_options) < 3:
        words_to_change = ["eu", "ele", "ela", "nós", "eles", "ontem", "amanhã", "para", "em", "de", "muitos", "poucos"]
        
        # Create a sentence with error
        wrong_sentence = portuguese_sentence
        for word in words_to_change:
            if word in portuguese_sentence.lower():
                replacement = random.choice([w for w in words_to_change if w != word])
                wrong_sentence = wrong_sentence.lower().replace(word, replacement)
                break
        
        if wrong_sentence != portuguese_sentence and wrong_sentence not in wrong_options:
            wrong_options.append(wrong_sentence.capitalize())
    
    # Truncate to 3 wrong options if we have more
    wrong_options = wrong_options[:3]
    
    # Create options list including correct answer
    options = wrong_options + [portuguese_sentence]
    random.shuffle(options)
    
    # Create exercise
    exercise = {
        "question": f"Which is the correct Portuguese translation of: '{english_sentence}'",
        "options": options,
        "correct": portuguese_sentence,
        "explanation": f"The correct translation preserves the grammar of the original sentence."
    }
    
    return exercise

# Function to generate an exercise
def generate_exercise():
    """Generate a random exercise using one of the generation methods"""
    generators = [
        generate_vocabulary_exercise,
        generate_grammar_exercise
    ]
    
    generator = random.choice(generators)
    return generator()

# Generate multiple exercises
def generate_exercises(count=5):
    """Generate multiple exercises"""
    exercises = []
    for _ in range(count):
        try:
            exercise = generate_exercise()
            exercises.append(exercise)
        except Exception as e:
            print(f"Error generating exercise: {e}")
    
    return exercises

# Load or generate exercises
def load_or_generate_exercises(count=10):
    """Load exercises from file or generate new ones if needed"""
    try:
        with open('portuguese_exercises.json', 'r', encoding='utf-8') as file:
            exercises = json.load(file)
            if not exercises or len(exercises) < count:
                # Generate more exercises if needed
                new_exercises = generate_exercises(count - len(exercises))
                exercises.extend(new_exercises)
                with open('portuguese_exercises.json', 'w', encoding='utf-8') as outfile:
                    json.dump(exercises, outfile, ensure_ascii=False, indent=4)
            return exercises
    except FileNotFoundError:
        # Generate exercises if file doesn't exist
        exercises = generate_exercises(count)
        with open('portuguese_exercises.json', 'w', encoding='utf-8') as file:
            json.dump(exercises, file, ensure_ascii=False, indent=4)
        return exercises

# Function to send a random exercise
def send_exercise(chat_id=None):
    if chat_id is None:
        chat_id = USER_CHAT_ID
    
    exercises = load_or_generate_exercises()    
    exercise = random.choice(exercises)
    current_exercise[chat_id] = exercise
    
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

# Handle the /now command to get an exercise immediately
@bot.message_handler(commands=['now'])
def now_command(message):
    chat_id = message.chat.id
    send_exercise(chat_id)

# Add a command to generate new exercises
@bot.message_handler(commands=['generate'])
def generate_command(message):
    chat_id = message.chat.id
    count = 5  # Default number of exercises to generate
    
    # Check if the command includes a number
    command_parts = message.text.split()
    if len(command_parts) > 1 and command_parts[1].isdigit():
        count = int(command_parts[1])
        if count > 20:  # Limit to reasonable number
            count = 20
    
    bot.send_message(chat_id, f"Generating {count} new Portuguese exercises using APIs...")
    
    # Generate new exercises
    new_exercises = generate_exercises(count)
    
    # Load existing exercises
    try:
        with open('portuguese_exercises.json', 'r', encoding='utf-8') as file:
            exercises = json.load(file)
    except FileNotFoundError:
        exercises = []
    
    # Add new exercises
    exercises.extend(new_exercises)
    
    # Save back to file
    with open('portuguese_exercises.json', 'w', encoding='utf-8') as file:
        json.dump(exercises, file, ensure_ascii=False, indent=4)
    
    bot.send_message(chat_id, f"Added {len(new_exercises)} new exercises to the database! Total exercises: {len(exercises)}")
    
    # Send a sample of the new exercises
    if new_exercises:
        sample = random.choice(new_exercises)
        bot.send_message(chat_id, f"Sample new exercise:\n\n{sample['question']}\n\nOptions: {', '.join(sample['options'])}")

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
