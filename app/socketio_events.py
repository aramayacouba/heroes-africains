from flask_socketio import emit, join_room, leave_room
from flask import request
from app import db
import app.models as models_module
import random
import uuid
from sqlalchemy.orm import joinedload

# Dictionnaire pour gérer les sessions de quiz
active_quiz_sessions = {}
active_duo_games = {}

def register_socketio_events(socketio, db_instance):
    """Enregistrer les événements SocketIO"""
    
    @socketio.on('connect')
    def handle_connect():
        print(f'✅ Client connecté: {request.sid}')
        emit('response', {'data': 'Connecté au serveur en temps réel'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f'❌ Client déconnecté: {request.sid}')
        
        # Nettoyer les sessions solo
        for session_id, session in list(active_quiz_sessions.items()):
            if session.get('client_id') == request.sid:
                del active_quiz_sessions[session_id]
        
        # Nettoyer les jeux duo
        for game_id, game in list(active_duo_games.items()):
            if request.sid in game['players']:
                print(f"🗑️ Suppression de la partie {game_id} - joueur déconnecté")
                emit('player_disconnected', {'game_id': game_id}, to=game['room'])
                del active_duo_games[game_id]
                break
    
    # ============================================
    # MODE SOLO
    # ============================================
    
    @socketio.on('start_quiz')
    def start_quiz(data):
        """Démarrer une session de quiz solo"""
        user_session_id = data.get('session_id')
        difficulty = data.get('difficulty', 'medium')
        
        print(f"🎯 Démarrage quiz solo - Difficulté: {difficulty}")
        
        try:
            question_count = {
                'easy': 5,
                'medium': 8,
                'hard': 10
            }.get(difficulty, 5)
            
            QuizQuestion = models_module.QuizQuestion
            questions = QuizQuestion.query.options(
                joinedload(QuizQuestion.hero)
            ).filter_by(difficulty=difficulty).all()
            
            if not questions:
                questions = QuizQuestion.query.options(
                    joinedload(QuizQuestion.hero)
                ).all()
            
            selected_questions = random.sample(
                questions, 
                min(question_count, len(questions))
            )
            
            random.shuffle(selected_questions)
            
            # Convertir en dictionnaires
            questions_data = []
            for q in selected_questions:
                questions_data.append({
                    'id': q.id,
                    'question': q.question,
                    'hero_name': q.hero.name if q.hero else 'Inconnu',
                    'option_a': q.option_a,
                    'option_b': q.option_b,
                    'option_c': q.option_c,
                    'option_d': q.option_d,
                    'correct_answer': q.correct_answer,
                    'difficulty': q.difficulty
                })
            
            active_quiz_sessions[user_session_id] = {
                'client_id': request.sid,
                'questions': questions_data,
                'current_index': 0,
                'score': 0,
                'answers': [],
                'difficulty': difficulty,
                'mode': 'solo'
            }
            
            print(f"✅ Quiz solo démarré: {len(questions_data)} questions")
            
            first_q = questions_data[0]
            emit('quiz_started', {
                'total_questions': len(questions_data),
                'current_question': 1,
                'question_data': {
                    'id': first_q['id'],
                    'question': first_q['question'],
                    'hero_name': first_q['hero_name'],
                    'options': {
                        'A': first_q['option_a'],
                        'B': first_q['option_b'],
                        'C': first_q['option_c'],
                        'D': first_q['option_d']
                    }
                }
            })
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            import traceback
            traceback.print_exc()
            emit('error', {'message': f'Erreur serveur: {str(e)}'})
    
    @socketio.on('submit_answer')
    def submit_answer(data):
        """Soumettre une réponse solo"""
        user_session_id = data.get('session_id')
        answer = data.get('answer')
        
        if user_session_id not in active_quiz_sessions:
            emit('error', {'message': 'Session non trouvée'})
            return
        
        session = active_quiz_sessions[user_session_id]
        current_q = session['questions'][session['current_index']]
        
        is_correct = answer == current_q['correct_answer']
        if is_correct:
            session['score'] += 1
        
        session['answers'].append({
            'question_id': current_q['id'],
            'user_answer': answer,
            'correct_answer': current_q['correct_answer'],
            'is_correct': is_correct
        })
        
        emit('answer_result', {
            'is_correct': is_correct,
            'correct_answer': current_q['correct_answer'],
            'score': session['score'],
            'total_answered': len(session['answers'])
        })
        
        if session['current_index'] < len(session['questions']) - 1:
            session['current_index'] += 1
            next_q = session['questions'][session['current_index']]
            
            emit('next_question', {
                'current_question': session['current_index'] + 1,
                'total_questions': len(session['questions']),
                'question_data': {
                    'id': next_q['id'],
                    'question': next_q['question'],
                    'hero_name': next_q['hero_name'],
                    'options': {
                        'A': next_q['option_a'],
                        'B': next_q['option_b'],
                        'C': next_q['option_c'],
                        'D': next_q['option_d']
                    }
                }
            })
        else:
            # Quiz solo terminé
            final_score = session['score']
            total = len(session['questions'])
            percentage = (final_score / total * 100) if total > 0 else 0
            
            UserQuizScore = models_module.UserQuizScore
            user_score = UserQuizScore(
                session_id=user_session_id,
                score=final_score,
                total_questions=total,
                percentage=percentage
            )
            db_instance.session.add(user_score)
            db_instance.session.commit()
            
            emit('quiz_completed', {
                'final_score': final_score,
                'total_questions': total,
                'percentage': round(percentage, 2),
                'answers_detail': session['answers']
            })
            
            del active_quiz_sessions[user_session_id]
    
    @socketio.on('get_leaderboard')
    def get_leaderboard():
        """Obtenir le classement"""
        UserQuizScore = models_module.UserQuizScore
        top_scores = UserQuizScore.query.order_by(
            UserQuizScore.percentage.desc()
        ).limit(10).all()
        
        leaderboard = [
            {
                'rank': i + 1,
                'score': s.score,
                'total_questions': s.total_questions,
                'percentage': s.percentage,
                'date': s.created_at.isoformat()
            }
            for i, s in enumerate(top_scores)
        ]
        
        emit('leaderboard_data', {'leaderboard': leaderboard})
    
    # ============================================
    # MODE DUO - SOLUTION SIMPLIFIÉE ET ROBUSTE
    # ============================================
    
    @socketio.on('create_duo_game')
    def create_duo_game(data):
        """Créer une nouvelle partie duo"""
        difficulty = data.get('difficulty', 'medium')
        player_name = data.get('player_name', 'Joueur')
        
        # Générer un code court
        game_id = str(uuid.uuid4())[:6].upper()
        room_name = f'duo_{game_id}'
        
        print(f"\n{'='*60}")
        print(f"🎮 CRÉATION PARTIE DUO")
        print(f"Code: {game_id}")
        print(f"Joueur 1: {player_name}")
        print(f"Difficulté: {difficulty}")
        print(f"{'='*60}\n")
        
        # Charger les questions dès le départ
        QuizQuestion = models_module.QuizQuestion
        questions = QuizQuestion.query.options(
            joinedload(QuizQuestion.hero)
        ).filter_by(difficulty=difficulty).all()
        
        if not questions:
            questions = QuizQuestion.query.options(
                joinedload(QuizQuestion.hero)
            ).all()
        
        # Sélectionner 5 questions aléatoires
        selected = random.sample(questions, min(5, len(questions)))
        
        # Convertir en dictionnaires
        questions_data = []
        for q in selected:
            questions_data.append({
                'id': q.id,
                'question': q.question,
                'hero_name': q.hero.name if q.hero else 'Inconnu',
                'option_a': q.option_a,
                'option_b': q.option_b,
                'option_c': q.option_c,
                'option_d': q.option_d,
                'correct_answer': q.correct_answer
            })
        
        # Créer la partie
        active_duo_games[game_id] = {
            'game_id': game_id,
            'room': room_name,
            'difficulty': difficulty,
            'questions': questions_data,
            'current_question': 0,
            'players': {
                request.sid: {
                    'name': player_name,
                    'score': 0,
                    'answered': False
                }
            },
            'answers_this_round': {}
        }
        
        join_room(room_name)
        
        # Notifier le créateur
        emit('duo_game_created', {
            'game_id': game_id,
            'player_name': player_name,
            'message': f'Code de jeu: {game_id}'
        })
        
        print(f"✅ Partie créée avec succès: {game_id}")
    
    @socketio.on('join_duo_game')
    def join_duo_game(data):
        """Rejoindre une partie duo existante"""
        game_id = data.get('game_id', '').upper()
        player_name = data.get('player_name', 'Joueur')
        
        print(f"\n{'='*60}")
        print(f"👥 REJOINDRE PARTIE DUO")
        print(f"Code: {game_id}")
        print(f"Joueur 2: {player_name}")
        print(f"{'='*60}\n")
        
        # Vérifier que la partie existe
        if game_id not in active_duo_games:
            print(f"❌ Partie {game_id} non trouvée")
            print(f"📋 Parties disponibles: {list(active_duo_games.keys())}")
            emit('error', {
                'message': f'Partie "{game_id}" non trouvée!',
                'code': game_id
            })
            return
        
        game = active_duo_games[game_id]
        room_name = game['room']
        
        # Vérifier qu'il n'y a qu'un joueur
        if len(game['players']) >= 2:
            print(f"❌ Partie {game_id} est complète")
            emit('error', {'message': 'Cette partie est déjà pleine!'})
            return
        
        # Ajouter le joueur
        game['players'][request.sid] = {
            'name': player_name,
            'score': 0,
            'answered': False
        }
        
        join_room(room_name)
        
        print(f"✅ Joueur 2 ajouté: {player_name}")
        print(f"👥 Joueurs: {len(game['players'])}/2")
        
        # Notifier les deux joueurs que la partie commence
        first_question = game['questions'][0]
        
        emit('duo_game_started', {
            'game_id': game_id,
            'players': [
                {'name': p['name'], 'score': p['score']} 
                for p in game['players'].values()
            ],
            'total_questions': len(game['questions']),
            'current_question': 1,
            'question_data': {
                'id': first_question['id'],
                'question': first_question['question'],
                'hero_name': first_question['hero_name'],
                'options': {
                    'A': first_question['option_a'],
                    'B': first_question['option_b'],
                    'C': first_question['option_c'],
                    'D': first_question['option_d']
                }
            }
        }, to=room_name)
        
        print(f"🎮 Partie {game_id} démarrée avec 2 joueurs!")
    
    @socketio.on('submit_duo_answer')
    def submit_duo_answer(data):
        """Soumettre une réponse en mode duo"""
        game_id = data.get('game_id', '').upper()
        answer = data.get('answer')
        player_sid = request.sid
        
        print(f"\n📨 Réponse reçue - Game: {game_id}, Réponse: {answer}")
        
        # Vérifications
        if game_id not in active_duo_games:
            print(f"❌ Partie {game_id} non trouvée")
            emit('error', {'message': 'Partie non trouvée'})
            return
        
        game = active_duo_games[game_id]
        
        if player_sid not in game['players']:
            print(f"❌ Joueur {player_sid} non trouvé")
            emit('error', {'message': 'Joueur non trouvé'})
            return
        
        if game['current_question'] >= len(game['questions']):
            print(f"❌ Index de question invalide")
            emit('error', {'message': 'Erreur: index invalide'})
            return
        
        # Récupérer la question actuelle
        current_q = game['questions'][game['current_question']]
        is_correct = answer == current_q['correct_answer']
        
        player_name = game['players'][player_sid]['name']
        
        # Mettre à jour le score si correct
        if is_correct:
            game['players'][player_sid]['score'] += 1
        
        # Marquer comme ayant répondu
        game['players'][player_sid]['answered'] = True
        game['answers_this_round'][player_sid] = {
            'name': player_name,
            'answer': answer,
            'is_correct': is_correct,
            'correct_answer': current_q['correct_answer']
        }
        
        print(f"✅ {player_name}: {answer} ({'✓' if is_correct else '✗'})")
        print(f"📊 Réponses: {len(game['answers_this_round'])}/{len(game['players'])}")
        
        # Afficher le résultat à tous
        emit('duo_answer_received', {
            'player_name': player_name,
            'player_sid': player_sid,  # ✅ AJOUTER L'ID DU JOUEUR
            'is_correct': is_correct,
            'correct_answer': current_q['correct_answer']
        }, to=game['room'])
        
        # Vérifier si tous ont répondu
        all_answered = all(p['answered'] for p in game['players'].values())
        
        if all_answered:
            print(f"\n{'='*60}")
            print(f"✅ Tous les joueurs ont répondu!")
            print(f"{'='*60}\n")
            
            # Réinitialiser les flags
            for p in game['players'].values():
                p['answered'] = False
            
            game['answers_this_round'] = {}
            
            # Passer à la question suivante
            if game['current_question'] < len(game['questions']) - 1:
                game['current_question'] += 1
                next_q = game['questions'][game['current_question']]
                
                print(f"➡️ Question suivante: {game['current_question'] + 1}/{len(game['questions'])}\n")
                
                # Envoyer la prochaine question
                emit('duo_next_question', {
                    'current_question': game['current_question'] + 1,
                    'total_questions': len(game['questions']),
                    'players': [
                        {'name': p['name'], 'score': p['score']} 
                        for p in game['players'].values()
                    ],
                    'question_data': {
                        'id': next_q['id'],
                        'question': next_q['question'],
                        'hero_name': next_q['hero_name'],
                        'options': {
                            'A': next_q['option_a'],
                            'B': next_q['option_b'],
                            'C': next_q['option_c'],
                            'D': next_q['option_d']
                        }
                    }
                }, to=game['room'])
            else:
                # Fin du quiz
                print(f"\n{'='*60}")
                print(f"🏆 PARTIE TERMINÉE - {game_id}")
                print(f"{'='*60}\n")
                
                # Calculer les résultats
                results = []
                for sid, player in game['players'].items():
                    percentage = (player['score'] / len(game['questions']) * 100)
                    results.append({
                        'name': player['name'],
                        'score': player['score'],
                        'total': len(game['questions']),
                        'percentage': round(percentage, 2)
                    })
                
                # Trier par score
                results.sort(key=lambda x: x['score'], reverse=True)
                
                for i, r in enumerate(results):
                    print(f"#{i+1} {r['name']}: {r['score']}/{r['total']} ({r['percentage']}%)")
                print()
                
                # Ajouter les rangs
                for i, r in enumerate(results):
                    r['rank'] = i + 1
                
                # Envoyer les résultats
                emit('duo_game_completed', {
                    'game_id': game_id,
                    'results': results
                }, to=game['room'])
                
                # Nettoyer la partie
                del active_duo_games[game_id]
                print(f"🗑️ Partie {game_id} supprimée\n")