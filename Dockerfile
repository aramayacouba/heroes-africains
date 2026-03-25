# ============================================
# DOCKERFILE - PLATEFORME HÉROS AFRICAINS
# Multi-étape pour optimisation
# ============================================

# 🔵 ÉTAPE 1: Construction et dépendances
FROM python:3.11-slim as builder

LABEL maintainer="DevNet Team"
LABEL description="Plateforme Héros Africains - Backend Flask"
LABEL version="1.0.0"

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 🟢 ÉTAPE 2: Image de production légère
FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances runtime uniquement
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier les dépendances Python du builder
COPY --from=builder /root/.local /root/.local

# Définir le PATH
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Copier le code source
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p /app/logs /app/tmp

# Exposer le port
EXPOSE 5000

# Vérifications de santé (healthcheck)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# 🎯 Commande de démarrage
CMD ["python", "run.py"]