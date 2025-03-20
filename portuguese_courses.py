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

# Définition des thèmes d'exercices
EXERCISE_THEMES = {
    
    "shopping": {
        "title": "Faire les courses",
        "description": "Apprenez à parler de vos achats et à faire les courses en portugais",
        "exercises": [
            {
                "question": "Comment dire 'Combien ça coûte ?' en portugais ?",
                "options": ["Quanto tempo?", "Quanto custa?", "Como você está?", "O que você quer?"],
                "correct": "Quanto custa?",
                "explanation": "'Quanto custa?' signifie 'Combien ça coûte ?'"
            },
            {
                "question": "Comment dire 'Je voudrais acheter du pain' en portugais ?",
                "options": ["Eu quero vender pão", "Eu vou comer pão", "Eu quero comprar pão", "Eu preciso de pão"],
                "correct": "Eu quero comprar pão",
                "explanation": "'Eu quero comprar pão' signifie 'Je voudrais acheter du pain'"
            },
            {
                "question": "Comment demander 'Où est la caisse ?' en portugais ?",
                "options": ["Onde está o mercado?", "Onde está o caixa?", "Onde está o pão?", "Onde está o carrinho?"],
                "correct": "Onde está o caixa?",
                "explanation": "'Onde está o caixa?' signifie 'Où est la caisse ?'"
            },
            {
                "question": "Comment dire 'Avez-vous de la monnaie ?' en portugais ?",
                "options": ["Você tem troco?", "Você tem dinheiro?", "Você tem comida?", "Você tem uma bolsa?"],
                "correct": "Você tem troco?",
                "explanation": "'Você tem troco?' signifie 'Avez-vous de la monnaie ?'"
            },
            {
                "question": "Comment dire 'Je paie par carte' en portugais ?",
                "options": ["Eu pago em dinheiro", "Eu pago com cartão", "Eu pago com cheque", "Eu pago depois"],
                "correct": "Eu pago com cartão",
                "explanation": "'Eu pago com cartão' signifie 'Je paie par carte'"
            },
            {
                "question": "Comment demander 'Pouvez-vous me donner un sac ?' en portugais ?",
                "options": ["Você pode me dar um troco?", "Você pode me dar uma sacola?", "Você pode me dar uma moeda?", "Você pode me dar uma nota?"],
                "correct": "Você pode me dar uma sacola?",
                "explanation": "'Você pode me dar uma sacola?' signifie 'Pouvez-vous me donner un sac ?'"
            },
            {
                "question": "Comment dire 'Je cherche du lait' en portugais ?",
                "options": ["Eu estou procurando leite", "Eu estou bebendo leite", "Eu estou comprando leite", "Eu estou vendendo leite"],
                "correct": "Eu estou procurando leite",
                "explanation": "'Eu estou procurando leite' signifie 'Je cherche du lait'"
            },
            {
                "question": "Comment dire 'C'est trop cher' en portugais ?",
                "options": ["Está muito barato", "Está muito caro", "Está muito pequeno", "Está muito grande"],
                "correct": "Está muito caro",
                "explanation": "'Está muito caro' signifie 'C'est trop cher'"
            },
            {
                "question": "Comment dire 'Avez-vous des fruits frais ?' en portugais ?",
                "options": ["Você tem pão?", "Você tem carne?", "Você tem frutas frescas?", "Você tem leite?"],
                "correct": "Você tem frutas frescas?",
                "explanation": "'Você tem frutas frescas?' signifie 'Avez-vous des fruits frais ?'"
            },
            {
                "question": "Comment dire 'Je voudrais un kilo de pommes' en portugais ?",
                "options": ["Eu quero um quilo de maçãs", "Eu como um quilo de maçãs", "Eu vendo um quilo de maçãs", "Eu pago um quilo de maçãs"],
                "correct": "Eu quero um quilo de maçãs",
                "explanation": "'Eu quero um quilo de maçãs' signifie 'Je voudrais un kilo de pommes'"
            }
        ]
    },
    "travel": {
        "title": "Voyager",
        "description": "Apprenez à parler de vos déplacements et de vos voyages en portugais",
        "exercises": [
            {
                "question": "Comment dire 'Où est la gare ?' en portugais ?",
                "options": ["Onde está a escola?", "Onde está a estação?", "Onde está o hotel?", "Onde está o aeroporto?"],
                "correct": "Onde está a estação?",
                "explanation": "'Onde está a estação?' signifie 'Où est la gare ?'"
            },
            {
                "question": "Comment dire 'Je voudrais acheter un billet' en portugais ?",
                "options": ["Eu quero comprar uma passagem", "Eu quero pagar um bilhete", "Eu quero pedir um bilhete", "Eu quero trocar uma passagem"],
                "correct": "Eu quero comprar uma passagem",
                "explanation": "'Eu quero comprar uma passagem' signifie 'Je voudrais acheter un billet'"
            },
            {
                "question": "Comment dire 'À quelle heure part le train ?' en portugais ?",
                "options": ["Que horas sai o trem?", "Quando chega o trem?", "Onde está o trem?", "Quanto custa o trem?"],
                "correct": "Que horas sai o trem?",
                "explanation": "'Que horas sai o trem?' signifie 'À quelle heure part le train ?'"
            },
            {
                "question": "Comment dire 'Je voudrais une chambre pour deux nuits' en portugais ?",
                "options": ["Eu quero um quarto por duas noites", "Eu quero dormir por duas noites", "Eu quero ficar em um quarto", "Eu quero sair depois de duas noites"],
                "correct": "Eu quero um quarto por duas noites",
                "explanation": "'Eu quero um quarto por duas noites' signifie 'Je voudrais une chambre pour deux nuits'"
            },
            {
                "question": "Comment demander 'Pouvez-vous m'appeler un taxi ?' en portugais ?",
                "options": ["Você pode me dar um táxi?", "Você pode me chamar um táxi?", "Você pode me pagar um táxi?", "Você pode me mostrar um táxi?"],
                "correct": "Você pode me chamar um táxi?",
                "explanation": "'Você pode me chamar um táxi?' signifie 'Pouvez-vous m'appeler un taxi ?'"
            },
            {
                "question": "Comment dire 'Je suis perdu' en portugais ?",
                "options": ["Eu estou feliz", "Eu estou cansado", "Eu estou perdido", "Eu estou preocupado"],
                "correct": "Eu estou perdido",
                "explanation": "'Eu estou perdido' signifie 'Je suis perdu'"
            },
            {
                "question": "Comment dire 'Est-ce loin d'ici ?' en portugais ?",
                "options": ["Está aqui?", "Está longe daqui?", "Está perto daqui?", "Está ao lado?"],
                "correct": "Está longe daqui?",
                "explanation": "'Está longe daqui?' signifie 'Est-ce loin d'ici ?'"
            },
            {
                "question": "Comment dire 'Pouvez-vous me prendre en photo ?' en portugais ?",
                "options": ["Você pode me ajudar?", "Você pode me pegar?", "Você pode tirar uma foto minha?", "Você pode me ouvir?"],
                "correct": "Você pode tirar uma foto minha?",
                "explanation": "'Você pode tirar uma foto minha?' signifie 'Pouvez-vous me prendre en photo ?'"
            },
            {
                "question": "Comment dire 'Je voudrais une carte de la ville' en portugais ?",
                "options": ["Eu quero uma passagem", "Eu quero um mapa da cidade", "Eu quero uma chave", "Eu quero um quarto"],
                "correct": "Eu quero um mapa da cidade",
                "explanation": "'Eu quero um mapa da cidade' signifie 'Je voudrais une carte de la ville'"
            },
            {
                "question": "Comment dire 'Où est le musée ?' en portugais ?",
                "options": ["Onde está o mercado?", "Onde está a estação?", "Onde está o museu?", "Onde está a escola?"],
                "correct": "Onde está o museu?",
                "explanation": "'Onde está o museu?' signifie 'Où est le musée ?'"
            }
        ]
    },
    "ser_estar": {
    "title": "Différence entre 'ser' et 'estar'",
    "description": "Apprenez à utiliser correctement les verbes 'ser' et 'estar' en portugais",
    "exercises": [
        {
            "question": "Comment dit-on 'Je suis étudiant' en portugais?",
            "options": ["Eu sou estudante", "Eu estou estudante"],
            "correct": "Eu sou estudante",
            "explanation": "'Ser' est utilisé pour une identité ou une profession."
        },
        {
            "question": "Comment dit-on 'Je suis fatigué' en portugais?",
            "options": ["Eu sou cansado", "Eu estou cansado"],
            "correct": "Eu estou cansado",
            "explanation": "'Estar' est utilisé pour un état temporaire."
        },
        {
            "question": "Comment dit-on 'Elle est contente' en portugais?",
            "options": ["Ela é feliz", "Ela está feliz"],
            "correct": "Ela está feliz",
            "explanation": "'Estar' est utilisé pour un état émotionnel temporaire."
        },
        {
            "question": "Comment dit-on 'Il est professeur' en portugais?",
            "options": ["Ele é professor", "Ele está professor"],
            "correct": "Ele é professor",
            "explanation": "'Ser' est utilisé pour une profession."
        },
        {
            "question": "Comment dit-on 'Nous sommes au restaurant' en portugais?",
            "options": ["Nós somos no restaurante", "Nós estamos no restaurante"],
            "correct": "Nós estamos no restaurante",
            "explanation": "'Estar' est utilisé pour une localisation temporaire."
        },
        {
            "question": "Comment dit-on 'Je suis brésilien' en portugais?",
            "options": ["Eu sou brasileiro", "Eu estou brasileiro"],
            "correct": "Eu sou brasileiro",
            "explanation": "'Ser' est utilisé pour la nationalité."
        },
        {
            "question": "Comment dit-on 'Il est malade' en portugais?",
            "options": ["Ele é doente", "Ele está doente"],
            "correct": "Ele está doente",
            "explanation": "'Estar' est utilisé pour un état temporaire."
        },
        {
            "question": "Comment dit-on 'Tu es intelligent' en portugais?",
            "options": ["Você é inteligente", "Você está inteligente"],
            "correct": "Você é inteligente",
            "explanation": "'Ser' est utilisé pour une qualité permanente."
        },
        {
            "question": "Comment dit-on 'Il est en retard' en portugais?",
            "options": ["Ele é atrasado", "Ele está atrasado"],
            "correct": "Ele está atrasado",
            "explanation": "'Estar' est utilisé pour une situation temporaire."
        },
        {
            "question": "Comment dit-on 'La maison est grande' en portugais?",
            "options": ["A casa é grande", "A casa está grande"],
            "correct": "A casa é grande",
            "explanation": "'Ser' est utilisé pour une caractéristique permanente."
        }
    ]
},
"culture_et_traditions": {
    "title": "Culture et traditions brésiliennes",
    "description": "Apprenez à parler des fêtes, coutumes et traditions brésiliennes",
    "exercises": [
        {
            "question": "Quelle est la plus grande fête traditionnelle du Brésil, connue pour ses défilés de samba?",
            "options": ["Carnaval", "Festa Junina"],
            "correct": "Carnaval",
            "explanation": "Le Carnaval est la plus grande fête du Brésil, célèbre pour ses défilés et ses costumes colorés."
        },
        {
            "question": "Quelle danse est traditionnellement associée à la culture brésilienne?",
            "options": ["Samba", "Flamenco"],
            "correct": "Samba",
            "explanation": "La samba est une danse et un genre musical typiquement brésilien."
        },
        {
            "question": "Que célèbre-t-on lors de la 'Festa Junina'?",
            "options": ["L'arrivée du printemps", "Les saints catholiques"],
            "correct": "Les saints catholiques",
            "explanation": "La 'Festa Junina' célèbre Saint Jean, Saint Pierre et Saint Antoine en juin."
        },
        {
            "question": "Quelle boisson est typiquement consommée pendant le Carnaval?",
            "options": ["Caipirinha", "Mojito"],
            "correct": "Caipirinha",
            "explanation": "La caipirinha est le cocktail national du Brésil, à base de cachaça, de sucre et de citron vert."
        },
        {
            "question": "Quel sport est considéré comme une véritable passion nationale au Brésil?",
            "options": ["Football", "Basketball"],
            "correct": "Football",
            "explanation": "Le football est le sport le plus populaire au Brésil."
        },
        {
            "question": "Comment appelle-t-on la musique traditionnelle originaire de Bahia, au Brésil?",
            "options": ["Forró", "Axé"],
            "correct": "Axé",
            "explanation": "L'Axé est un genre musical populaire à Bahia, influencé par le reggae et le samba."
        },
        {
            "question": "Quelle est la langue officielle du Brésil?",
            "options": ["Espagnol", "Portugais"],
            "correct": "Portugais",
            "explanation": "Le portugais est la langue officielle du Brésil."
        },
        {
            "question": "Que représente le 7 septembre au Brésil?",
            "options": ["Fête de l'Indépendance", "Fête nationale"],
            "correct": "Fête de l'Indépendance",
            "explanation": "Le 7 septembre est la date de l'indépendance du Brésil (1822)."
        },
        {
            "question": "Quel célèbre genre musical brésilien est connu pour son rythme lent et sensuel?",
            "options": ["Bossa nova", "Salsa"],
            "correct": "Bossa nova",
            "explanation": "La bossa nova est un genre musical brésilien influencé par le jazz et la samba."
        },
        {
            "question": "Quel instrument de percussion est utilisé dans la capoeira?",
            "options": ["Berimbau", "Tamborim"],
            "correct": "Berimbau",
            "explanation": "Le berimbau est un instrument utilisé dans la capoeira, une danse-lutte brésilienne."
        }
    ]
}
,
"technologie": {
    "title": "Technologie en portugais",
    "description": "Apprenez à parler de la technologie et du numérique",
    "exercises": [
        {
            "question": "Comment dit-on 'ordinateur' en portugais?",
            "options": ["Computador", "Ordenador"],
            "correct": "Computador",
            "explanation": "En portugais brésilien, on utilise le terme 'computador'."
        },
        {
            "question": "Comment dit-on 'mot de passe' en portugais?",
            "options": ["Senha", "Palavra"],
            "correct": "Senha",
            "explanation": "'Senha' est le mot utilisé pour 'mot de passe' en portugais."
        },
        {
            "question": "Comment dit-on 'courrier électronique' en portugais?",
            "options": ["Email", "Correio eletrônico"],
            "correct": "Email",
            "explanation": "'Email' est le terme le plus utilisé pour 'courrier électronique' au Brésil."
        },
        {
            "question": "Comment appelle-t-on un téléphone portable au Brésil?",
            "options": ["Celular", "Telemóvel"],
            "correct": "Celular",
            "explanation": "'Celular' est le mot brésilien pour téléphone portable."
        },
        {
            "question": "Comment dit-on 'site web' en portugais?",
            "options": ["Website", "Site"],
            "correct": "Site",
            "explanation": "'Site' est le mot le plus couramment utilisé au Brésil."
        },
        {
            "question": "Comment dit-on 'clavier' en portugais?",
            "options": ["Teclado", "Tecla"],
            "correct": "Teclado",
            "explanation": "'Teclado' est le mot portugais pour clavier."
        },
        {
            "question": "Comment dit-on 'application' en portugais?",
            "options": ["App", "Aplicativo"],
            "correct": "Aplicativo",
            "explanation": "'Aplicativo' est le terme correct pour une application au Brésil."
        },
        {
            "question": "Comment dit-on 'réseau social' en portugais?",
            "options": ["Rede social", "Rede pública"],
            "correct": "Rede social",
            "explanation": "'Rede social' signifie réseau social."
        },
        {
            "question": "Comment dit-on 'télécharger' en portugais?",
            "options": ["Descarregar", "Baixar"],
            "correct": "Baixar",
            "explanation": "'Baixar' est le mot le plus utilisé au Brésil pour 'télécharger'."
        },
        {
            "question": "Comment dit-on 'imprimante' en portugais?",
            "options": ["Impressor", "Impressora"],
            "correct": "Impressora",
            "explanation": "'Impressora' est le terme pour imprimante en portugais."
        }
    ]
}
,
"relations_sociales": {
        "title": "Relations sociales en portugais",
        "description": "Apprenez à parler des relations sociales et des interactions en portugais",
        "exercises": [
            {
                "question": "Comment dit-on 'Je suis content de te voir' en portugais ?",
                "options": ["Estou feliz de te ver", "Fico feliz de ver você", "Eu gosto de ver você", "Estou bem, e você?"],
                "correct": "Estou feliz de te ver",
                "explanation": "'Estou feliz de te ver' est la manière la plus courante de dire cela."
            },
            {
                "question": "Comment demander 'Comment ça va ?' en portugais ?",
                "options": ["Tudo bem?", "Como vai?", "Onde você está?", "Qual é o seu nome?"],
                "correct": "Tudo bem?",
                "explanation": "'Tudo bem?' est l'expression la plus utilisée pour demander comment ça va."
            },
            {
                "question": "Comment dire 'J'ai besoin de parler à quelqu'un' en portugais ?",
                "options": ["Preciso falar com alguém", "Quero falar com você", "Eu falo com alguém", "Eu preciso ir à loja"],
                "correct": "Preciso falar com alguém",
                "explanation": "'Preciso falar com alguém' est l'expression correcte."
            },
            {
                "question": "Comment dire 'Je suis désolé(e)' en portugais ?",
                "options": ["Desculpe", "Eu me desculpo", "Sinto muito", "Eu te amo"],
                "correct": "Sinto muito",
                "explanation": "'Sinto muito' est souvent plus formel pour exprimer des excuses."
            },
            {
                "question": "Comment dire 'Je t'aime' en portugais ?",
                "options": ["Eu gosto de você", "Eu te amo", "Eu te adoro", "Eu sou apaixonado(a) por você"],
                "correct": "Eu te amo",
                "explanation": "'Eu te amo' est la phrase standard pour dire 'Je t'aime'."
            },
            {
                "question": "Comment demander 'Tu veux sortir avec moi ?' en portugais ?",
                "options": ["Você quer sair comigo?", "Você gosta de mim?", "Posso te ajudar?", "Eu vou sair hoje"],
                "correct": "Você quer sair comigo?",
                "explanation": "'Você quer sair comigo?' est la manière courante de demander à quelqu'un de sortir."
            },
            {
                "question": "Comment dire 'Je ne suis pas intéressé(e)' en portugais ?",
                "options": ["Não estou interessado(a)", "Eu não gosto", "Não quero", "Eu te odeio"],
                "correct": "Não estou interessado(a)",
                "explanation": "'Não estou interessado(a)' est la manière polie de refuser."
            },
            {
                "question": "Comment dire 'Il/Elle est mon meilleur ami(e)' en portugais ?",
                "options": ["Ele/Ela é meu melhor amigo(a)", "Ele/Ela é meu namorado(a)", "Ele/Ela é meu colega", "Ele/Ela é minha irmã"],
                "correct": "Ele/Ela é meu melhor amigo(a)",
                "explanation": "'Ele/Ela é meu melhor amigo(a)' est la manière correcte de dire que quelqu'un est votre meilleur ami."
            },
            {
                "question": "Comment dire 'J'ai un rendez-vous' en portugais ?",
                "options": ["Eu tenho um encontro", "Eu tenho uma reunião", "Eu vou ao médico", "Eu estou ocupado(a)"],
                "correct": "Eu tenho um encontro",
                "explanation": "'Eu tenho um encontro' signifie que vous avez un rendez-vous."
            },
            {
                "question": "Comment dire 'À tout de suite' en portugais ?",
                "options": ["Até logo", "Até já", "Até amanhã", "Tchau"],
                "correct": "Até já",
                "explanation": "'Até já' est plus informel pour dire 'À tout de suite'."
            }
        ]
    }
    ,
     "jours_de_la_semaine": {
        "title": "Jours de la semaine en portugais",
        "description": "Apprenez à parler des jours de la semaine en portugais",
        "exercises": [
            {
                "question": "Comment dit-on 'Aujourd'hui, c'est lundi' en portugais ?",
                "options": ["Hoje é segunda-feira", "Hoje é terça-feira", "Hoje é sexta-feira", "Hoje é domingo"],
                "correct": "Hoje é segunda-feira",
                "explanation": "'Hoje é segunda-feira' signifie 'Aujourd'hui, c'est lundi'."
            },
            {
                "question": "Comment dit-on 'Demain, ce sera vendredi' en portugais ?",
                "options": ["Amanhã será terça-feira", "Amanhã será quinta-feira", "Amanhã será domingo", "Amanhã será sexta-feira"],
                "correct": "Amanhã será sexta-feira",
                "explanation": "L'expression correcte pour dire 'Demain, ce sera vendredi' est 'Amanhã será sexta-feira'."
            },
            {
                "question": "Quel jour vient après mercredi ?",
                "options": ["Jeudi", "Mardi", "Lundi", "Dimanche"],
                "correct": "Quinta-feira",
                "explanation": "En portugais, jeudi est 'quinta-feira', qui suit mercredi (quarta-feira)."
            },
            {
                "question": "Comment dit-on 'Je travaille du lundi au vendredi' en portugais ?",
                "options": ["Eu trabalho de segunda a sexta-feira", "Eu trabalho de terça a sábado", "Eu trabalho de segunda a quarta-feira", "Eu trabalho de quarta a domingo"],
                "correct": "Eu trabalho de segunda a sexta-feira",
                "explanation": "'Eu trabalho de segunda a sexta-feira' est la manière correcte de dire 'Je travaille du lundi au vendredi'."
            },
            {
                "question": "Comment dit-on 'Le week-end est samedi et dimanche' en portugais ?",
                "options": ["O fim de semana é sábado e domingo", "O fim de semana é quinta e sexta", "O fim de semana é sexta et samedi", "O fim de semana é terça et quarta"],
                "correct": "O fim de semana é sábado e domingo",
                "explanation": "'O fim de semana' désigne le week-end qui est composé du samedi et du dimanche."
            },
            {
                "question": "Quel jour est-ce aujourd'hui si hier était dimanche ?",
                "options": ["Segunda-feira", "Terça-feira", "Quarta-feira", "Sexta-feira"],
                "correct": "Segunda-feira",
                "explanation": "Si hier était dimanche (domingo), aujourd'hui est lundi (segunda-feira)."
            },
            {
                "question": "Comment dit-on 'Il est mardi' en portugais ?",
                "options": ["Hoje é terça-feira", "Hoje é quinta-feira", "Hoje é domingo", "Hoje é segunda-feira"],
                "correct": "Hoje é terça-feira",
                "explanation": "Terça-feira est le mot portugais pour mardi."
            },
            {
                "question": "Quel jour de la semaine commence par 'S' en portugais ?",
                "options": ["Segunda-feira", "Sábado", "Quinta-feira", "Terça-feira"],
                "correct": "Sábado",
                "explanation": "Sábado (samedi) commence par 'S' en portugais."
            },
            {
                "question": "Quel jour de la semaine est avant vendredi ?",
                "options": ["Quinta-feira", "Segunda-feira", "Terça-feira", "Quarta-feira"],
                "correct": "Quinta-feira",
                "explanation": "Quinta-feira (jeudi) est avant sexta-feira (vendredi)."
            },
            {
                "question": "Comment dit-on 'Nous avons une réunion le mercredi' en portugais ?",
                "options": ["Nós temos uma reunião na terça-feira", "Nós temos uma reunião na segunda-feira", "Nós temos uma reunião na quarta-feira", "Nós temos uma reunião no sábado"],
                "correct": "Nós temos uma reunião na quarta-feira",
                "explanation": "La réunion est le mercredi, donc 'na quarta-feira' (mercredi)."
            }
        ]
    },
    "conjugaison_de_base": {
    "title": "Conjugaison de base en portugais",
    "description": "Apprenez les bases de la conjugaison des verbes en portugais",
    "exercises": [
        {
            "question": "Comment conjugue-t-on le verbe 'être' (ser) au présent de l'indicatif pour 'eu'?",
            "options": ["Sou", "Estou", "É", "Sei"],
            "correct": "Sou",
            "explanation": "'Sou' est la forme correcte du verbe 'ser' pour 'eu' au présent."
        },
        {
            "question": "Comment conjugue-t-on le verbe 'avoir' (ter) au présent de l'indicatif pour 'tu'?",
            "options": ["Tenho", "Tens", "Tem", "Têm"],
            "correct": "Tens",
            "explanation": "'Tens' est la forme correcte du verbe 'ter' pour 'tu' au présent."
        },
        {
            "question": "Comment conjugue-t-on le verbe 'manger' (comer) au présent de l'indicatif pour 'eles'? ",
            "options": ["Comem", "Comi", "Comeram", "Come"],
            "correct": "Comem",
            "explanation": "'Comem' est la forme correcte du verbe 'comer' pour 'eles' au présent."
        },
        {
            "question": "Comment conjugue-t-on le verbe 'aller' (ir) au présent de l'indicatif pour 'eu'?",
            "options": ["Vou", "Vai", "Vais", "Irá"],
            "correct": "Vou",
            "explanation": "'Vou' est la forme correcte du verbe 'ir' pour 'eu' au présent."
        },
        {
            "question": "Comment conjugue-t-on le verbe 'parler' (falar) au présent de l'indicatif pour 'você'?",
            "options": ["Falo", "Fala", "Falamos", "Falam"],
            "correct": "Fala",
            "explanation": "'Fala' est la forme correcte du verbe 'falar' pour 'você' au présent."
        }
    ]
},
"nationalites": {
    "title": "Les nationalités en portugais",
    "description": "Apprenez à parler des nationalités et à poser des questions sur l'origine des gens.",
    "exercises": [
        {
            "question": "Comment dit-on 'Je suis français' en portugais?",
            "options": ["Eu sou francês", "Eu sou francesa", "Eu sou francesa", "Eu sou francês"],
            "correct": "Eu sou francês",
            "explanation": "'Eu sou francês' est la façon correcte de dire 'Je suis français'."
        },
        {
            "question": "Comment demande-t-on 'D'où viens-tu?' en portugais?",
            "options": ["De onde você é?", "Onde você mora?", "Qual a sua nacionalidade?", "Como se chama?"],
            "correct": "De onde você é?",
            "explanation": "'De onde você é?' est la question pour demander d'où vient quelqu'un."
        },
        {
            "question": "Comment dit-on 'Je suis brésilien' en portugais?",
            "options": ["Eu sou brasileiro", "Eu sou brésilienne", "Eu sou brésilienne", "Eu sou brésilien"],
            "correct": "Eu sou brasileiro",
            "explanation": "'Eu sou brasileiro' est la façon correcte de dire 'Je suis brésilien'."
        },
        {
            "question": "Comment dit-on 'Ils sont italiens' en portugais?",
            "options": ["Eles são italianos", "Eles são italianas", "Eles são italianos", "Eles são italianas"],
            "correct": "Eles são italianos",
            "explanation": "'Eles são italianos' est la façon correcte de dire 'Ils sont italiens'."
        },
        {
            "question": "Comment dit-on 'Je suis chinois' en portugais?",
            "options": ["Eu sou chinês", "Eu sou chinesa", "Eu sou chinês", "Eu sou chinesa"],
            "correct": "Eu sou chinês",
            "explanation": "'Eu sou chinês' est la façon correcte de dire 'Je suis chinois'."
        }
    ]
},
"nombres": {
    "title": "Les nombres en portugais",
    "description": "Apprenez à compter et utiliser les nombres en portugais.",
    "exercises": [
        {
            "question": "Comment dit-on 'dix' en portugais?",
            "options": ["Dez", "Diz", "Vinte", "Onze"],
            "correct": "Dez",
            "explanation": "'Dez' est le mot correct pour 'dix' en portugais."
        },
        {
            "question": "Comment dit-on 'cent' en portugais?",
            "options": ["Cem", "Cento", "Centa", "Cento"],
            "correct": "Cem",
            "explanation": "'Cem' est le mot correct pour 'cent' en portugais."
        },
        {
            "question": "Comment dit-on 'vingt-cinq' en portugais?",
            "options": ["Vinte e cinco", "Cinco e vinte", "Vinte e muitos", "Cinco e vinte"],
            "correct": "Vinte e cinco",
            "explanation": "'Vinte e cinco' est la façon correcte de dire 'vingt-cinq'."
        },
        {
            "question": "Comment dit-on 'trente' en portugais?",
            "options": ["Trinta", "Trinta", "Vinte e quatro", "Vinte"],
            "correct": "Trinta",
            "explanation": "'Trinta' est le mot correct pour 'trente' en portugais."
        },
        {
            "question": "Comment dit-on 'quarante' en portugais?",
            "options": ["Quarenta", "Cinco", "Vinte", "Cento"],
            "correct": "Quarenta",
            "explanation": "'Quarenta' est le mot correct pour 'quarante' en portugais."
        }
    ]
}
,
  "culture_and_traditions": {
    "title": "Culture et traditions",
    "description": "Découvrez les aspects culturels et les traditions du Brésil",
    "exercises": [
      {
        "question": "Quelle danse est typiquement associée au Brésil ?",
        "options": ["Samba", "Flamenco", "Tango", "Valse"],
        "correct": "Samba",
        "explanation": "La samba est une danse populaire brésilienne associée au carnaval."
      },
      {
        "question": "Quelle ville est célèbre pour son carnaval au Brésil ?",
        "options": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador"],
        "correct": "Rio de Janeiro",
        "explanation": "Le carnaval de Rio de Janeiro est l'un des plus grands du monde."
      },
      {
        "question": "Quelle est la langue officielle du Brésil ?",
        "options": ["Espagnol", "Portugais", "Français", "Anglais"],
        "correct": "Portugais",
        "explanation": "Le portugais est la langue officielle du Brésil."
      },
      {
        "question": "Quelle religion est la plus pratiquée au Brésil ?",
        "options": ["Christianisme", "Islam", "Bouddhisme", "Hindouisme"],
        "correct": "Christianisme",
        "explanation": "Le christianisme (principalement le catholicisme) est la religion dominante au Brésil."
      },
      {
        "question": "Quelle boisson est typiquement associée au Brésil ?",
        "options": ["Sangria", "Caipirinha", "Mojito", "Pisco Sour"],
        "correct": "Caipirinha",
        "explanation": "La caipirinha est un cocktail brésilien à base de cachaça, citron vert et sucre."
      },
      {
        "question": "Quel sport est le plus populaire au Brésil ?",
        "options": ["Basketball", "Football", "Rugby", "Volleyball"],
        "correct": "Football",
        "explanation": "Le football est une passion nationale au Brésil."
      },
      {
        "question": "Comment s'appelle la célèbre statue à Rio de Janeiro ?",
        "options": ["Statue de la Liberté", "Christ Rédempteur", "Colosse de Rhodes", "Statue de David"],
        "correct": "Christ Rédempteur",
        "explanation": "Le Christ Rédempteur est un symbole de Rio de Janeiro."
      },
      {
        "question": "Quel est le plus grand fleuve du Brésil ?",
        "options": ["Mississippi", "Nil", "Amazone", "Yangtsé"],
        "correct": "Amazone",
        "explanation": "L'Amazone est le plus grand fleuve du monde en volume d'eau."
      },
      {
        "question": "Quel plat est typiquement brésilien ?",
        "options": ["Paella", "Feijoada", "Tacos", "Risotto"],
        "correct": "Feijoada",
        "explanation": "La feijoada est un plat de haricots noirs avec de la viande."
      },
      {
        "question": "Quelle ville est connue pour son architecture moderniste au Brésil ?",
        "options": ["São Paulo", "Brasília", "Salvador", "Curitiba"],
        "correct": "Brasília",
        "explanation": "Brasília a été conçue par l'architecte Oscar Niemeyer."
      }
    ]
  },
  "technology": {
    "title": "Technologie",
    "description": "Apprenez le vocabulaire lié à la technologie en portugais",
    "exercises": [
      {
        "question": "Comment dit-on 'ordinateur' en portugais ?",
        "options": ["Computador", "Ordenador", "Laptop", "Máquina"],
        "correct": "Computador",
        "explanation": "Le mot 'computador' signifie 'ordinateur' en portugais brésilien."
      },
      {
        "question": "Comment dit-on 'clavier' en portugais ?",
        "options": ["Tecla", "Mouse", "Tela", "Teclado"],
        "correct": "Teclado",
        "explanation": "Le mot 'teclado' signifie 'clavier'."
      },
      {
        "question": "Quel terme désigne une connexion Internet sans fil ?",
        "options": ["Ethernet", "Wi-Fi", "Bluetooth", "Modem"],
        "correct": "Wi-Fi",
        "explanation": "'Wi-Fi' est utilisé pour désigner une connexion sans fil."
      },
      {
        "question": "Comment dit-on 'écran' en portugais ?",
        "options": ["Tela", "Teclado", "Monitor", "Mural"],
        "correct": "Tela",
        "explanation": "'Tela' signifie 'écran' en portugais."
      },
      {
        "question": "Comment dit-on 'mot de passe' en portugais ?",
        "options": ["Senha", "Código", "Tecla", "Login"],
        "correct": "Senha",
        "explanation": "'Senha' signifie 'mot de passe'."
      },
      {
        "question": "Comment dit-on 'logiciel' en portugais ?",
        "options": ["Hardware", "Software", "Programa", "Código"],
        "correct": "Programa",
        "explanation": "'Programa' est le mot pour 'logiciel'."
      },
      {
        "question": "Comment dit-on 'souris' (informatique) en portugais ?",
        "options": ["Teclado", "Tela", "Mouse", "Senha"],
        "correct": "Mouse",
        "explanation": "'Mouse' est le terme utilisé en portugais brésilien pour 'souris'."
      },
      {
        "question": "Comment dit-on 'navigateur' en portugais ?",
        "options": ["Programa", "Navegador", "Internet", "Página"],
        "correct": "Navegador",
        "explanation": "'Navegador' signifie 'navigateur' en portugais."
      },
      {
        "question": "Comment dit-on 'télécharger' en portugais ?",
        "options": ["Baixar", "Uploadar", "Conectar", "Salvar"],
        "correct": "Baixar",
        "explanation": "'Baixar' signifie 'télécharger' en portugais brésilien."
      },
      {
        "question": "Comment dit-on 'site web' en portugais ?",
        "options": ["Programa", "Página", "Navegador", "Website"],
        "correct": "Página",
        "explanation": "'Página' est le mot pour 'site web'."
      }
    ]
  }
,

    "presentation": {
        "title": "Se présenter en portugais brésilien",
        "description": "Apprenez à vous présenter et à parler de vous en portugais brésilien",
        "exercises": [
            {
                "question": "Comment dit-on 'Je m'appelle...' en portugais?",
                "options": ["Eu sou...", "Me chamo...", "Estou...", "Tenho..."],
                "correct": "Me chamo...",
                "explanation": "'Me chamo...' est la façon la plus courante de dire 'Je m'appelle...'"
            },
            {
                "question": "Comment demander 'Comment t'appelles-tu?' en portugais brésilien?",
                "options": ["Como você está?", "Quanto anos tem?", "Como você se chama?", "De onde você é?"],
                "correct": "Como você se chama?",
                "explanation": "'Como você se chama?' est la forme brésilienne pour demander le nom de quelqu'un"
            },
            {
                "question": "Comment dit-on 'J'ai ... ans' en portugais?",
                "options": ["Eu sou ... anos", "Tenho ... anos", "Estou ... anos", "Meu ... anos"],
                "correct": "Tenho ... anos",
                "explanation": "'Tenho ... anos' est la façon correcte d'indiquer son âge"
            },
            {
                "question": "Comment dit-on 'Je suis de France' en portugais brésilien?",
                "options": ["Eu venho da França", "Eu sou da França", "Eu moro na França", "Eu visito a França"],
                "correct": "Eu sou da França",
                "explanation": "'Eu sou da França' est la traduction directe de 'Je suis de France'"
            },
            {
                "question": "Comment dit-on 'Je parle français' en portugais?",
                "options": ["Eu falo francês", "Eu digo francês", "Eu entendo francês", "Eu estudo francês"],
                "correct": "Eu falo francês",
                "explanation": "'Eu falo francês' signifie littéralement 'Je parle français'"
            },
            {
                "question": "Comment dit-on 'J'habite à Paris' en portugais brésilien?",
                "options": ["Eu vivo em Paris", "Eu moro em Paris", "Eu estou em Paris", "Eu visito Paris"],
                "correct": "Eu moro em Paris",
                "explanation": "'Eu moro em Paris' est l'expression courante pour dire où l'on habite"
            },
            {
                "question": "Comment dit-on 'Enchanté(e) de faire votre connaissance' en portugais?",
                "options": ["Bom dia", "Muito prazer", "Até logo", "Obrigado(a)"],
                "correct": "Muito prazer",
                "explanation": "'Muito prazer' (littéralement 'beaucoup de plaisir') est l'équivalent de 'Enchanté(e)'"
            },
            {
                "question": "Comment demander 'Que fais-tu dans la vie?' en portugais brésilien?",
                "options": ["O que você gosta?", "Onde você trabalha?", "O que você faz?", "Como é sua vida?"],
                "correct": "O que você faz?",
                "explanation": "'O que você faz?' est la façon simple de demander ce que quelqu'un fait comme métier"
            },
            {
                "question": "Comment dit-on 'Je suis étudiant(e)' en portugais?",
                "options": ["Eu aprendo", "Eu ensino", "Eu sou estudante", "Eu vou à escola"],
                "correct": "Eu sou estudante",
                "explanation": "'Eu sou estudante' est la traduction directe de 'Je suis étudiant(e)'"
            },
            {
                "question": "Comment dit-on 'Au revoir, à bientôt' en portugais brésilien?",
                "options": ["Olá, até mais", "Adeus, nunca mais", "Tchau, até logo", "Bom dia, até amanhã"],
                "correct": "Tchau, até logo",
                "explanation": "'Tchau' est le 'au revoir' informel, et 'até logo' signifie 'à bientôt'"
            }
        ]
    },
    "daily_routine": {
        "title": "La routine quotidienne",
        "description": "Apprenez à parler de vos activités quotidiennes en portugais",
        "exercises": [
            {
                "question": "Comment dit-on 'Je me réveille à 7 heures' en portugais?",
                "options": ["Eu acordo às 7 horas", "Eu durmo às 7 horas", "Eu saio às 7 horas", "Eu chego às 7 horas"],
                "correct": "Eu acordo às 7 horas",
                "explanation": "'Eu acordo às 7 horas' est la traduction correcte de 'Je me réveille à 7 heures'"
            },
            {
                "question": "Comment dit-on 'Je prends une douche' en portugais?",
                "options": ["Eu tomo banho", "Eu lavo o rosto", "Eu escovo os dentes", "Eu visto a roupa"],
                "correct": "Eu tomo banho",
                "explanation": "'Eu tomo banho' signifie 'Je prends une douche'"
            },
            {
                "question": "Comment dire 'Je prends le petit-déjeuner' en portugais?",
                "options": ["Eu almoço", "Eu tomo café da manhã", "Eu como um lanche", "Eu faço o jantar"],
                "correct": "Eu tomo café da manhã",
                "explanation": "'Eu tomo café da manhã' signifie 'Je prends le petit-déjeuner'"
            },
            {
                "question": "Comment dire 'Je vais au travail' en portugais?",
                "options": ["Eu vou para o trabalho", "Eu chego em casa", "Eu saio da escola", "Eu descanso"],
                "correct": "Eu vou para o trabalho",
                "explanation": "'Eu vou para o trabalho' est la traduction correcte de 'Je vais au travail'"
            },
            {
                "question": "Comment dire 'Je déjeune à midi' en portugais?",
                "options": ["Eu janto ao meio-dia", "Eu almoço ao meio-dia", "Eu lancho ao meio-dia", "Eu como ao meio-dia"],
                "correct": "Eu almoço ao meio-dia",
                "explanation": "'Eu almoço ao meio-dia' signifie 'Je déjeune à midi'"
            },
            {
                "question": "Comment dire 'Je fais une sieste après le déjeuner' en portugais?",
                "options": ["Eu descanso depois do jantar", "Eu durmo antes do almoço", "Eu tiro uma soneca depois do almoço", "Eu como depois do almoço"],
                "correct": "Eu tiro uma soneca depois do almoço",
                "explanation": "'Eu tiro uma soneca depois do almoço' est la façon de dire 'Je fais une sieste après le déjeuner'"
            },
            {
                "question": "Comment dire 'Je rentre à la maison à 18 heures' en portugais?",
                "options": ["Eu saio às 18 horas", "Eu chego em casa às 18 horas", "Eu durmo às 18 horas", "Eu como às 18 horas"],
                "correct": "Eu chego em casa às 18 horas",
                "explanation": "'Eu chego em casa às 18 horas' est la traduction correcte de 'Je rentre à la maison à 18 heures'"
            },
            {
                "question": "Comment dire 'Je dîne à 20 heures' en portugais?",
                "options": ["Eu almoço às 20 horas", "Eu janto às 20 horas", "Eu como às 20 horas", "Eu lancho às 20 horas"],
                "correct": "Eu janto às 20 horas",
                "explanation": "'Eu janto às 20 horas' signifie 'Je dîne à 20 heures'"
            },
            {
                "question": "Comment dire 'Je regarde la télévision avant de dormir' en portugais?",
                "options": ["Eu assisto TV antes de dormir", "Eu como antes de dormir", "Eu trabalho antes de dormir", "Eu acordo antes de dormir"],
                "correct": "Eu assisto TV antes de dormir",
                "explanation": "'Eu assisto TV antes de dormir' signifie 'Je regarde la télévision avant de dormir'"
            },
            {
                "question": "Comment dire 'Je vais dormir à 22 heures' en portugais?",
                "options": ["Eu acordo às 22 horas", "Eu janto às 22 horas", "Eu vou dormir às 22 horas", "Eu trabalho às 22 horas"],
                "correct": "Eu vou dormir às 22 horas",
                "explanation": "'Eu vou dormir às 22 horas' signifie 'Je vais dormir à 22 heures'"
            }
        ]
    }
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