#!/usr/bin/env python3
"""
Script pour ajouter 24+ héros africains complets avec biographies détaillées
"""

from app import create_app, db
from app.models import init_models

app = create_app()

with app.app_context():
    Category, Hero, QuizQuestion, UserQuizScore = init_models(db)
    
    print("🔄 Ajout des héros africains complets...")
    
    # Récupérer les catégories
    categories = {cat.name: cat for cat in Category.query.all()}
    
    if not categories:
        print("❌ Aucune catégorie trouvée! Exécutez l'app d'abord.")
        exit(1)
    
    # ============================================
    # DONNÉES COMPLÈTES DES HÉROS
    # ============================================
    
    heroes_data = [
        # INDÉPENDANCE & POLITIQUE
        {
            "name": "Kwame Nkrumah",
            "country": "Ghana",
            "era": "XXe siècle (1909-1972)",
            "category": "Indépendance & Politique",
            "birth_year": 1909,
            "death_year": 1972,
            "bio": "Kwame Nkrumah (1909-1972) fut le premier président de la Guinée et leader charismatique du mouvement panafricain. Éducateur et nationaliste, il dirigea le Ghana vers l'indépendance en 1957, mettant fin à plus de 100 ans de domination coloniale britannique. Nkrumah révolutionna l'Afrique en promouvant l'unification continentale et en fondant l'Organisation de l'Unité Africaine (OUA). Son engagement envers le socialisme africain et l'égalité des droits inspira des générations d'activistes. Bien que renversé par un coup d'État en 1966, son héritage panafricain continue d'influencer les mouvements d'unité africaine aujourd'hui.",
            "achievements": "Indépendance du Ghana (1957)\nFondateur du panafricanisme\nPremier président du Ghana indépendant\nCréateur de l'Organisation de l'Unité Africaine\nRéformes éducatives révolutionnaires\nSocialisme africain",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Kwame_Nkrumah_%281960%29.jpg/440px-Kwame_Nkrumah_%281960%29.jpg"
        },
        {
            "name": "Nelson Mandela",
            "country": "Afrique du Sud",
            "era": "XXe-XXIe siècles (1918-2013)",
            "category": "Droits Humains & Paix",
            "birth_year": 1918,
            "death_year": 2013,
            "bio": "Nelson Rolihlahla Mandela (1918-2013) était un révolutionnaire sud-africain et premier président noir de l'Afrique du Sud. Après 27 années d'emprisonnement sur l'île de Robben Island pour ses activités contre l'apartheid, il émergea en 1990 comme leader incontesté de la lutte pour la liberté. Mandela négocia pacifiquement la fin du régime ségrégationniste et établit une démocratie multiraciale. Son dédication à la réconciliation, incarnée par la Commission Vérité et Réconciliation, posa les fondations d'une nouvelle Afrique du Sud. Mandela devint une icône mondiale de paix, justice et dignité humaine.",
            "achievements": "27 ans de lutte contre l'apartheid\nPremier président noir d'Afrique du Sud\nPrix Nobel de la Paix (1993)\nCommission Vérité et Réconciliation\nAbolition du régime d'apartheid\nRéconciliation nationale pacifique",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Nelson_Mandela-2008_%28edit%29.jpg/440px-Nelson_Mandela-2008_%28edit%29.jpg"
        },
        {
            "name": "Haile Selassie I",
            "country": "Éthiopie",
            "era": "XXe siècle (1892-1975)",
            "category": "Indépendance & Politique",
            "birth_year": 1892,
            "death_year": 1975,
            "bio": "Haile Selassie I, née Tafari Makonnen (1892-1975), fut le dernier empereur d'Éthiopie et symbole du panafricanisme. Il modernisa l'Éthiopie en introduisant l'éducation, les réformes administratives et les infrastructures. Selassie résista brillamment à l'invasion italienne en 1936 et obtint le respect international pour son courage. Vénéré comme messie dans le rastafarianisme, son vision d'unité africaine influença les mouvements de libération à travers le continent. En 1963, il fonda l'Organisation de l'Unité Africaine, consolidant le rêve panafricain.",
            "achievements": "Résistance à l'invasion italienne (1936)\nFondateur de l'OUA\nModernisateur de l'Éthiopie\nDéfenseur du panafricanisme\nVeneration dans le rastafarianisme\nDéveloppement éducatif et administratif",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Haile_Selassie_in_1967.jpg/440px-Haile_Selassie_in_1967.jpg"
        },
        {
            "name": "Patrice Lumumba",
            "country": "République Démocratique du Congo",
            "era": "XXe siècle (1925-1961)",
            "category": "Indépendance & Politique",
            "birth_year": 1925,
            "death_year": 1961,
            "bio": "Patrice Émery Lumumba (1925-1961) fut le premier ministre ministre de la République Démocratique du Congo indépendante et martyr de l'anticolonialisme africain. Oratrice passionnée et leader nationaliste, il mobilisa les Congolais contre la domination belge. Son discours d'indépendance du 30 juin 1960 critiqua vertement le colonialisme et ses atrocités. Bien que sa présidence fût brève et tumulte, Lumumba incarna la dignité et le courage face à l'oppression. Son assassinat politique en 1961, orchestré par des puissances étrangères, le transforma en symbole martyr de la liberté africaine.",
            "achievements": "Premier ministre du Congo indépendant\nCritique du colonialisme belge\nLeader du Mouvement National Congolais\nDiscours historique d'indépendance\nSymbole du panafricanisme\nMartyr de la liberté africaine",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Patrice_Lumumba_cropped.jpg/440px-Patrice_Lumumba_cropped.jpg"
        },
        {
            "name": "Julius Nyerere",
            "country": "Tanzanie",
            "era": "XXe siècle (1922-1999)",
            "category": "Indépendance & Politique",
            "birth_year": 1922,
            "death_year": 1999,
            "bio": "Julius Kambarage Nyerere (1922-1999) fut le premier président de la Tanzanie et architecte du développement post-colonial africain. Formé en éducation, il appliqua sa philosophie de l'Ujamaa (familialisme africain) pour construire une nation basée sur l'égalité et la coopération. Nyerere développa les villages Ujamaa pour promouvoir l'autosuffisance agricole et créa une société socialiste équitable. Supporter actif des mouvements de libération en Afrique australe, il aida à libérer le Zimbabwe, le Mozambique et l'Ouganda. Nyerere privilégia l'éducation universelle, en particulier l'alphabétisation, transformant la Tanzanie en modèle de développement équitable.",
            "achievements": "Fondateur de la politique Ujamaa\nPremier président de la Tanzanie indépendante\nPromoteur de l'éducation universelle\nDefenseur des mouvements de libération\nCréateur du Parti unique socialist\nConsolidation de l'identité tanzenienne",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Julius_Nyerere_Ar.jpg/440px-Julius_Nyerere_Ar.jpg"
        },
        
        # LITTÉRATURE & CULTURE
        {
            "name": "Chinua Achebe",
            "country": "Nigeria",
            "era": "XXe-XXIe siècles (1930-2013)",
            "category": "Littérature & Culture",
            "birth_year": 1930,
            "death_year": 2013,
            "bio": "Chinua Achebe (1930-2013) fut le plus grand écrivain africain du XXe siècle. Son roman 'Les Choses s'effondrent' (1958) révolutionna la littérature africaine en offrant une perspective authentique africaine sur le colonialisme. Achebe brisa les stéréotypes occidentaux et établit la voix africaine dans le canon littéraire mondial. Ses œuvres explorent l'impact du colonialisme, les traditions culturelles et l'identité postcoloniale. Au-delà de la littérature, Achebe fut aussi éditeur, essayiste et humanitaire engagé. Son influence sur la littérature africaine et mondiale est immense et durable.",
            "achievements": "Auteur des Choses s'effondrent\nFondateur de la voix littéraire africaine\nPrix Man Booker du Commonwealth\nEditeur de magazines littéraires\nImportance dans le canon littéraire mondial\nRepérage des voix africaines",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Chinua_Achebe.jpg/440px-Chinua_Achebe.jpg"
        },
        {
            "name": "Chimamanda Ngozi Adichie",
            "country": "Nigeria",
            "era": "XXIe siècle (née 1977)",
            "category": "Littérature & Culture",
            "birth_year": 1977,
            "death_year": None,
            "bio": "Chimamanda Ngozi Adichie (née 1977) est une écrivaine nigériane contemporaine de renommée mondiale. Ses romans 'Americanah' et 'Demi d'une couleur jaune soleil' explorent les thèmes d'identité, d'immigration, de race et de genre avec profondeur et nuance. Adichie est aussi une conférencière brillante, dont le TED talk 'Nous devrions tous être féministes' inspira des millions de personnes. Ses essais et articles contribuent au discours contemporain sur le féminisme africain et la littérature. Elle représente l'écrivain africain contemporain, racontant des histoires universelles avec une voix uniquement africaine.",
            "achievements": "Auteure d'Americanah\nTED talker mondiale\nFéministe engagée\nVoix de la littérature africaine contemporaine\nAuteure primée internationalement\nAdvocate pour les histoires africaines",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Chimamanda_Ngozi_Adichie_-_Hay_Festival_2018.jpg/440px-Chimamanda_Ngozi_Adichie_-_Hay_Festival_2018.jpg"
        },
        {
            "name": "Wole Soyinka",
            "country": "Nigeria",
            "era": "XXe-XXIe siècles (né 1934)",
            "category": "Littérature & Culture",
            "birth_year": 1934,
            "death_year": None,
            "bio": "Wole Soyinka (né 1934) est un dramaturge, poète et essayiste nigérian de premier plan. Premier Africain à recevoir le Prix Nobel de Littérature (1986), Soyinka utilise le théâtre comme véhicule de critique sociale et politique. Ses pièces 'La Route' et 'Les Lions et les Joyaux' explorent les contradictions de la société moderne africaine. Au-delà de la littérature, Soyinka est un critique social engagé qui s'oppose au despotisme et promeut les droits de l'homme. Son engagement vis-à-vis de l'intégrité et de la vérité le rend une figure morale du continent africain.",
            "achievements": "Prix Nobel de Littérature (1986)\nDramaturge révolutionnaire\nPoète et essayiste influent\nCritique social courageux\nOpposant au despotisme\nRepresentant culturel de l'Afrique",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Wole_Soyinka_DSC_0031.jpg/440px-Wole_Soyinka_DSC_0031.jpg"
        },
        
        # SCIENCES & TECHNOLOGIE
        {
            "name": "Philip Emeagwali",
            "country": "Nigeria",
            "era": "XXe-XXIe siècles (né 1954)",
            "category": "Sciences & Technologie",
            "birth_year": 1954,
            "death_year": None,
            "bio": "Philip Emeagwali (né 1954) est un informaticien nigérian et pionnier du calcul haute performance. Ingénieur autodidacte, il développa des algorithmes révolutionnaires pour le calcul parallèle qui transformèrent les simulations scientifiques. Ses contributions à l'informatique furent décisives pour les applications en géophysique, climat et recherche pétrolière. Emeagwali incarne l'esprit innovant africain et la capacité de génies africains à rivaliser avec les meilleures penseurs mondiaux. Il reçut le Prix Gordon Bell pour ses avancées en technologie informatique.",
            "achievements": "Pionnier du calcul parallèle\nPrix Gordon Bell\nInnovations en informatique haute performance\nContributions à la géophysique\nRéchauffement climatique et simulations\nReconaissance scientifique mondiale",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Philip_Emeagwali_-_2008.jpg/440px-Philip_Emeagwali_-_2008.jpg"
        },
        {
            "name": "Cheikh Anta Diop",
            "country": "Sénégal",
            "era": "XXe siècle (1923-1986)",
            "category": "Éducation & Philosophie",
            "birth_year": 1923,
            "death_year": 1986,
            "bio": "Cheikh Anta Diop (1923-1986) fut un historien, anthropologue et politicien sénégalais révolutionnaire. Son œuvre maîtresse 'Les Racines égyptiennes de la civilisation grecque' réécrivit l'histoire africaine en démontrant l'influence des civilisations africaines antiques sur le monde occidental. Diop défia les récits eurocentriques et plaça les Africains au centre de l'histoire humaine. Ses recherches scientifiques utilisant la datation au carbone radioactif établirent des preuves irréfutables de ses théories. Diop inspira un mouvement de récupération de l'histoire et de la fierté africaines, influençant des générations de chercheurs et d'intellectuels.",
            "achievements": "Réécriture de l'histoire africaine\nDémonisation de l'influence africaine antique\nRecherches scientifiques novatrices\nFondateur du nationalisme intellectuel africain\nOuvrages académiques majeurs\nRépudiation du récit eurocentriste",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Cheikh_Anta_Diop.jpg/440px-Cheikh_Anta_Diop.jpg"
        },
        
        # MILITAIRE & RÉSISTANCE
        {
            "name": "Almamy Samory Touré",
            "country": "Mali",
            "era": "XIXe-XXe siècles (1830-1900)",
            "category": "Militaire & Résistance",
            "birth_year": 1830,
            "death_year": 1900,
            "bio": "Samori Touré (1830-1900) fut un général et empire-builder ouest-africain qui construisit un empire puissant et résista férocement à l'expansion coloniale française. Créateur d'un État militaire centralisé, il modernisa ses forces avec des armes européennes et des tactiques stratégiques. Pendant 30 ans, Samori combattit les colonialistes français, infligeant des défaites humiliantes aux forces européennes. Bien que finalement vaincu par le nombre et les ressources supérieures des Français, son résistance prolongée inspira les mouvements anticoloniaux africains. Samori Touré symbolise le courage et la dignité face à la domination coloniale.",
            "achievements": "Fondateur de l'Empire Wassoulou\nRésistance prolongée au colonialisme\nModernisation de l'armée africaine\nStratégie militaire novatrice\nSymbole de la résistance africaine\nProtection des territoires africains",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Samory_Toure.jpg/440px-Samory_Toure.jpg"
        },
        {
            "name": "Yaa Asantewaa",
            "country": "Ghana",
            "era": "XIXe-XXe siècles (1840-1921)",
            "category": "Militaire & Résistance",
            "birth_year": 1840,
            "death_year": 1921,
            "bio": "Yaa Asantewaa (1840-1921) fut une guerrière et leader de la Rébellion Asante contre la domination coloniale britannique. À 60 ans, elle rallia les chefs Asante à révolter contre les Britanniques par un appel passionné. Elle déclara 'Si vous, les hommes d'Asante, n'allez pas marcher, je prendrai les armes en tant que femme'. Sa Guerre de la Reine (1900-1902) marqua la dernière grande résistance contre la colonisation britannique en Afrique de l'Ouest. Bien que vaincu par les forces britanniques supérieures, sa révolte affirma la fierté et l'indépendance des Asante.",
            "achievements": "Leader de la Rébellion Asante\nGuerre de la Reine (1900-1902)\nRallliement des chefs Asante\nSymbole féminin de la résistance\nDéfense de la fierté Asante\nMouvements de libération féminine",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/YaaAsantewa.jpg/440px-YaaAsantewa.jpg"
        },
        {
            "name": "Nzinga d'Ndongo et Matamba",
            "country": "Angola",
            "era": "XVIIe siècle (1583-1663)",
            "category": "Militaire & Résistance",
            "birth_year": 1583,
            "death_year": 1663,
            "bio": "Nzinga de Ndongo et Matamba (1583-1663) fut une reine angolaise et guerrière qui résista 40 ans à la traite d'esclaves portugaise et à la colonisation. En tant que diplomate perspicace, elle négocia des alliances stratégiques et utilisa les tactiques militaires et politiques pour protéger son peuple. Nzinga combattit les Portugais et les trafiquants d'esclaves avec une détermination féroce et un intellect politique remarquable. Elle fonda des États indépendants et maintint l'intégrité territoriale contre les puissances étrangères. Nzinga symbolise le courage féminin et la résistance aux dépréciations coloniales.",
            "achievements": "Reine guerrière de l'Angola\nRésistance à la traite d'esclaves\nAlliances diplomatiques novatrices\nDefense de Ndongo et Matamba\nFondation d'États indépendants\nSymbole féminin de la dignité africaine",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/01/Nzinga_of_Ndongo_and_Matamba.jpg/440px-Nzinga_of_Ndongo_and_Matamba.jpg"
        },
        
        # DROITS HUMAINS & PAIX
        {
            "name": "Steve Biko",
            "country": "Afrique du Sud",
            "era": "XXe siècle (1946-1977)",
            "category": "Droits Humains & Paix",
            "birth_year": 1946,
            "death_year": 1977,
            "bio": "Stephen Bantu 'Steve' Biko (1946-1977) fut un activiste anti-apartheid sud-africain et fondateur du mouvement de Conscience Noire. Biko réorienta la lutte contre l'apartheid en mettant l'accent sur la fierté noire et l'autonomisation psychologique. Sa philosophie de Conscience Noire promut l'estime de soi africaine et la dignité face à la discrimination systématique. Bien que jeune, ses écrits et ses paroles inspirèrent une génération de résistants. Assassiné par la police de sécurité en 1977, Biko devint un martyr du mouvement pour la justice. Son héritage continue d'inspirer les mouvements de lutte contre le racisme et pour l'égalité.",
            "achievements": "Fondateur du mouvement de Conscience Noire\nPhilosophie de fierté noire\nActiviste anti-apartheid courageux\nEcrivain et penseur inspirant\nMartyr de la justice raciale\nHéritage durable dans la lutte contre le racisme",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Steve_Biko.jpg/440px-Steve_Biko.jpg"
        },
        {
            "name": "Desmond Tutu",
            "country": "Afrique du Sud",
            "era": "XXe-XXIe siècles (1931-2021)",
            "category": "Droits Humains & Paix",
            "birth_year": 1931,
            "death_year": 2021,
            "bio": "Desmond Mpilo Tutu (1931-2021) fut un évêque sud-africain épiscopal et leader du mouvement anti-apartheid. Homme d'église passionné, Tutu utilisa sa foi pour combattre l'injustice. En tant que Président de la Commission Vérité et Réconciliation, il orchestrat un processus révolutionnaire de guérison et de réconciliation nationales. Tutu prôna le pardon sans impunité et la dignité humaine pour tous. Reconnu mondialement pour son engagement envers la paix, la justice et la défense des droits de l'homme, Tutu reçut le Prix Nobel de la Paix en 1984. Son héritage continue d'influencer les mouvements de paix et de justice dans le monde.",
            "achievements": "Évêque anti-apartheid courageux\nPrix Nobel de la Paix (1984)\nPrésident de la Commission Vérité et Réconciliation\nPhilosophie de pardon et réconciliation\nAdvocate des droits humains\nLeader spirituel de la transformation sud-africaine",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Desmond_Tutu.jpg/440px-Desmond_Tutu.jpg"
        },
        {
            "name": "Kofi Annan",
            "country": "Ghana",
            "era": "XXe-XXIe siècles (1938-2018)",
            "category": "Droits Humains & Paix",
            "birth_year": 1938,
            "death_year": 2018,
            "bio": "Kofi Atta Annan (1938-2018) fut le septième Secrétaire général des Nations unies et diplomate ghanéen de renommée mondiale. Pendant 10 ans, Annan prôna la paix, les droits de l'homme et le développement durable. Il initia la doctrine de la 'Responsabilité de Protéger' pour prévenir les génocides et les crimes contre l'humanité. Annan fonda la Fondation Kofi Annan pour promouvoir la bonne gouvernance et la paix en Afrique. Bien que confronté à des crises complexes, Annan maintint l'intégrité morale et l'engagement envers les principes de l'ONU. Son héritage continue d'influencer les politiques internationales de paix et de développement.",
            "achievements": "Secrétaire général de l'ONU\nPrix Nobel de la Paix (2001)\nPromotion de la Responsabilité de Protéger\nFondateur de la Fondation Kofi Annan\nDefenseur des droits humains internationaux\nLeader de la diplomatie africaine",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Kofi_Annan_%282006%29.jpg/440px-Kofi_Annan_%282006%29.jpg"
        },
        {
            "name": "Ellen Johnson Sirleaf",
            "country": "Liberia",
            "era": "XXe-XXIe siècles (née 1938)",
            "category": "Droits Humains & Paix",
            "birth_year": 1938,
            "death_year": None,
            "bio": "Ellen Johnson Sirleaf (née 1938) fut la première femme présidente d'Afrique de l'Ouest et leader du Liberia post-conflit. Économiste formée, elle reconstruit une nation dévastée par la guerre civile. Sirleaf établit la Commission Réconciliation et Pardon et promut la bonne gouvernance. En tant que femme leader dans un contexte patriarcal, elle brisa les barrières et inspira les femmes partout en Afrique. Elle reçut le Prix Nobel de la Paix en 2011 pour ses efforts de paix et de droits des femmes. Son administration se concentra sur la reconstruction économique et la reconstruction de l'État de droit.",
            "achievements": "Première femme présidente d'Afrique de l'Ouest\nPrix Nobel de la Paix (2011)\nReconstruction du Liberia post-conflit\nPromotion des droits des femmes\nBonne gouvernance et transparence\nLeadership économique féminin",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Ellen_Johnson_Sirleaf_%282012%29.jpg/440px-Ellen_Johnson_Sirleaf_%282012%29.jpg"
        },
        
        # COMMERCE & ENTREPRENEURIAT
        {
            "name": "Aliko Dangote",
            "country": "Nigeria",
            "era": "XXe-XXIe siècles (né 1957)",
            "category": "Commerce & Entrepreneuriat",
            "birth_year": 1957,
            "death_year": None,
            "bio": "Aliko Dangote (né 1957) est un entrepreneur nigérian et l'homme le plus riche d'Afrique. Fondateur du Groupe Dangote, il construisit un empire commercial massif dans l'alimentaire, le ciment et l'agriculture. Dangote révolutionna les industries manufacturières africaines par l'intégration verticale et l'innovation. Son usine de ciment est l'une des plus modernes du monde. Dangote promeut l'entrepreneuriat africain et l'industrialisation du continent. Philanthrope engagé, il investit dans l'éducation et les services de santé. Dangote symbolise le succès entrepreneurial africain et la capacité des Africains à bâtir des empires économiques.",
            "achievements": "Fondateur du Groupe Dangote\nHmme le plus riche d'Afrique\nRévolutionaire de l'industrie manufacturière africaine\nCimenterie ultra-moderne\nPhilanthrope engagé\nAdvocate de l'entrepreneuriat africain",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Aliko_Dangote_2017.jpg/440px-Aliko_Dangote_2017.jpg"
        },
        
        # SPIRITUALITÉ & SAGESSE
        {
            "name": "Thomas Sankara",
            "country": "Burkina Faso",
            "era": "XXe siècle (1949-1987)",
            "category": "Indépendance & Politique",
            "birth_year": 1949,
            "death_year": 1987,
            "bio": "Thomas Sankara (1949-1987) fut un révolutionnaire burkinabè et leader visionnaire du Burkina Faso. Président marxiste-léniniste, il transforma le pays en 4 ans par des réformes radicales en éducation, santé et agriculture. Sankara plaça l'autosuffisance et la fierté africaine au centre de sa révolution. Il refusa le dettes de la Banque mondiale et prôna l'indépendance économique. Sankara opposa aussi la discrimination contre les femmes et promut l'égalité des genres. Assassiné lors d'un coup d'État en 1987, il devint un symbole du socialisme africain et de la résistance à l'impérialisme. Son héritage inspira les mouvements progressistes en Afrique.",
            "achievements": "Révolutionnaire du Burkina Faso\nTransformation radicale de la nation\nAutosuffisance économique\nRéformes éducatives massives\nPromotion de l'égalité des genres\nRésistance à l'impérialisme occidental",
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/Thomas_Sankara.jpg/440px-Thomas_Sankara.jpg"
        }
    ]
    
    # ============================================
    # AJOUTER LES HÉROS À LA BD
    # ============================================
    
    heroes_count = 0
    
    for hero_data in heroes_data:
        # Vérifier si le héros existe déjà
        existing = Hero.query.filter_by(name=hero_data['name']).first()
        if existing:
            print(f"⏭️  {hero_data['name']} existe déjà - Sauté")
            continue
        
        # Trouver la catégorie
        category = categories.get(hero_data['category'])
        if not category:
            print(f"⚠️  Catégorie '{hero_data['category']}' non trouvée pour {hero_data['name']}")
            continue
        
        # Créer le héros
        hero = Hero(
            name=hero_data['name'],
            country=hero_data['country'],
            era=hero_data['era'],
            category_id=category.id,
            bio=hero_data['bio'],
            achievements=hero_data['achievements'],
            image_url=hero_data['image_url'],
            birth_year=hero_data['birth_year'],
            death_year=hero_data['death_year'],
            views=0
        )
        
        db.session.add(hero)
        heroes_count += 1
        print(f"✅ {hero_data['name']} ajouté")
    
    db.session.commit()
    
    print(f"\n✅ {heroes_count} nouveaux héros ajoutés!")
    print(f"📊 Total héros dans la BD: {Hero.query.count()}")
    print(f"✅ Base de données enrichie et prête!")