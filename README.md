# 🌍 Plateforme Numérique de Valorisation des Héros Africains

Une application web éducative moderne pour découvrir, apprendre et partager l'histoire des grands héros africains.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Flask](https://img.shields.io/badge/flask-2.3-white)
![Docker](https://img.shields.io/badge/docker-latest-blue)

## 🎯 Objectif du Projet

Cette plateforme vise à :
- ✅ Valoriser les contributions des héros africains à l'histoire mondiale
- ✅ Fournir une ressource éducative interactive et attrayante
- ✅ Intégrer des technologies modernes (Flask, Docker, WebSockets, Monitoring)
- ✅ Démontrer l'utilisation de réseaux Docker pour la communication inter-services
- ✅ Mettre en œuvre un système de monitoring en temps réel

## 🏗️ Architecture du Système

```
┌─────────────────────────────────────────────────────────────┐
│                    Utilisateurs Finaux                      │
└────────────────────────┬────────────────────────────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌────────┐       ┌────────┐      ┌─────────┐
   │ Web UI │       │ API    │      │ WebSocket│
   │(Flask) │◄─────►│(REST)  │      │(SocketIO)│
   └────────┘       └────────┘      └─────────┘
        │                │                │
        └────────────────┼────────────────┘
                         │
          ┌──────────────▼──────────────┐
          │   Docker Network Bridge     │
          └──────────────┬──────────────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
     ┌─────────┐    ┌──────────┐   ┌──────────┐
     │PostgreSQL│    │Prometheus│   │ Grafana  │
     │Database  │    │Metrics   │   │Dashboard │
     └─────────┘    └──────────┘   └──────────┘
```

## 🚀 Démarrage Rapide

### Prérequis

- Docker Desktop (3.0+)
- Python 3.9+ (pour développement local)
- Git
- VS Code (recommandé)

### Installation et Lancement

#### 1️⃣ Cloner le Dépôt
```bash
git clone https://github.com/pjdevnet/devnet-projet.git
cd heroes_africains
```

#### 2️⃣ Lancer avec Docker Compose
```bash
docker-compose up --build
```

#### 3️⃣ Accéder à l'Application
- **Application Web**: http://localhost:5000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (Admin: admin/admin)

#### 4️⃣ Arrêter les Conteneurs
```bash
docker-compose down
```

## 📊 Structure du Projet

```
heroes_africains/
├── app/
│   ├── __init__.py              # Initialisation Flask & extensions
│   ├── models.py                # Modèles SQLAlchemy (Hero, Category, Quiz)
│   ├── routes.py                # Routes principales
│   ├── api.py                   # Endpoints API REST
│   ├── socketio_events.py       # Événements WebSocket temps réel
│   ├── templates/               # Templates HTML Jinja2
│   │   ├── base.html            # Template de base
│   │   ├── index.html           # Page d'accueil
│   │   ├── hero_detail.html     # Détail d'un héros
│   │   ├── category.html        # Listing par catégorie
│   │   ├── add_hero.html        # Formulaire ajout héros
│   │   └── quiz.html            # Page interactive du quiz
│   └── static/                  # Ressources statiques
│       ├── css/
│       │   └── style.css        # Styles CSS personnalisés
│       ├── js/
│       │   ├── script.js        # JS global
│       │   └── quiz.js          # Logique du quiz
│       └── images/              # Images
│
├── docker/
│   ├── Dockerfile               # Image Flask
│   ├── prometheus.yml           # Configuration Prometheus
│   └── grafana/
│       └── provisioning/        # Configuration Grafana
│
├── config.py                    # Configuration (DB, environment)
├── run.py                       # Point d'entrée application
├── requirements.txt             # Dépendances Python
├── docker-compose.yml           # Orchestration services
└── README.md                    # Cette documentation
```

## 🗄️ Modèles de Données

### Hero (Héros)
```python
- id: Integer (PK)
- name: String(150) - Nom unique
- country: String(100)
- era: String(100)
- category_id: Integer (FK)
- bio: Text - Biographie complète
- image_url: String
- achievements: Text
- birth_year: Integer
- death_year: Integer
- views: Integer
- created_at: DateTime
```

### Category (Catégories)
```python
- id: Integer (PK)
- name: String(100)
- description: Text
- icon: String (emoji)
- created_at: DateTime
- heroes: Relationship
```

### QuizQuestion
```python
- id: Integer (PK)
- hero_id: Integer (FK)
- question: String(500)
- option_a, b, c, d: String
- correct_answer: String (A/B/C/D)
- difficulty: String (easy/medium/hard)
```

### UserQuizScore
```python
- id: Integer (PK)
- session_id: String (unique)
- score: Integer
- total_questions: Integer
- percentage: Float
- created_at: DateTime
```

## 🌐 API REST Endpoints

### Héros
```
GET    /api/heroes                    # Lister tous les héros (paginátion)
GET    /api/hero/<id>                # Détail d'un héros
PUT    /api/hero/<id>                # Modifier un héros
DELETE /api/hero/<id>                # Supprimer un héros
```

### Catégories
```
GET    /api/categories               # Lister les catégories
```

### Quiz
```
GET    /api/quiz-questions           # Lister les questions (pagination)
```

### Statistiques
```
GET    /api/stats                    # Statistiques globales
```

### Recherche
```
GET    /search?q=<query>             # Recherche tous les champs
```

## ⚡ Événements WebSocket (SocketIO)

### Côté Client
```javascript
// Démarrer un quiz
socket.emit('start_quiz', {
    session_id: 'uuid',
    difficulty: 'medium'
});

// Soumettre une réponse
socket.emit('submit_answer', {
    session_id: 'uuid',
    answer: 'A'
});

// Obtenir le classement
socket.emit('get_leaderboard');
```

### Côté Serveur
```javascript
// Quiz démarré
socket.on('quiz_started', data => { ... });

// Prochaine question
socket.on('next_question', data => { ... });

// Résultat de la réponse
socket.on('answer_result', data => { ... });

// Quiz complété
socket.on('quiz_completed', data => { ... });

// Données du classement
socket.on('leaderboard_data', data => { ... });
```

## 📊 Monitoring avec Prometheus & Grafana

### Métriques Collectées
- Nombre total de requêtes HTTP
- Temps de réponse moyen
- Taux d'erreurs (4xx, 5xx)
- Activité SocketIO en temps réel
- Latence des requêtes à la base de données
- Nombre de connexions actives

### Accès Grafana
1. Aller sur http://localhost:3000
2. Login: `admin` / Mot de passe: `admin`
3. Importer le dashboard depuis Prometheus

### URLs Utiles
- Prometheus: http://localhost:9090
- Metrics Flask: http://localhost:5000/metrics
- Grafana: http://localhost:3000

## 🎓 Fonctionnalités Principales

### 1. 📚 Exploration des Héros
- Affichage en grille responsive
- Recherche par nom, pays, époque
- Filtrage par catégorie
- Tri par popularité
- Vue détaillée avec biographie complète

### 2. 🧠 Quiz Interactif
- Questions en temps réel (WebSocket)
- 3 niveaux de difficulté
- Feedback immédiat
- Classement en direct
- Statistiques personnelles

### 3. ➕ Contribution Communautaire
- Formulaire d'ajout de héros
- Validation côté client/serveur
- Images via URL
- Catégorisation flexible

### 4. 🔍 Recherche Globale
- Recherche sur tous les champs
- Résultats en temps réel
- Suggestion automatique

### 5. 📊 Tableau de Bord
- Vue d'ensemble globale
- Statistiques en temps réel
- Top héros consultés
- Monitoring du système

## 🎨 Design & UX

### Caractéristiques du Design
- ✨ Interface moderne et élégante
- 🎨 Palette de couleurs harmonieuse (Or, Noir, Blanc)
- 📱 Responsive Design (Mobile, Tablet, Desktop)
- ⚡ Animations fluides et transitions douces
- ♿ Accessibilité optimale
- 🌙 Support du mode sombre (optionnel)

### Typographie
- **Títulos**: Playfair Display (serif élégante)
- **Texte**: Poppins (sans-serif moderne)
- Hiérarchie visuelle claire

### Couleurs Principales
```
- Primaire: #FFD700 (Or)
- Secondaire: #1a1a1a (Noir)
- Accent: #FF6B35 (Orange)
- Succès: #06A77D (Vert)
- Info: #0066CC (Bleu)
- Erreur: #E63946 (Rouge)
```

## 🐳 Docker & Orchestration

### Services
1. **web**: Application Flask (port 5000)
2. **db**: PostgreSQL (port 5432)
3. **prometheus**: Monitoring (port 9090)
4. **grafana**: Dashboards (port 3000)

### Réseau Docker
- Bridge network: `heroes_network`
- Isolation et communication sécurisée

### Volumes
- `postgres_data`: Persistance BD
- `prometheus_data`: Métriques stockées
- `grafana_data`: Configuration Grafana

## 🔐 Configuration & Sécurité

### Variables d'Environnement
```env
FLASK_ENV=production
DATABASE_URL=postgresql://heroes_user:heroes_pass@db:5432/heroes_db
SECRET_KEY=your-secret-key-change-this
```

### Bonnes Pratiques
- ✅ Variables sensibles en `.env`
- ✅ Isolation des services en réseau Docker
- ✅ Healthchecks pour la BD
- ✅ Validation des données
- ✅ Gestion des erreurs cohérente

## 🚀 CI/CD avec GitHub Actions

(Voir la section déploiement)

## 📝 Développement Local

### Installation d'Environnement
```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Lancer en Mode Développement
```bash
export FLASK_ENV=development
python run.py
```

## 🤝 Contribution

Les contributions sont bienvenues! Pour contribuer:

1. Fork le dépôt
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Commit vos changements (`git commit -m 'Add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier `LICENSE`

## 👤 Auteur

**PJDevNet**
- GitHub: [@pjdevnet](https://github.com/pjdevnet)

## 🙏 Remerciements

- Gratitude à tous les héros africains qui ont inspiré ce projet
- Merci à la communauté Flask et Docker
- Inspiration des meilleurs projets éducatifs mondiaux

## 📞 Support

Pour toute question ou problème:
- 📧 Email: contact@pjdevnet.com
- 🐙 GitHub Issues: [Issues](https://github.com/pjdevnet/devnet-projet/issues)

## 🔗 Ressources Utiles

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)

## 📊 Statistiques du Projet

- 🐍 **Langage**: Python 3.11
- 📦 **Framework**: Flask 2.3
- 🗄️ **BD**: PostgreSQL 15
- 🐳 **Conteneurisation**: Docker + Docker Compose
- 📈 **Monitoring**: Prometheus + Grafana
- ⚡ **Temps Réel**: Flask-SocketIO
- 🎨 **Frontend**: Bootstrap 5 + CSS3

---

**Fait avec ❤️ pour l'Afrique et son histoire**