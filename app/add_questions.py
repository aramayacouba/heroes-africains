#!/usr/bin/env python3
"""
Script pour ajouter des questions de quiz
"""

from app import create_app, db
from app.models import init_models

app = create_app()

with app.app_context():
    Category, Hero, QuizQuestion, UserQuizScore = init_models(db)
    
    print("🔄 Ajout de questions de quiz...")
    
    # Vérifier s'il y a des héros
    heroes = Hero.query.all()
    print(f"📊 Héros trouvés: {len(heroes)}")
    
    if len(heroes) == 0:
        print("❌ Aucun héros dans la base - Ajoutez d'abord des héros!")
        print("   Visitez: http://localhost:5000/add-hero")
        exit(1)
    
    # Vérifier s'il y a déjà des questions
    existing_questions = QuizQuestion.query.count()
    print(f"❓ Questions existantes: {existing_questions}")
    
    if existing_questions > 0:
        print("✅ Des questions existent déjà")
        exit(0)
    
    print("\n🔄 Création de questions d'exemple...")
    
    # Créer des questions génériques pour chaque héros
    questions_created = 0
    
    for hero in heroes:
        # Question 1: Sur le héros
        q1 = QuizQuestion(
            hero_id=hero.id,
            question=f"Quel pays d'origine a {hero.name}?",
            option_a=hero.country,
            option_b="Autre pays 1",
            option_c="Autre pays 2",
            option_d="Autre pays 3",
            correct_answer='A',
            difficulty='easy'
        )
        db.session.add(q1)
        questions_created += 1
        
        # Question 2: Époque
        q2 = QuizQuestion(
            hero_id=hero.id,
            question=f"À quelle époque a vécu {hero.name}?",
            option_a=hero.era,
            option_b="XIXe siècle",
            option_c="XVe siècle",
            option_d="XXIe siècle",
            correct_answer='A',
            difficulty='medium'
        )
        db.session.add(q2)
        questions_created += 1
        
        # Question 3: Catégorie
        q3 = QuizQuestion(
            hero_id=hero.id,
            question=f"Dans quel domaine {hero.name} s'est-il distingué?",
            option_a=hero.category.name,
            option_b="Autre domaine 1",
            option_c="Autre domaine 2",
            option_d="Autre domaine 3",
            correct_answer='A',
            difficulty='hard'
        )
        db.session.add(q3)
        questions_created += 1
    
    db.session.commit()
    
    print(f"\n✅ {questions_created} questions créées!")
    print(f"📊 Total questions dans la BD: {QuizQuestion.query.count()}")
    print("\n🎉 Le quiz devrait maintenant fonctionner!")