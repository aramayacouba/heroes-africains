import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from prometheus_flask_exporter import PrometheusMetrics
from config import config
import time

# UNE SEULE instance db
db = SQLAlchemy()
socketio = SocketIO()

def create_app(config_name=None):
    """Factory pour créer l'application Flask"""
    
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    print(f"🔧 Initialisation de l'app en mode: {config_name}")
    
    # Créer l'app Flask
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # ✅ CONFIGURATION SOCKETIO - TRÈS IMPORTANT
    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode='threading',
        logger=True,
        engineio_logger=True,
        ping_timeout=60,
        ping_interval=25,
        max_http_buffer_size=1e6,
        allow_upgrades=True,
        transports=['websocket', 'polling']
    )
    
    print("✅ SocketIO configuré")
    
    # Initialiser les extensions
    db.init_app(app)
    metrics = PrometheusMetrics(app)
    
    # Initialiser les modèles
    from app.models import init_models
    Category, Hero, QuizQuestion, UserQuizScore = init_models(db)
    
    # Créer le contexte de l'app
    with app.app_context():
        # Créer les tables
        max_retries = 10
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                print(f"⏳ Tentative de connexion à la BD... ({retry_count + 1}/{max_retries})")
                print(f"   📍 URL: {os.getenv('DATABASE_URL')}")
                db.create_all()
                print("✅ BD initialisée avec succès!")
                break
            except Exception as e:
                print(f"❌ Erreur connexion BD: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    time.sleep(2)
                else:
                    print("❌ Impossible de se connecter à la BD après plusieurs tentatives")
                    raise
        
        # Initialiser seulement les catégories
        _init_default_categories(Category)
    
    # Enregistrer les routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # ✅ ENREGISTRER SOCKETIO APRÈS INITIALISATION DES MODÈLES
    print("🔌 Enregistrement des événements SocketIO...")
    from app.socketio_events import register_socketio_events
    register_socketio_events(socketio, db)
    print("✅ SocketIO prêt")
    
    # Enregistrer l'API
    from flask_restful import Api
    api = Api(app)
    from app.api import HeroesList, HeroDetail, CategoriesList, QuizQuestionsList
    
    api.add_resource(HeroesList, '/api/heroes')
    api.add_resource(HeroDetail, '/api/hero/<int:hero_id>')
    api.add_resource(CategoriesList, '/api/categories')
    api.add_resource(QuizQuestionsList, '/api/quiz-questions')
    
    # 🔥 Exporter les modèles globalement
    import app.models as models_module
    models_module.Category = Category
    models_module.Hero = Hero
    models_module.QuizQuestion = QuizQuestion
    models_module.UserQuizScore = UserQuizScore
    
    # ✅ TEST DE CONNEXION SOCKETIO
    @app.route('/socketio-test')
    def socketio_test():
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test SocketIO</title>
        </head>
        <body>
            <h1>Test SocketIO</h1>
            <div id="status">En attente...</div>
            <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
            <script>
                const socket = io();
                
                socket.on('connect', function() {
                    document.getElementById('status').innerHTML = '✅ SocketIO CONNECTÉ!';
                    document.getElementById('status').style.color = 'green';
                });
                
                socket.on('disconnect', function() {
                    document.getElementById('status').innerHTML = '❌ SocketIO DÉCONNECTÉ';
                    document.getElementById('status').style.color = 'red';
                });
                
                socket.on('connect_error', function(error) {
                    document.getElementById('status').innerHTML = '❌ Erreur: ' + error;
                    document.getElementById('status').style.color = 'red';
                });
            </script>
        </body>
        </html>
        '''
    
    return app

def _init_default_categories(Category):
    """Initialiser SEULEMENT les 8 catégories"""
    
    if Category.query.first() is not None:
        print("✅ Catégories déjà existantes")
        return
    
    print("🔄 Initialisation des 8 catégories...")
    
    categories_data = [
        {
            'name': 'Indépendance & Politique',
            'description': 'Révolutionnaires et leaders qui ont libéré l\'Afrique du colonialisme',
            'icon': '🗽'
        },
        {
            'name': 'Littérature & Culture',
            'description': 'Écrivains, poètes et artistes qui ont enrichi la culture africaine',
            'icon': '📚'
        },
        {
            'name': 'Sciences & Technologie',
            'description': 'Scientifiques, innovateurs et penseurs africains',
            'icon': '🔬'
        },
        {
            'name': 'Militaire & Résistance',
            'description': 'Généraux et stratèges qui ont défendu l\'Afrique',
            'icon': '⚔️'
        },
        {
            'name': 'Éducation & Philosophie',
            'description': 'Éducateurs et penseurs qui ont transformé la conscience africaine',
            'icon': '🎓'
        },
        {
            'name': 'Droits Humains & Paix',
            'description': 'Défenseurs des droits, justice et paix en Afrique',
            'icon': '✊'
        },
        {
            'name': 'Commerce & Entrepreneuriat',
            'description': 'Commerçants et entrepreneurs qui ont bâti des empires',
            'icon': '💼'
        },
        {
            'name': 'Spiritualité & Sagesse',
            'description': 'Guides spirituels et sages africains',
            'icon': '🙏'
        }
    ]
    
    for cat_data in categories_data:
        cat = Category(**cat_data)
        db.session.add(cat)
    
    db.session.commit()
    print(f"✅ {len(categories_data)} catégories créées")
    print("🎉 BD prête! Zéro héros - À vous de les ajouter manuellement!")