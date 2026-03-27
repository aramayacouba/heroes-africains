# 📋 PLATEFORME HÉROS AFRICAINS - DOCUMENTATION D'EXAMEN

## 🎯 1. PROBLÈME RÉSOLU

**Thème :** Plateforme numérique de valorisation des héros africains

**Problème :** Manque de ressources éducatives interactives pour valoriser les contributions des héros africains à l'histoire mondiale

**Solution :** Application web collaborative permettant de :
- 📚 Explorer les biographies de 24+ héros africains
- 🧠 Participer à des quiz interactifs en temps réel
- ➕ Contribuer en ajoutant de nouveaux héros
- 📊 Monitorer les performances via Prometheus/Grafana
- 🌐 Échanger via API REST distribuée

---no

## 🏗️ 2. ARCHITECTURE DU SYSTÈME

### Schéma Réseau

```
┌─────────────────────────────────────────────────────────────┐
│                       Utilisateurs                          │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
    HTTP/REST         WebSocket (Quiz)
        │                 │
        ▼                 ▼
    ┌──────────────────────────────┐
    │    Flask Application         │
    │    (Port 5000)               │
    │  - Routes CRUD              │
    │  - API REST                 │
    │  - SocketIO Events          │
    │  - Prometheus Metrics       │
    └──────────┬───────┬──────────┘
               │       │
        ┌──────┘       └──────┐
        │                     │
        ▼                     ▼
   ┌─────────────┐    ┌──────────────────┐
   │ PostgreSQL  │    │ Monitoring Stack │
   │ (Port 5432) │    ├──────────────────┤
   │  - Heroes   │    │ Prometheus 9090  │
   │  - Quiz     │    │ Grafana 3000     │
   │  - Scores   │    │ PgAdmin 5050     │
   └─────────────┘    └──────────────────┘
        │
  ┌─────┴─────────────┐
  │                   │
Docker Network: heroes_network (Bridge)
Subnet: 172.25.0.0/16
```

### Architecture Technique

| Composant | Technologie | Rôle | Port |
|-----------|------------|------|------|
| Frontend | HTML/Bootstrap/CSS | Interface utilisateur | 5000 |
| Backend | Flask/Python | Logique métier | 5000 |
| BD | PostgreSQL 15 | Persistance données | 5432 |
| Cache | En mémoire (Python) | Sessions quiz | - |
| Monitoring | Prometheus | Collecte métriques | 9090 |
| Dashboards | Grafana | Visualisation | 3000 |
| Gestion BD | PgAdmin | Interface BD | 5050 |

---

## 🌐 3. ASPECTS RÉSEAU

### 3.1 Communication Inter-Services

**Bridge Docker Network :**
- Isolation: Services dans réseau `heroes_network`
- DNS: Hostname-based service discovery
- Subnets: 172.25.0.0/16

**Communication :**
```
Flask ←→ PostgreSQL: TCP/5432 (driver psycopg2)
Flask ←→ Prometheus: TCP/9090 (scrape metrics)
Flask ←→ Clients: HTTP REST (5000) + WebSocket (SocketIO)
```

### 3.2 API REST Distribuée

```
GET    /api/heroes                  # Pagination: page=1&per_page=10
GET    /api/heroes/<id>             # Détail d'un héros
POST   /api/heroes                  # Création (non implémenté)
GET    /api/categories              # Lister toutes catégories
GET    /api/quiz-questions          # Questions avec pagination
GET    /api/stats                   # Statistiques globales
GET    /search?q=<query>            # Recherche tous champs
GET    /health                      # Santé application
GET    /metrics                     # Prometheus metrics
```

### 3.3 SocketIO - Communication Temps Réel

**Événements Client → Serveur :**
```javascript
socket.emit('start_quiz', {
    session_id: 'uuid',
    difficulty: 'medium|easy|hard'
});

socket.emit('submit_answer', {
    session_id: 'uuid',
    answer: 'A|B|C|D'
});

socket.emit('get_leaderboard');
socket.emit('get_session_stats', { session_id: 'uuid' });
```

