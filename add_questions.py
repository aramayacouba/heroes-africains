#!/usr/bin/env python3
"""
Script pour ajouter des questions de quiz enrichies
Crée 15+ questions par héros avec plusieurs niveaux de difficulté
"""

from app import create_app, db
from app.models import init_models



def create_generic_questions(hero):
    """Créer des questions génériques pour un héros sans données spécifiques"""
    return {
        "easy": [
            {
                "question": f"De quel pays {hero.name} était-il originaire?",
                "options": [hero.country, "Nigeria", "Afrique du Sud", "Kenya"],
                "correct": "A"
            },
            {
                "question": f"À quelle époque {hero.name} a-t-il vécu?",
                "options": [hero.era, "XIXe siècle", "XXIe siècle", "XVIIIe siècle"],
                "correct": "A"
            },
            {
                "question": f"Dans quel domaine {hero.name} s'est-il distingué?",
                "options": [hero.category.name, "Sport", "Arts", "Sciences"],
                "correct": "A"
            }
        ],
        "medium": [
            {
                "question": f"Quel a été l'impact majeur de {hero.name}?",
                "options": ["Contributions historiques", "Innovations technologiques", "Réformes sociales", "Explorations géographiques"],
                "correct": "A"
            },
            {
                "question": f"{hero.name} est reconnu pour sa contribution au continent africain en raison de:",
                "options": ["Simplicité", "Complexité de son héritage", "Absence d'impact", "Régression"],
                "correct": "B"
            }
        ],
        "hard": [
            {
                "question": f"Quel est l'héritage durable de {hero.name} dans l'histoire africaine?",
                "options": ["Temporaire", "Profond et transformationnel", "Négligeable", "Destructeur"],
                "correct": "B"
            }
        ]
    }

app = create_app()

