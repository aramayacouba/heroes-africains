from datetime import datetime

# Variables globales pour les modèles
Category = None
Hero = None
QuizQuestion = None
UserQuizScore = None

def init_models(db):
    """Initialiser les modèles SQLAlchemy - APPELÉ UNE SEULE FOIS"""
    
    global Category, Hero, QuizQuestion, UserQuizScore
    
    # Vérifier si déjà initialisés
    if Category is not None:
        return Category, Hero, QuizQuestion, UserQuizScore
    
    class Category(db.Model):
        """Modèle pour les catégories de héros"""
        __tablename__ = 'categories'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True, nullable=False)
        description = db.Column(db.Text)
        icon = db.Column(db.String(255))
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        heroes = db.relationship('Hero', backref='category', lazy=True, cascade='all, delete-orphan')
        
        def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'icon': self.icon,
                'heroes_count': len(self.heroes)
            }
        
        def __repr__(self):
            return f'<Category {self.name}>'
    
    class Hero(db.Model):
        """Modèle pour les héros africains"""
        __tablename__ = 'heroes'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(150), nullable=False, unique=True)
        country = db.Column(db.String(100), nullable=False)
        era = db.Column(db.String(100), nullable=False)
        category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
        bio = db.Column(db.Text, nullable=False)
        image_url = db.Column(db.String(500))
        achievements = db.Column(db.Text)
        birth_year = db.Column(db.Integer)
        death_year = db.Column(db.Integer)
        views = db.Column(db.Integer, default=0)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
        
        def to_dict(self):
            return {
                'id': self.id,
                'name': self.name,
                'country': self.country,
                'era': self.era,
                'category': self.category.name if self.category else None,
                'bio': self.bio,
                'image_url': self.image_url,
                'achievements': self.achievements,
                'birth_year': self.birth_year,
                'death_year': self.death_year,
                'views': self.views,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
        
        def __repr__(self):
            return f'<Hero {self.name}>'
    
    class QuizQuestion(db.Model):
        """Modèle pour les questions de quiz"""
        __tablename__ = 'quiz_questions'
        
        id = db.Column(db.Integer, primary_key=True)
        hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
        question = db.Column(db.String(500), nullable=False)
        option_a = db.Column(db.String(200), nullable=False)
        option_b = db.Column(db.String(200), nullable=False)
        option_c = db.Column(db.String(200), nullable=False)
        option_d = db.Column(db.String(200), nullable=False)
        correct_answer = db.Column(db.String(1), nullable=False)
        difficulty = db.Column(db.String(20), default='medium')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        hero = db.relationship('Hero', backref='quiz_questions')
        
        def to_dict(self):
            return {
                'id': self.id,
                'hero_id': self.hero_id,
                'hero_name': self.hero.name if self.hero else None,
                'question': self.question,
                'options': {
                    'A': self.option_a,
                    'B': self.option_b,
                    'C': self.option_c,
                    'D': self.option_d
                },
                'correct_answer': self.correct_answer,
                'difficulty': self.difficulty
            }
        
        def __repr__(self):
            return f'<QuizQuestion {self.id}>'
    
    class UserQuizScore(db.Model):
        """Modèle pour enregistrer les scores des utilisateurs"""
        __tablename__ = 'user_quiz_scores'
        
        id = db.Column(db.Integer, primary_key=True)
        session_id = db.Column(db.String(255), nullable=False)
        score = db.Column(db.Integer, default=0)
        total_questions = db.Column(db.Integer, default=0)
        percentage = db.Column(db.Float, default=0.0)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        def to_dict(self):
            return {
                'id': self.id,
                'session_id': self.session_id,
                'score': self.score,
                'total_questions': self.total_questions,
                'percentage': self.percentage,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
        
        def __repr__(self):
            return f'<UserQuizScore {self.session_id}>'
    
    return Category, Hero, QuizQuestion, UserQuizScore