**Événements Serveur → Client :**
```javascript
socket.on('quiz_started', data);       // Quiz initialisé
socket.on('next_question', data);      // Prochaine question
socket.on('answer_result', data);      // Résultat réponse
socket.on('quiz_completed', data);     // Quiz fini
socket.on('leaderboard_data', data);   # Classement top 10
socket.on('session_stats', data);      # Stats session
socket.on('quiz_error', data);         # Erreur
```

### 3.4 Monitoring Réseau

**Prometheus scrape Flask :**
```yaml
- job_name: 'flask-app'
  targets: ['web:5000']
  metrics_path: '/metrics'
  scrape_interval: 10s
```

**Métriques collectées :**
- `flask_http_requests_total` - Total requêtes HTTP
- `flask_http_request_duration_seconds` - Latence
- `flask_http_requests_total{status="5xx"}` - Erreurs serveur
- `flask_http_requests_total{status="4xx"}` - Erreurs client

---

## 🐳 4. CONTENEURISATION DOCKER

### Structure

```
heroes_africains/
├── Dockerfile              # Image multi-stage optimisée
├── docker-compose.yml      # Orchestration 5 services
├── docker/
│   ├── prometheus.yml      # Configuration monitoring
│   ├── init-db.sql        # Initialisation BD
│   ├── seed-data.sql      # Données de base
│   └── grafana/
│       ├── provisioning/   # Datasources Grafana
│       └── dashboards/     # Dashboards JSON
├── .github/
│   └── workflows/
│       └── docker-publish.yml  # CI/CD GitHub→Docker Hub
└── ...
```

### Services Docker

**1. PostgreSQL (postgres:15-alpine)**
```bash
# Health check: pg_isready
# Volumes: postgres_data (BD persistante)
# Network: heroes_network
```

**2. Flask (Dockerfile multi-stage)**
```bash
# Stage 1: Builder - Compilation dépendances
# Stage 2: Runtime - Image optimisée (400MB)
# Healthcheck: GET /health
# Non-root user (security)
```

**3. Prometheus (prom/prometheus:latest)**
```bash
# Scrape Flask /metrics toutes les 10s
# Retention: 30 jours
# Port: 9090
```

**4. Grafana (grafana/grafana:10.4.0)**
```bash
# Datasource: Prometheus
# Admin: admin/admin
# Dashboards: Héros Africains Monitoring
```

**5. PgAdmin (dpage/pgadmin4)**
```bash
# Interface graphique PostgreSQL
# Port: 5050
# Email: PGADMIN_DEFAULT_EMAIL
```

---

## ✅ 5. INSTRUCTION DE MISE EN PLACE

### Prérequis

```bash
# Installation
- Docker Desktop 3.0+
- Docker Compose 2.0+
- Git
- Terminal/PowerShell
```

### Démarrage Rapide

```bash
# 1. Cloner le dépôt
git clone https://github.com/timaguindo/heroes-africains.git
cd heroes_africains

# 2. Créer le fichier .env
cp .env.example .env

# 3. Créer les répertoires de données
mkdir -p data/{postgres,prometheus,grafana}

# 4. Lancer les services
docker-compose up -d

# 5. Vérifier l'état
docker-compose ps

# Résultat attendu:
# CONTAINER           STATUS
# heroes_db           Up (healthy)
# heroes_app          Up (healthy)
# heroes_prometheus   Up
# heroes_grafana      Up
# heroes_pgadmin      Up
```

### Accès Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Application | http://localhost:5000 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin/admin |
| PgAdmin | http://localhost:5050 | PGADMIN_EMAIL/PASSWORD |

### Arrêt

```bash
docker-compose down -v      # Down + delete volumes
docker-compose down         # Down sans supprimer données
```

---

## 🎁 6. BONUS : CI/CD GITHUB → DOCKER HUB

### Configuration GitHub Secrets

```bash
DOCKER_USERNAME     # Votre username Docker Hub
DOCKER_PASSWORD     # Votre token Docker Hub
```

### Workflow Automatique