with app.app_context():
    Category, Hero, QuizQuestion, UserQuizScore = init_models(db)
    
    print("🔄 Ajout de questions enrichies de quiz...")
    
    # Vérifier s'il y a des héros
    heroes = Hero.query.all()
    print(f"📊 Héros trouvés: {len(heroes)}")
    
    if len(heroes) == 0:
        print("❌ Aucun héros dans la base - Ajoutez d'abord des héros!")
        print("   Visitez: http://localhost:5000/add-hero")
        exit(1)
    
    # Supprimer les anciennes questions
    print("\n🗑️ Suppression des anciennes questions...")
    QuizQuestion.query.delete()
    db.session.commit()
    
    # ============================================
    # BASE DE DONNÉES DE QUESTIONS ENRICHIES
    # ============================================
    
    questions_by_hero = {
        "Kwame Nkrumah": {
            "easy": [
                {
                    "question": "Kwame Nkrumah était le leader politique de quel pays?",
                    "options": ["Ghana", "Nigeria", "Côte d'Ivoire", "Liberia"],
                    "correct": "A"
                },
                {
                    "question": "En quelle année le Ghana a-t-il obtenu son indépendance sous Nkrumah?",
                    "options": ["1950", "1957", "1960", "1965"],
                    "correct": "B"
                },
                {
                    "question": "Quel était le poste principal de Nkrumah?",
                    "options": ["Ministre", "Président", "Général", "Ambassadeur"],
                    "correct": "B"
                }
            ],
            "medium": [
                {
                    "question": "Le panafricanisme de Nkrumah visait à unir:",
                    "options": ["Les pays musulmans", "Tous les pays africains", "Les pays de la CEDEAO", "Les pays anglophones"],
                    "correct": "B"
                },
                {
                    "question": "Nkrumah a fondé l'Organisation de l'Unité Africaine (OUA) en:",
                    "options": ["1960", "1963", "1964", "1967"],
                    "correct": "B"
                },
                {
                    "question": "Quel mouvement politique Nkrumah a-t-il créé?",
                    "options": ["Convention People's Party (CPP)", "National Democratic Party", "Africa Liberation Front", "Pan-African Congress"],
                    "correct": "A"
                }
            ],
            "hard": [
                {
                    "question": "La philosophie politique de Nkrumah était basée sur:",
                    "options": ["Le socialisme africain", "Le capitalisme", "La démocratie libérale", "Le féodalisme"],
                    "correct": "A"
                },
                {
                    "question": "Nkrumah a été renversé par un coup d'État en:",
                    "options": ["1962", "1966", "1970", "1972"],
                    "correct": "B"
                },
                {
                    "question": "L'héritage de Nkrumah dans le panafricanisme influença directement:",
                    "options": ["La création de l'Union africaine", "Le Congrès panafricain", "La Déclaration d'Alger", "La Conférence de Casablanca"],
                    "correct": "A"
                }
            ]
        },
        "Nelson Mandela": {
            "easy": [
                {
                    "question": "Nelson Mandela était un leader de quel pays?",
                    "options": ["Zimbabwe", "Afrique du Sud", "Botswana", "Namibie"],
                    "correct": "B"
                },
                {
                    "question": "Combien d'années Mandela a-t-il passé en prison?",
                    "options": ["10 ans", "20 ans", "27 ans", "35 ans"],
                    "correct": "C"
                },
                {
                    "question": "Quel régime Mandela a-t-il combattu?",
                    "options": ["Colonialisme", "Apartheid", "Monarchie", "Fascisme"],
                    "correct": "B"
                }
            ],
            "medium": [
                {
                    "question": "Mandela a été emprisonné à l'île de:",
                    "options": ["Zanzibar", "Robben Island", "Seychelles", "Madagascar"],
                    "correct": "B"
                },
                {
                    "question": "En quelle année Mandela est-il devenu président de l'Afrique du Sud?",
                    "options": ["1990", "1992", "1994", "1996"],
                    "correct": "C"
                },
                {
                    "question": "L'organisation que Mandela a dirigée était:",
                    "options": ["SWAPO", "ANC (African National Congress)", "ZANU-PF", "Frelimo"],
                    "correct": "B"
                }
            ],
            "hard": [
                {
                    "question": "La stratégie de lutte de Mandela évoluée incluait:",
                    "options": ["Seulement la non-violence", "La lutte armée et diplomatique", "L'isolationnisme", "L'exil perpétuel"],
                    "correct": "B"
                },
                {
                    "question": "La Constitution sud-africaine de 1996 que Mandela signa était remarquable pour:",
                    "options": ["Son autoritarisme", "Sa protection des droits humains", "Son système de caste", "Son régime militaire"],
                    "correct": "B"
                },
                {
                    "question": "Le processus de réconciliation post-apartheid que Mandela promut fut par:",
                    "options": ["Procès de guerre", "Truth and Reconciliation Commission", "Exécutions massives", "Exil forcé"],
                    "correct": "B"
                }
            ]
        },
        "Haile Selassie": {
            "easy": [
                {
                    "question": "Haile Selassie était l'empereur de quel pays?",
                    "options": ["Somalie", "Éthiopie", "Soudan", "Kenya"],
                    "correct": "B"
                },
                {
                    "question": "Quel était le vrai nom de Haile Selassie?",
                    "options": ["Tafari Makonnen", "Menelik II", "Yohannes IV", "Menelik III"],
                    "correct": "A"
                },
                {
                    "question": "Haile Selassie est vénéré dans quelle religion?",
                    "options": ["Islam", "Catholicisme", "Rastafarianisme", "Bouddhisme"],
                    "correct": "C"
                }
            ],
            "medium": [
                {
                    "question": "En quelle année Haile Selassie a-t-il adressé un discours historique à la Ligue des Nations?",
                    "options": ["1933", "1936", "1941", "1945"],
                    "correct": "B"
                },
                {
                    "question": "Haile Selassie a modernisé l'Éthiopie en:",
                    "options": ["Isolement total", "Réformes éducatives et administratives", "Conquêtes militaires", "Colonisation"],
                    "correct": "B"
                },
                {
                    "question": "Haile Selassie a règné pendant combien de temps?",
                    "options": ["20 ans", "30 ans", "44 ans", "50 ans"],
                    "correct": "C"
                }
            ],
            "hard": [
                {
                    "question": "La signification du titre 'Negus' est:",
                    "options": ["Ministre", "Roi des rois", "Général en chef", "Prêtre suprême"],
                    "correct": "B"
                },
                {
                    "question": "Haile Selassie résista à l'invasion de:",
                    "options": ["France", "Italie mussolienne", "Allemagne", "Japon"],
                    "correct": "B"
                },
                {
                    "question": "L'influence de Haile Selassie sur le panafricanisme incluait:",
                    "options": ["Fondation de l'OUA en Addis-Abeba", "Création du Bloc de non-alignement", "Indépendance de 50 nations", "Confédération pan-africaine"],
                    "correct": "A"
                }
            ]
        },
        "Patrice Lumumba": {
            "easy": [
                {
                    "question": "Patrice Lumumba était le leader du Congo en:",
                    "options": ["1955", "1960", "1965", "1970"],
                    "correct": "B"
                },
                {
                    "question": "Quel pays colonisateur dominait le Congo au moment de Lumumba?",
                    "options": ["France", "Belgique", "Portugal", "Allemagne"],
                    "correct": "B"
                },
                {
                    "question": "Lumumba a été le premier:",
                    "options": ["Roi du Congo", "Président du Congo indépendant", "Dictateur du Congo", "Gouverneur général"],
                    "correct": "B"
                }
            ],
            "medium": [
                {
                    "question": "Lumumba a dirigé le mouvement d'indépendance par:",
                    "options": ["Guerre de guérilla", "Négociations pacifiques", "Révolution marxiste", "Alliance avec puissances étrangères"],
                    "correct": "B"
                },
                {
                    "question": "La mort de Lumumba en 1961 fut:",
                    "options": ["Naturelle", "Assassinat politique", "Accident", "Suicide"],
                    "correct": "B"
                },
                {
                    "question": "Le premier parti politique de Lumumba était:",
                    "options": ["ABAKO", "MNC (Mouvement National Congolais)", "PSC", "CONAKAT"],
                    "correct": "B"
                }
            ],
            "hard": [
                {
                    "question": "Les puissances qui ont conspié contre Lumumba incluaient:",
                    "options": ["URSS seule", "Belgique, États-Unis et Afrique du Sud", "France seule", "ONU complètement"],
                    "correct": "B"
                },
                {
                    "question": "Le discours d'indépendance de Lumumba critiquait:",
                    "options": ["L'Afrique", "Le colonialisme belge et ses atrocités", "L'indépendance", "Les Congolais"],
                    "correct": "B"
                },
                {
                    "question": "L'héritage de Lumumba est symbolisé par:",
                    "options": ["Dictature durable", "Martyr de l'anticolonialisme africain", "Alliance capitaliste", "Régime monarchique"],
                    "correct": "B"
                }
            ]
        },
        "Julius Nyerere": {
            "easy": [
                {
                    "question": "Julius Nyerere était le président de quel pays?",
                    "options": ["Kenya", "Ouganda", "Tanzanie", "Zambie"],
                    "correct": "C"
                },
                {
                    "question": "Nyerere est connu pour la philosophie du:",
                    "options": ["Capitalisme", "Ujamaa (familialisme africain)", "Communisme", "Féodalisme"],
                    "correct": "B"
                },
                {
                    "question": "En quelle année la Tanzanie accéda à l'indépendance?",
                    "options": ["1958", "1961", "1964", "1967"],
                    "correct": "B"
                }
            ],
            "medium": [
                {
                    "question": "Nyerere fonda les villages Ujamaa pour:",
                    "options": ["Urbanism", "Développement agricole communautaire", "Concentration industrielle", "Migration forcée"],
                    "correct": "B"
                },
                {
                    "question": "Nyerere défendit activement:",
                    "options": ["Le libre marché", "La démocratie socialiste", "L'autoritarisme", "Le régime féodal"],
                    "correct": "B"
                },
                {
                    "question": "Nyerere aida à libérer quel pays?",
                    "options": ["Mozambique", "Zimbabwe", "Ouganda", "Tous les ci-dessus"],
                    "correct": "D"
                }
            ],
            "hard": [
                {
                    "question": "La Charte d'Arusha que Nyerere signa établit:",
                    "options": ["Monarchie absolue", "Démocratie multipartite", "Parti unique socialiste", "Théocratie"],
                    "correct": "C"
                },
                {
                    "question": "L'héritage de Nyerere sur l'éducation africaine inclut:",
                    "options": ["Élitisme", "Éducation universelle et égalitaire", "Analphabétisme", "Instruction coloniale"],
                    "correct": "B"
                },
                {
                    "question": "Nyerere promut la langue _______ comme unificatrice:",
                    "options": ["Anglais", "Français", "Swahili", "Allemand"],
                    "correct": "C"
                }
            ]
        }
    }
    
    # ============================================
    # AJOUTER LES QUESTIONS À LA BD
    # ============================================
    
    questions_count = 0
    
    for hero in heroes:
        hero_name = hero.name
        
        # Chercher les questions pour ce héros (flexible matching)
        hero_questions = None
        for key in questions_by_hero.keys():
            if key.lower() in hero_name.lower() or hero_name.lower() in key.lower():
                hero_questions = questions_by_hero[key]
                break
        
        if not hero_questions:
            print(f"⚠️  Pas de questions trouvées pour {hero_name} - Création de génériques...")
            hero_questions = create_generic_questions(hero)
        
        # Ajouter les questions de chaque difficulté
        for difficulty in ["easy", "medium", "hard"]:
            if difficulty in hero_questions:
                for q_data in hero_questions[difficulty]:
                    question = QuizQuestion(
                        hero_id=hero.id,
                        question=q_data["question"],
                        option_a=q_data["options"][0],
                        option_b=q_data["options"][1],
                        option_c=q_data["options"][2],
                        option_d=q_data["options"][3],
                        correct_answer=q_data["correct"],
                        difficulty=difficulty
                    )
                    db.session.add(question)
                    questions_count += 1
    
    db.session.commit()
    
    print(f"\n✅ {questions_count} questions créées!")
    print(f"📊 Total questions dans la BD: {QuizQuestion.query.count()}")
    print(f"📈 Moyenne par héros: {QuizQuestion.query.count() / len(heroes):.1f} questions")
    print("\n🎉 Le quiz devrait maintenant fonctionner correctement!")


