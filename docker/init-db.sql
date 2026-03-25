-- ============================================
-- INITIALISATION BASE DE DONNÉES POSTGRESQL
-- Plateforme Héros Africains
-- ============================================

-- Paramètres pour logging
SET log_statement = 'all';
SET application_name = 'heroes_db_init';

-- ============================================
-- 1. CRÉER LES EXTENSIONS
-- ============================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================
-- 2. CRÉER LES TABLES
-- ============================================

-- Table Categories
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE categories IS 'Catégories des héros africains';
COMMENT ON COLUMN categories.name IS 'Nom unique de la catégorie';
COMMENT ON COLUMN categories.icon IS 'Emoji représentant la catégorie';

-- Table Heroes
CREATE TABLE IF NOT EXISTS heroes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) UNIQUE NOT NULL,
    country VARCHAR(100) NOT NULL,
    era VARCHAR(100) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    bio TEXT NOT NULL,
    image_url VARCHAR(500),
    achievements TEXT,
    birth_year INTEGER,
    death_year INTEGER,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE heroes IS 'Héros africains et leurs biographies';
COMMENT ON COLUMN heroes.name IS 'Nom complet du héros (unique)';
COMMENT ON COLUMN heroes.bio IS 'Biographie complète';
COMMENT ON COLUMN heroes.views IS 'Nombre de consultations';

-- Table QuizQuestions
CREATE TABLE IF NOT EXISTS quiz_questions (
    id SERIAL PRIMARY KEY,
    hero_id INTEGER NOT NULL REFERENCES heroes(id) ON DELETE CASCADE,
    question VARCHAR(500) NOT NULL,
    option_a VARCHAR(200) NOT NULL,
    option_b VARCHAR(200) NOT NULL,
    option_c VARCHAR(200) NOT NULL,
    option_d VARCHAR(200) NOT NULL,
    correct_answer VARCHAR(1) NOT NULL CHECK (correct_answer IN ('A', 'B', 'C', 'D')),
    difficulty VARCHAR(20) DEFAULT 'medium' CHECK (difficulty IN ('easy', 'medium', 'hard')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE quiz_questions IS 'Questions du quiz interactif';
COMMENT ON COLUMN quiz_questions.correct_answer IS 'Bonne réponse (A, B, C ou D)';

-- Table UserQuizScores
CREATE TABLE IF NOT EXISTS user_quiz_scores (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    score INTEGER DEFAULT 0,
    total_questions INTEGER DEFAULT 0,
    percentage FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE user_quiz_scores IS 'Scores des utilisateurs au quiz';

-- ============================================
-- 3. CRÉER LES INDEX
-- ============================================

CREATE INDEX IF NOT EXISTS idx_heroes_category ON heroes(category_id);
CREATE INDEX IF NOT EXISTS idx_heroes_name ON heroes USING GIN(name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_heroes_country ON heroes(country);
CREATE INDEX IF NOT EXISTS idx_quiz_hero ON quiz_questions(hero_id);
CREATE INDEX IF NOT EXISTS idx_scores_session ON user_quiz_scores(session_id);
CREATE INDEX IF NOT EXISTS idx_scores_date ON user_quiz_scores(created_at);

-- ============================================
-- 4. CRÉER LES VUES UTILES
-- ============================================

CREATE OR REPLACE VIEW hero_stats AS
SELECT 
    h.id,
    h.name,
    h.country,
    COUNT(q.id) as quiz_count,
    COALESCE(h.views, 0) as total_views,
    c.name as category,
    h.created_at
FROM heroes h
LEFT JOIN quiz_questions q ON h.id = q.hero_id
LEFT JOIN categories c ON h.category_id = c.id
GROUP BY h.id, h.name, h.country, h.views, c.name, h.created_at
ORDER BY total_views DESC;

COMMENT ON VIEW hero_stats IS 'Vue statistique des héros';

CREATE OR REPLACE VIEW quiz_leaderboard AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY percentage DESC, score DESC) as rank,
    session_id,
    score,
    total_questions,
    ROUND(percentage, 2) as percentage,
    created_at
FROM user_quiz_scores
ORDER BY percentage DESC, score DESC, created_at DESC;

COMMENT ON VIEW quiz_leaderboard IS 'Classement des meilleurs scores du quiz';

CREATE OR REPLACE VIEW category_stats AS
SELECT 
    c.id,
    c.name,
    c.icon,
    COUNT(h.id) as hero_count,
    COUNT(DISTINCT q.id) as quiz_count
FROM categories c
LEFT JOIN heroes h ON c.id = h.category_id
LEFT JOIN quiz_questions q ON h.id = q.hero_id
GROUP BY c.id, c.name, c.icon
ORDER BY hero_count DESC;

COMMENT ON VIEW category_stats IS 'Statistiques par catégorie';

-- ============================================
-- 5. ACCORDER LES PERMISSIONS
-- ============================================

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO african_legends;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO african_legends;
GRANT SELECT ON hero_stats TO african_legends;
GRANT SELECT ON quiz_leaderboard TO african_legends;
GRANT SELECT ON category_stats TO african_legends;

-- ============================================
-- 6. LOG DE SUCCÈS
-- ============================================

\echo '════════════════════════════════════════'
\echo '✅ Base de données initialisée!'
\echo '════════════════════════════════════════'
\echo ''
\echo 'Tables créées:'
\echo '  ✓ categories'
\echo '  ✓ heroes'
\echo '  ✓ quiz_questions'
\echo '  ✓ user_quiz_scores'
\echo ''
\echo 'Vues créées:'
\echo '  ✓ hero_stats'
\echo '  ✓ quiz_leaderboard'
\echo '  ✓ category_stats'
\echo ''
\echo 'Utilisation:'
\echo '  psql -U african_legends -d heroes_db'
\echo '════════════════════════════════════════'