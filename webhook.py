# webhook.py
import os
import json
import subprocess
import threading
from flask import Flask, request

# Import vos modules de bot pour pouvoir le redémarrer
import telebot
import time
import signal
import sys
from dotenv import load_dotenv

app = Flask(__name__)


# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# Variables pour gérer le bot
bot_thread = None
bot_process = None
stop_bot_flag = threading.Event()

@app.route('/')
def home():
    return "Webhook pour l'auto-déploiement du bot Telegram d'apprentissage du portugais actif!"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Vérifiez la clé secrète si vous en utilisez une
    if SECRET_KEY and request.args.get('key') != SECRET_KEY:
        return "Clé non autorisée", 403
        
    # Vérifiez que c'est bien un événement push de GitHub
    if request.headers.get('X-GitHub-Event') == 'push':
        # Récupérer les données JSON du webhook
        data = request.json
        
        # Vous pouvez logger les infos du push
        print(f"Nouveau push détecté sur la branche: {data.get('ref', 'unknown')}")
        print(f"Mise à jour par: {data.get('pusher', {}).get('name', 'unknown')}")
        
        try:
            # Arrêter le bot actuel si en cours d'exécution
            stop_bot()
            
            # Exécuter git pull pour mettre à jour le code
            result = subprocess.check_output(['git', 'pull'], stderr=subprocess.STDOUT)
            pull_result = result.decode('utf-8')
            print(f"Git pull réussi: {pull_result}")
            
            # Installer éventuellement les nouvelles dépendances
            if "portuguese_courses.py" in pull_result or "requirements.txt" in pull_result:
                try:
                    subprocess.check_output(['pip', 'install', '-r', 'requirements.txt'], stderr=subprocess.STDOUT)
                    print("Dépendances mises à jour")
                except:
                    print("Pas de fichier requirements.txt ou erreur d'installation")
            
            # Redémarrer le bot après la mise à jour
            start_bot()
            
            return f"Mise à jour réussie! Bot redémarré.\n{pull_result}", 200
        except subprocess.CalledProcessError as e:
            error_output = e.output.decode('utf-8')
            print(f"Erreur lors du git pull: {error_output}")
            
            # Redémarrer le bot même en cas d'erreur
            start_bot()
            
            return f"Erreur de mise à jour: {error_output}", 500
    
    return "Événement ignoré", 200

def run_bot():
    global stop_bot_flag
    stop_bot_flag.clear()
    
    print("Démarrage du bot...")
    
    # Importation du script du bot
    try:
        # On exécute le bot principal comme sous-processus
        bot_proc = subprocess.Popen([sys.executable, 'main.py'])
        
        # Attendre que le flag d'arrêt soit défini ou que le processus se termine
        while not stop_bot_flag.is_set() and bot_proc.poll() is None:
            time.sleep(1)
        
        # Tuer le processus s'il est encore en cours d'exécution
        if bot_proc.poll() is None:
            bot_proc.terminate()
            try:
                bot_proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                bot_proc.kill()
    except Exception as e:
        print(f"Erreur lors de l'exécution du bot: {e}")

def start_bot():
    global bot_thread, stop_bot_flag
    
    # Arrêter l'instance précédente si elle existe
    stop_bot()
    
    # Démarrer une nouvelle instance du bot dans un thread séparé
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("Bot redémarré dans un nouveau thread")

def stop_bot():
    global bot_thread, stop_bot_flag
    
    if bot_thread and bot_thread.is_alive():
        print("Arrêt du bot en cours...")
        stop_bot_flag.set()
        bot_thread.join(timeout=10)
        print("Bot arrêté")

if __name__ == '__main__':
    # Démarrer le bot initialement
    start_bot()
    
    # Démarrer le serveur Flask
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)