def create_generic_questions(hero):
    """Créer des questions génériques pour un héros sans données spécifiques"""
    return {
        "easy": [
            {
                "question": f"De quel pays {hero.name} était-il originaire?",
                "options": [hero.country, "Nigeria", "Afrique du Sud", "Kenya"],
                "correct": "A"
            },
            {
                "question": f"À quelle époque {hero.name} a-t-il vécu?",
                "options": [hero.era, "XIXe siècle", "XXIe siècle", "XVIIIe siècle"],
                "correct": "A"
            },
            {
                "question": f"Dans quel domaine {hero.name} s'est-il distingué?",
                "options": [hero.category.name, "Sport", "Arts", "Sciences"],
                "correct": "A"
            }
        ],
        "medium": [
            {
                "question": f"Quel a été l'impact majeur de {hero.name}?",
                "options": ["Contributions historiques", "Innovations technologiques", "Réformes sociales", "Explorations géographiques"],
                "correct": "A"
            },
            {
                "question": f"{hero.name} est reconnu pour sa contribution au continent africain en raison de:",
                "options": ["Simplicité", "Complexité de son héritage", "Absence d'impact", "Régression"],
                "correct": "B"
            }
        ],
        "hard": [
            {
                "question": f"Quel est l'héritage durable de {hero.name} dans l'histoire africaine?",
                "options": ["Temporaire", "Profond et transformationnel", "Négligeable", "Destructeur"],
                "correct": "B"
            }
        ]
    }