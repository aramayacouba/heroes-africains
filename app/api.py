from flask_restful import Resource, reqparse
from app import db
from app.models import Hero, Category, QuizQuestion
# from app.models import Hero, Category, QuizQuestion, db
from flask import request, jsonify

class HeroesList(Resource):
    """API pour lister tous les héros"""
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        pagination = Hero.query.paginate(page=page, per_page=per_page)
        heroes = [h.to_dict() for h in pagination.items]
        
        return {
            'heroes': heroes,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page
        }, 200

class HeroDetail(Resource):
    """API pour détail d'un héros"""
    def get(self, hero_id):
        hero = Hero.query.get(hero_id)
        if not hero:
            return {'error': 'Héros non trouvé'}, 404
        
        return {'hero': hero.to_dict()}, 200
    
    def put(self, hero_id):
        """Mettre à jour un héros"""
        hero = Hero.query.get(hero_id)
        if not hero:
            return {'error': 'Héros non trouvé'}, 404
        
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('bio', type=str)
        parser.add_argument('country', type=str)
        args = parser.parse_args()
        
        if args.name:
            hero.name = args.name
        if args.bio:
            hero.bio = args.bio
        if args.country:
            hero.country = args.country
        
        db.session.commit()
        return {'hero': hero.to_dict()}, 200
    
    def delete(self, hero_id):
        """Supprimer un héros"""
        hero = Hero.query.get(hero_id)
        if not hero:
            return {'error': 'Héros non trouvé'}, 404
        
        db.session.delete(hero)
        db.session.commit()
        return {'message': 'Héros supprimé'}, 200

class CategoriesList(Resource):
    """API pour lister les catégories"""
    def get(self):
        categories = Category.query.all()
        return {
            'categories': [c.to_dict() for c in categories],
            'total': len(categories)
        }, 200

class QuizQuestionsList(Resource):
    """API pour les questions de quiz"""
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))
        
        pagination = QuizQuestion.query.paginate(page=page, per_page=per_page)
        questions = [q.to_dict() for q in pagination.items]
        
        return {
            'questions': questions,
            'total': pagination.total
        }, 200