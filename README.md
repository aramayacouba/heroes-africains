# 🌍 Plateforme Héros Africains - Projet DEVNET

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.3-white)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/docker-latest-blue)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15-336791)](https://www.postgresql.org/)

**Plateforme web éducative distribuée pour découvrir l'histoire des héros africains** | L3 Réseaux & Informatique - ISI Keur Massar

---

## 📋 Table des Matières

| Section | Lien |
|---------|------|
| 🎯 Vue d'Ensemble | [Voir](#vue-densemble) |
| 🚀 Démarrage | [Voir](#démarrage-rapide) |
| 🏗️ Architecture | [Voir](#architecture) |
| 🐳 Docker | [Voir](#docker--conteneurisation) |
| 📊 Monitoring | [Voir](#monitoring) |
| 📚 Documentation | [Voir](#documentation-complète) |

---

## 🎯 Vue d'Ensemble

### Problème & Solution

| Aspect | Détail |
|--------|--------|
| **Problème** | Manque de ressources éducatives interactives pour valoriser les héros africains |
| **Solution** | Plateforme collaborative avec 24+ héros, quiz temps réel, API REST distribuée |
| **Impact** | ✅ 100% responsive • ✅ Quiz multiplayer • ✅ Monitoring en temps réel |

### Objectifs Atteints

✅ **Valoriser** les héros africains avec biographies complètes  
✅ **Éduquer** via quiz interactifs (solo & duo)  
✅ **Intégrer** technologies modernes (Flask, Docker, WebSocket, Prometheus)  
✅ **Démontrer** architecture distribuée avec orchestration Docker  
✅ **Monitorer** performances en temps réel

### Statistiques

24+ Héros | 8 Catégories | 70+ questions | 6 Services Docker


---

## 🚀 Démarrage Rapide

### Installation (3 minutes)

```bash
# 1️⃣ Cloner
git clone https://github.com/aramayacouba/heroes-africains.git
cd heroes_africains

# 2️⃣ Lancer
docker-compose up -d

# 3️⃣ Accéder
# Web: http://localhost:5000
# Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090

Arrêter

    docker-compose down -v  # Tout supprimer

🏗️ Architecture


Diagramme Réseau
┌─── Utilisateurs ────────────────────────┐
│   HTTP/REST + WebSocket (SocketIO)     │
└─────────────────┬──────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐   ┌────────┐   ┌──────────┐
│Web UI  │   │API     │   │WebSocket │
│(Flask) │   │(REST)  │   │(SocketIO)│
└────┬───┘   └───┬────┘   └────┬─────┘
     │          │              │
     └──────────┼──────────────┘
                │
     ┌──────────▼──────────┐
     │  Docker Network     │
     │  heroes_network     │
     └──────────┬──────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
┌────────┐ ┌──────────┐ ┌─────────┐
│PosgSQL │ │Prometheus│ │ Grafana │
│(5432)  │ │(9090)    │ │(3000)   │
└────────┘ └──────────┘ └─────────┘

Technique de la pile

      Couche	Tech	Rôle
      Frontend	Bootstrap 5 + CSS3 + JS	Réactivité à l’interface
      Backend	Flask 2.3 (Python 3.11)	API REST + Logique métier
      Temps Réel	Flask-SocketIO	WebSocket pour quiz en direct
      BD	PostgreSQL 15	Persistance distribuée
      Surveillance	Prométhée + Grafana	Métriques & tableaux de bord
      Orchestration	Docker + Composer	6 services orchestrés
  
📋 Structure

      heroes_africains/
      │
      ├── 📁 app/                          # Code source Flask
      │   ├── __init__.py                  # Initialisation et factory Flask
      │   ├── models.py                    # Modèles SQLAlchemy
      │   ├── routes.py                    # Routes HTTP principales
      │   ├── api.py                       # Endpoints API REST
      │   ├── socketio_events.py           # Événements WebSocket
      │   │
      │   ├── 📁 templates/                # Templates HTML Jinja2
      │   │   ├── base.html                # Template de base (navbar, footer)
      │   │   ├── index.html               # Page d'accueil
      │   │   ├── hero_detail.html         # Page détail d'un héros
      │   │   ├── category.html            # Listing par catégorie
      │   │   ├── add_hero.html            # Formulaire d'ajout
      │   │   └── quiz.html                # Interface interactive du quiz
      │   │
      │   └── 📁 static/                   # Ressources statiques
      │       ├── 📁 css/
      │       │   └── style.css            # Styles CSS personnalisés
      │       ├── 📁 js/
      │       │   ├── script.js            # JavaScript global
      │       │   └── quiz.js              # Logique du quiz
      │       ├── 📁 images/
      │       │   └── heroes/              # Images des héros
      │       └── 📁 fonts/                # Polices custom
      │
      ├── 📁 docker/                       # Configuration Docker
      │   ├── init-db.sql                  # Script d'initialisation BD
      │   ├── pgadmin_servers.json         # Configuration PgAdmin
      │   ├── prometheus.yml               # Configuration Prometheus
      │   │
      │   └── 📁 grafana/
      │       ├── 📁 provisioning/
      │       │   ├── datasources/
      │       │   │   └── prometheus.yml   # Datasource Prometheus
      │       │   └── dashboards/
      │       │       ├── dashboards.yml   # Configuration dashboards
      │       │       └── heroes.json      # Dashboard monitoring
      │       │
      │       └── 📁 dashboards/           # Dashboards JSON
      │
      ├── 📄 config.py                     # Configuration (DB, environnement)
      ├── 📄 run.py                        # Point d'entrée application
      ├── 📄 requirements.txt              # Dépendances Python
      ├── 📄 Dockerfile                    # Image Flask multi-stage
      ├── 📄 docker-compose.yml            # Orchestration services
      ├── 📄 .dockerignore                 # Fichiers à ignorer dans Docker
      ├── 📄 .env                          # Variables d'environnement (⚠️ GIT IGNORED)
      ├── 📄 .env.example                  # Exemple de .env
      ├── 📄 .gitignore                    # Fichiers à ignorer dans Git
      │
      ├── 📄 README.md                     # Cette documentation
      ├── 📄 DEMO.md                       # Guide de démonstration
      ├── 📄 LICENSE                       # Licence MIT
      │
      └── 📁 .github/
          └── 📁 workflows/
              └── docker-publish.yml       # CI/CD GitHub Actions

🗄️ Données

Modèle ER

CATEGORIES (8) ←── HEROES (24+) ←── QUIZ_QUESTIONS (70+)
                                     ↓
                              USER_QUIZ_SCORES

Tables Principales

 -- Categories (8 enregistrements)
CREATE TABLE categories (id, name, icon, created_at);

-- Heroes (24+)
CREATE TABLE heroes (id, name, country, category_id, bio, views, ...);

-- Quiz (70+ questions)
CREATE TABLE quiz_questions (id, hero_id, question, options A-D, difficulty);

-- Scores (dynamique)
CREATE TABLE user_quiz_scores (id, session_id, score, percentage, ...);

🌐 API REST

   Points de terminaison (8+)

GET    /api/heroes              # Lister héros (pagination)
GET    /api/hero/<id>           # Détail
PUT    /api/hero/<id>           # Modifier
DELETE /api/hero/<id>           # Supprimer
GET    /api/categories          # Catégories
GET    /api/quiz-questions      # Questions
GET    /api/stats               # Statistiques
GET    /search?q=               # Recherche

Exemple
    curl http://localhost:5000/api/heroes?page=1&per_page=10

⚡ WebSocket & Temps Réel

    Quiz Solo
Client: start_quiz(difficulty)
Server: quiz_started(question)
Client: submit_answer(A)
Server: answer_result(correct) + next_question
...
Server: quiz_completed(score)

Quiz Duo
      Joueur 1: create_duo_game() → Code ABC
      Joueur 2: join_duo_game(ABC)
      Both: Questions synchronisées
      Server: Leaderboard en direct


📊 Surveillance

    Prométhée (http://localhost:9090)
    Métriques collectées :
flask_http_requests_total          # Total requêtes
flask_http_request_duration_seconds # Latence (ms)
flask_http_requests_total{status}   # Par statut (2xx/4xx/5xx)

Grafana (http://localhost:3000)
Tableau de bord « Plateforme Héros Africains » :

📊 Totaux HTTP des requêtes (graphique circulaire)
⏱️ Temps de réponse moyen (stat)
📈 Taux de requêtes (séries temporelles)
❌ Erreurs 4xx (stat)
⚠️ Erreurs 5xx (stat)
✅ Requêtes 200 (stat)


🐳 Docker & Conteneurisation
  Services
  
    Service	Image	Port	Rôle
Web	Python 3.11	5000	Application Flask
db	PostgreSQL 15	5432	Base de données
Prométhée	Prométhée	9090	Collecte métriques
Grafana	Grafana 10.4	3000	Tableaux de bord
PGADMIN	PgAdmin 4	5050	Gestion BD
Postgres-exportateur	Exportateur	9187	Métriques PG

Réseau Docker

Network: heroes_network (bridge)
Subnet: 172.25.0.0/16

Services connectés:
├─ web ←→ db (psql/5432)
├─ prometheus ← web (/metrics)
├─ grafana ← prometheus (datasource)
└─ pgadmin ← db (gestion)

Volumes Persistants

postgres_data      # BD (chiffrée)
prometheus_data    # Métriques (30j rétention)
grafana_data       # Configuration
pgadmin_data       # Configuration

Commandes Essentielles

docker-compose up -d          # Démarrer
docker-compose ps             # État
docker-compose logs -f web    # Logs temps réel
docker-compose down -v        # Arrêter + supprimer
docker-compose exec web bash  # Shell

🎮 Fonctionnalités

1️⃣ Exploration des Héros
✅ Grille responsive (1/2/3-4 colonnes)
✅ Recherche multi-champs
✅ Filtrage par catégorie
✅ Tri par popularité
✅ Biographie complète + années

2️⃣ Quiz Interactif
Mode Solo :

3 niveaux (Facile 5Q, Moyen 8Q, Difficile 10Q)
Retour immédiat
Barre de progression
Scores de sauvegarde
Duo de modes :

Code court pour rejoindre
5 questions synchronisées
Classement en direct
Podium avec médailles 🥇🥈🥉
3️⃣ Contribution
✅ Formulaire d’ajout de héros
✅ Validation server
✅ Images via URL
✅ Biographie + réalisations

4️⃣ Tableau de Bord
✅ Statistiques globales
✅ Top 5 héros
✅ Compteurs animés

🔐 Configuration & Sécurité

   Variables d’Environnement (.env)
# FLASK
FLASK_APP=run.py
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<secret>

# DATABASE
POSTGRES_USER=african_legends
POSTGRES_PASSWORD=<password>
POSTGRES_DB=heroes_db
DATABASE_URL=postgresql://...

# GRAFANA
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=<password>

# APP
CORS_ORIGINS=*

Bonnes Pratiques
✅ Secrets en .env (non versionné)
✅ Non-root user (UID 1000)
✅ Healthchecks activés
✅ Validation côté server
✅ Isolation réseau Docker


📝 Développement local

# 1. Cloner
git clone https://github.com/aramayacouba/heroes-africains.git

# 2. Env virtuel
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate (Windows)

# 3. Dépendances
pip install -r requirements.txt

# 4. BD locale
docker run -d --name heroes_db -e POSTGRES_USER=african_legends \
  -e POSTGRES_PASSWORD=passer123 -e POSTGRES_DB=heroes_db \
  -p 5432:5432 postgres:15-alpine

# 5. Lancer
export FLASK_ENV=development
python run.py

📚 Documentation complète

API REST
Exemples :

      # Lister héros
curl http://localhost:5000/api/heroes?page=1&per_page=10

# Détail héros
curl http://localhost:5000/api/hero/1

# Catégories
curl http://localhost:5000/api/categories

# Statistiques
curl http://localhost:5000/api/stats

# Recherche
curl http://localhost:5000/search?q=mandela

WebSocket

const socket = io({
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionAttempts: 5
});

// Solo
socket.emit('start_quiz', {session_id, difficulty});

// Duo
socket.emit('create_duo_game', {difficulty, player_name});
socket.emit('join_duo_game', {game_id, player_name});

📞 Soutien

Canal	Contact
📧 Email	yacoubaarama12@gmail.com
🐙 Problèmes sur GitHub	Ouvrir, numéro
💬 Discussions	Discussions

👨 💻 Auteur

aramayacouba (Arama Yacouba)

🐙 GitHub : @aramayacouba
🐳 Docker Hub : @arama01
📧 Email : yacoubaarama12@gmail.com

📊 Statistiques Finales

🐍 Python 3.11      📦 Flask 2.3         🗄️ PostgreSQL 15
🐳 Docker Compose   📈 Prometheus+Grafana ⚡ Flask-SocketIO

🦸 24+ Héros        📂 8 Catégories       ❓ 70+ Questions
🔌 8+ Endpoints     📡 10+ Événements     🐳 6 Services Docker

⏱️ < 1 min démarrage  📦 496 MB image      📝 ~3000 lignes code

<div align="center">
🎉 Fait avec ❤️ pour valoriser l’histoire africaine

« L’Afrique n’a pas besoin de savants, elle a besoin de croire en ses fils. » — Frantz Fanon

🌍 🦸‍♂️ 🎓 💡 🚀

Valoriser | Éduquer | Inspirer | Innover | Réussir

Version 1.0.0 | Dernière mise à jour le 26-03-2026 | Licence MIT | Statut ✅ actif

# Test CI/CD - 30/03/2026

</div> ```