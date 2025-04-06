# webhook.py
import os
import json
import hmac
import hashlib
import subprocess
import threading
from flask import Flask, request
import time
import sys
from dotenv import load_dotenv

app = Flask(__name__)

# Charger les variables d'environnement
load_dotenv()

# Utiliser un secret stocké dans les variables d'environnement Replit
# et non dans le code source
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
GITHUB_REPO_OWNER = os.getenv('GITHUB_REPO_OWNER')
GITHUB_REPO_NAME = os.getenv('GITHUB_REPO_NAME')

# Variables pour gérer le bot
bot_thread = None
stop_bot_flag = threading.Event()

@app.route('/')
def home():
    return "Webhook actif - Aucune information exposée"

@app.route('/webhook', methods=['POST'])
def webhook():
    # Vérification de sécurité avec signature GitHub
    if not verify_github_signature(request):
        return "Signature non valide", 403
    
    # Vérifier l'origine du dépôt
    payload = request.json
    if not validate_repository(payload):
        return "Dépôt non autorisé", 403
    
    # Récupérer les infos du push
    branch = payload.get('ref', '').replace('refs/heads/', '')
    
    # Ne réagir qu'aux pushs sur la branche principale (généralement main ou master)
    if branch not in ['main', 'master']:
        return f"Ignorer le push sur la branche {branch}", 200
    
    print(f"Push détecté sur la branche: {branch}")
    
    try:
        # Arrêter le bot actuel
        stop_bot()
        
        # Exécuter git pull
        result = subprocess.check_output(['git', 'pull'], stderr=subprocess.STDOUT)
        pull_result = result.decode('utf-8')
        print(f"Git pull réussi: {pull_result}")
        
        # Installer les dépendances si nécessaire
        if "requirements.txt" in pull_result:
            try:
                subprocess.check_output(['pip', 'install', '-r', 'requirements.txt'], stderr=subprocess.STDOUT)
                print("Dépendances mises à jour")
            except Exception as e:
                print(f"Erreur d'installation des dépendances: {e}")
        
        # Redémarrer le bot
        start_bot()
        
        return "Mise à jour réussie", 200
    except subprocess.CalledProcessError as e:
        error_output = e.output.decode('utf-8')
        print(f"Erreur lors du git pull: {error_output}")
        
        # Redémarrer le bot même en cas d'erreur
        start_bot()
        
        return f"Erreur de mise à jour", 500

def verify_github_signature(request):
    """Vérifie la signature SHA-256 de GitHub"""
    if not WEBHOOK_SECRET:
        print("AVERTISSEMENT: WEBHOOK_SECRET non configuré")
        return False
    
    signature_header = request.headers.get('X-Hub-Signature-256')
    if not signature_header:
        return False
    
    # Format: 'sha256=SIGNATURE'
    signature = signature_header.split('=')[1]
    
    # Calculer la signature attendue
    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=request.data, digestmod=hashlib.sha256)
    expected_signature = mac.hexdigest()
    
    # Vérifier que les signatures correspondent
    return hmac.compare_digest(signature, expected_signature)

def validate_repository(payload):
    """Vérifie que le push vient du bon dépôt"""
    if not GITHUB_REPO_OWNER or not GITHUB_REPO_NAME:
        print("AVERTISSEMENT: GITHUB_REPO_OWNER ou GITHUB_REPO_NAME non configuré")
        return True  # Si non configuré, accepter tous les dépôts
    
    repo = payload.get('repository', {})
    owner = repo.get('owner', {}).get('name')
    name = repo.get('name')
    
    return owner == GITHUB_REPO_OWNER and name == GITHUB_REPO_NAME

def run_bot():
    """Exécute le bot dans un processus séparé"""
    global stop_bot_flag
    stop_bot_flag.clear()
    
    print("Démarrage du bot...")
    
    try:
        # Exécuter le bot principal comme sous-processus
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
    """Démarre le bot dans un thread séparé"""
    global bot_thread, stop_bot_flag
    
    # Arrêter l'instance précédente si elle existe
    stop_bot()
    
    # Démarrer une nouvelle instance
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("Bot démarré dans un nouveau thread")

def stop_bot():
    """Arrête le bot s'il est en cours d'exécution"""
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