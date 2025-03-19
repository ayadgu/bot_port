from collections import OrderedDict

# Structure de données améliorée pour organiser les cours par niveau
PORTUGUESE_LEVELS = {
    "A0": {
        "title": "Débutant complet",
        "courses": {
            "a0_1": {"title": "Salutations de base", "content": "...", "exercises": []},
            "a0_2": {"title": "Se présenter", "content": "...", "exercises": []},
            # Plus de cours...
        }
    },
    "A1": {
        "title": "Débutant",
        "courses": {
            # Courses for A1 level
        }
    },
    # A2, B1, etc.
}

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
                "question": "What is the Portuguese phrase for 'I don't understand'?",
                "options": ["Eu entendi", "Eu sei", "Eu não entendo", "Eu gosto"],
                "correct": "Eu não entendo",
                "explanation": "'Eu não entendo' means 'I don't understand'."
            },
            {
                "question": "Which word means 'Friend' in Portuguese?",
                "options": ["Amigo", "Amiga", "Amizade", "Amigável"],
                "correct": "Amigo",
                "explanation": "'Amigo' means 'Friend' in Portuguese."
            }
        ]
    }),
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