**Sur chaque push vers main :**
1. ✅ Code checkout
2. ✅ Docker login Docker Hub
3. ✅ Build image multi-stage
4. ✅ Tag: branch, version (git tags), SHA
5. ✅ Push sur Docker Hub
6. ✅ Cache buildx pour rapidité

**Utilisation :**
```bash
# Tirer l'image
docker pull timaguindo/heroes-africains:main
docker run -p 5000:5000 timaguindo/heroes-africains:main
```

---

## 📊 7. STATISTIQUES DU PROJET

| Métrique | Valeur |
|----------|--------|
| **Héros**| 24 |
| **Catégories** | 8 |
| **Questions Quiz** | 10 |
| **Lignes de Code** | ~2500 |
| **Services Docker** | 5 |
| **Endpoints API** | 8 |
| **Événements SocketIO** | 6 |

---

## 🔒 8. SÉCURITÉ

### Bonnes Pratiques Implémentées

✅ **Docker :**
- Non-root user (UID 1000)
- Health checks
- Logging
- Secrets via .env

✅ **Flask :**
- CORS configuré
- Validation données
- Gestion erreurs
- Secret key sécurisé

✅ **BD :**
- Authentification MD5
- Isolation réseau
- Connexion chiffrée
- Backups via volumes

---

## 📝 9. CAHIER DE CHARGES EXAMEN

### Contraintes Obligatoires

| Contrainte | Implémentation | ✅ |
|-----------|----------------|---|
| Flask | Framework principal | ✅ |
| BD Docker | PostgreSQL 15 | ✅ |
| Docker | Dockerfile multi-stage | ✅ |
| Réseau Docker | Bridge heroes_network | ✅ |
| API REST | 8 endpoints | ✅ |
| Temps réel | SocketIO quiz | ✅ |
| Communication services | Flask↔DB↔Prometheus | ✅ |

### Barème (20 points)

```
1. Fonctionnement (5 pts)     ← COMPLET
2. Flask (3 pts)             ← COMPLET
3. Docker (4 pts)            ← COMPLET
4. Réseau (3 pts)            ← COMPLET
5. BD (2 pts)                ← COMPLET
6. Code (1 pt)               ← COMPLET
7. Documentation (1 pt)      ← COMPLET
8. Démo (1 pt)               ← À PRÉSENTER

BONUS :
- CI/CD GitHub→Docker Hub    ← IMPLÉMENTÉ 🎁
- Architecture pro            ← IMPLÉMENTÉE 🎁
```

---

## 🚀 10. DÉMONSTRATION EXAMEN

### Points à Montrer

1. **Application Fonctionne**
   ```bash
   curl http://localhost:5000/
   # Affiche page HTML avec 24 héros ✅
   ```

2. **Docker Services Actifs**
   ```bash
   docker-compose ps
   # 5 services UP avec health checks ✅
   ```

3. **Communication Réseau**
   ```bash
   # Flask → PostgreSQL
   curl http://localhost:5000/api/heroes
   # JSON avec données BD ✅
   
   # Prometheus collecte
   curl http://localhost:9090/api/v1/targets
   # flask-app UP ✅
   ```

4. **Quiz Temps Réel**
   ```bash
   # Ouvrir http://localhost:5000/quiz
   # Sélectionner difficulté → Démarrer
   # Répondre questions → Score en temps réel ✅
   ```

5. **Monitoring Actif**
   ```bash
   # http://localhost:3000
   # Dashboard affiche métriques Flask ✅
   ```

6. **CI/CD Configuré**
   ```bash
   # Montrer GitHub Actions
   # Dernier build avec tag Docker Hub ✅
   ```

---

## 📚 RESSOURCES

- [Flask Docs](https://flask.palletsprojects.com/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [SocketIO](https://python-socketio.readthedocs.io/)
- [Prometheus](https://prometheus.io/docs/)
- [Grafana](https://grafana.com/docs/)

---

**Fait avec ❤️ pour l'examen DEVNET**  
**L3 Réseaux et Informatique - ISI Keur Massar**