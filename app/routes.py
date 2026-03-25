from app import db
from app.models import Hero, Category, QuizQuestion, UserQuizScore
from flask import Blueprint, render_template, request, jsonify, session
# from app.models import Hero, Category, QuizQuestion, UserQuizScore, db
from uuid import uuid4
from flask import Flask, send_from_directory, make_response
from datetime import datetime
import mimetypes

main_bp = Blueprint('main', __name__)


@main_bp.route('/static/images/heroes/<filename>')
def serve_hero_image(filename):
    """
    Servir les images avec headers NO-CACHE
    pour forcer le rafraîchissement
    """
    print(f"🖼️  Serveur l'image: {filename}")
    
    try:
        # Sécurité: éviter les chemins en remontée
        if '..' in filename or filename.startswith('/'):
            return 'Fichier invalide', 400
        
        # Servir le fichier
        response = make_response(
            send_from_directory('app/static/images/heroes', filename)
        )
        
        # ✅ HEADERS IMPORTANTS - Pas de cache
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, public, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['ETag'] = f'"{datetime.now().timestamp()}"'
        
        return response
    
    except FileNotFoundError:
        print(f"❌ Fichier non trouvé: {filename}")
        # Retourner placeholder
        return send_from_directory('app/static/images/heroes', 'placeholder.jpg')
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return f'Erreur: {str(e)}', 500

@main_bp.route('/')
def index():
    """Page d'accueil"""
    categories = Category.query.all()
    heroes = Hero.query.limit(6).all()
    return render_template('index.html', categories=categories, heroes=heroes)

@main_bp.route('/hero/<int:hero_id>')
def hero_detail(hero_id):
    """Détail d'un héros"""
    hero = Hero.query.get_or_404(hero_id)
    hero.views += 1
    db.session.commit()
    
    related_heroes = Hero.query.filter_by(category_id=hero.category_id).filter(Hero.id != hero_id).limit(4).all()
    return render_template('hero_detail.html', hero=hero, related_heroes=related_heroes)

@main_bp.route('/category/<int:category_id>')
def category_heroes(category_id):
    """Afficher tous les héros d'une catégorie"""
    category = Category.query.get_or_404(category_id)
    heroes = Hero.query.filter_by(category_id=category_id).all()
    return render_template('category.html', category=category, heroes=heroes)

@main_bp.route('/add-hero', methods=['GET', 'POST'])
def add_hero():
    """Ajouter un nouveau héros"""
    if request.method == 'POST':
        data = request.form
        
        # Validation
        if not all([data.get('name'), data.get('country'), data.get('era'), 
                   data.get('category_id'), data.get('bio')]):
            return jsonify({'error': 'Données incomplètes'}), 400
        
        try:
            hero = Hero(
                name=data['name'],
                country=data['country'],
                era=data['era'],
                category_id=int(data['category_id']),
                bio=data['bio'],
                image_url=data.get('image_url', ''),
                achievements=data.get('achievements', ''),
                birth_year=int(data.get('birth_year', 0)) if data.get('birth_year') else None,
                death_year=int(data.get('death_year', 0)) if data.get('death_year') else None
            )
            db.session.add(hero)
            db.session.commit()
            return jsonify({'success': True, 'hero_id': hero.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    
    categories = Category.query.all()
    return render_template('add_hero.html', categories=categories)

@main_bp.route('/quiz')
def quiz():
    """Page de quiz"""
    questions = QuizQuestion.query.all()
    
    # Créer une session utilisateur si elle n'existe pas
    if 'user_session_id' not in session:
        session['user_session_id'] = str(uuid4())
    
    return render_template('quiz.html', questions=questions)

@main_bp.route('/api/stats')
def get_stats():
    """Obtenir les statistiques du site"""
    total_heroes = Hero.query.count()
    total_categories = Category.query.count()
    total_views = db.session.query(db.func.sum(Hero.views)).scalar() or 0
    
    top_heroes = Hero.query.order_by(Hero.views.desc()).limit(5).all()
    
    return jsonify({
        'total_heroes': total_heroes,
        'total_categories': total_categories,
        'total_views': int(total_views),
        'top_heroes': [h.to_dict() for h in top_heroes]
    })

@main_bp.route('/search')
def search():
    """Rechercher des héros"""
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({'results': []}), 400
    
    heroes = Hero.query.filter(
        db.or_(
            Hero.name.ilike(f'%{query}%'),
            Hero.bio.ilike(f'%{query}%'),
            Hero.country.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    return jsonify({
        'results': [h.to_dict() for h in heroes],
        'total': len(heroes)
    })