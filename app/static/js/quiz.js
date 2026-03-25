// ========================================
// CONFIGURATION DU QUIZ
// ========================================

let quizState = {
    sessionId: null,
    difficulty: 'medium',
    selectedAnswer: null,
    mode: 'solo'
};

let duoGameState = {
    gameId: null,
    playerName: '',
    isStarted: false
};

// Initialiser SocketIO
const socket = io({
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: 5
});

// ========================================
// CONNEXION SOCKETIO
// ========================================

socket.on('connect', function() {
    console.log('✅ Connecté au serveur');
    showAlert('Connecté au serveur', 'success');
});

socket.on('disconnect', function() {
    console.log('❌ Déconnecté');
    showAlert('Déconnecté du serveur', 'error');
});

socket.on('error', function(error) {
    console.error('❌ Erreur:', error);
    if (error.code) {
        showAlert(`Erreur: "${error.code}" non trouvé!`, 'error');
    } else {
        showAlert(error.message || 'Erreur serveur', 'error');
    }
});

// ========================================
// ÉVÉNEMENTS SOLO
// ========================================

socket.on('quiz_started', function(data) {
    console.log('🎯 Quiz démarré');
    showQuizSection();
    document.getElementById('totalQuestions').textContent = data.total_questions;
    displayQuestion(data.question_data, data.current_question, data.total_questions);
});
function displayQuestion(questionData, current, total) {
    const container = document.getElementById('questionContainer');
    
    container.innerHTML = `
        <div class="hero-info fade-enter">
            <i class="fas fa-user-circle"></i>
            <div>
                <strong>À propos de:</strong> ${questionData.hero_name}
            </div>
        </div>
        <div class="question-text">${questionData.question}</div>
        <div class="quiz-options">
            <button class="quiz-option" onclick="selectAnswer(this, 'A')">
                <span class="option-label">A</span>
                <span>${questionData.options.A}</span>
            </button>
            <button class="quiz-option" onclick="selectAnswer(this, 'B')">
                <span class="option-label">B</span>
                <span>${questionData.options.B}</span>
            </button>
            <button class="quiz-option" onclick="selectAnswer(this, 'C')">
                <span class="option-label">C</span>
                <span>${questionData.options.C}</span>
            </button>
            <button class="quiz-option" onclick="selectAnswer(this, 'D')">
                <span class="option-label">D</span>
                <span>${questionData.options.D}</span>
            </button>
        </div>
        <div class="text-center mt-4">
            <button class="btn btn-warning btn-lg" id="submitBtn" onclick="submitAnswer()" disabled style="min-width: 200px;">
                <i class="fas fa-check-circle me-2"></i>Valider
            </button>
        </div>
    `;
}

socket.on('next_question', function(data) {
    console.log('➡️ Prochaine question');
    updateProgress(data.current_question, data.total_questions);
    displayQuestion(data.question_data, data.current_question, data.total_questions);
    quizState.selectedAnswer = null;
});

socket.on('answer_result', function(data) {
    console.log('✔️ Résultat:', data);
    showAnswerFeedback(data.is_correct, data.correct_answer);
    document.getElementById('currentScore').textContent = data.score;
    disableAllAnswerButtons();
});

socket.on('quiz_completed', function(data) {
    console.log('🏆 Quiz terminé');
    showResults(data.final_score, data.total_questions, data.percentage, data.answers_detail);
});

socket.on('leaderboard_data', function(data) {
    console.log('🏅 Classement');
    displayLeaderboard(data.leaderboard);
});

// ========================================
// ÉVÉNEMENTS DUO
// ========================================

socket.on('duo_game_created', function(data) {
    console.log('🎮 Partie créée:', data);
    duoGameState.gameId = data.game_id;
    duoGameState.playerName = data.player_name;
    
    document.getElementById('startSection').style.display = 'none';
    document.getElementById('duoWaitingSection').style.display = 'block';
    document.getElementById('duoGameCode').textContent = data.game_id;
    document.getElementById('duoWaitingMessage').innerHTML = `
        <div class="text-center">
            <div class="spinner-border mb-3" role="status">
                <span class="visually-hidden">Chargement...</span>
            </div>
            <h5>En attente d'un adversaire...</h5>
            <p class="text-muted">Code: <strong style="font-size: 1.3rem;">${data.game_id}</strong></p>
        </div>
    `;
    
    showAlert(`Votre code: ${data.game_id}`, 'info');
});

socket.on('duo_game_started', function(data) {
    console.log('🎮 Partie duo démarrée');
    duoGameState.isStarted = true;
    duoGameState.gameId = data.game_id;
    
    // ✅ ENREGISTRER MON ID DE JOUEUR
    sessionStorage.setItem('myPlayerId', socket.id);
    console.log(`📝 Mon ID: ${socket.id}`);
    
    document.getElementById('duoWaitingSection').style.display = 'none';
    document.getElementById('duoGameSection').style.display = 'block';
    
    document.getElementById('duoTotalQuestions').textContent = data.total_questions;
    document.getElementById('duoCurrentQuestion').textContent = data.current_question;
    
    updateDuoPlayers(data.players);
    displayDuoQuestion(data.question_data);
});

socket.on('duo_answer_received', function(data) {
    console.log('✔️ Réponse reçue de:', data.player_name);
    
    // ✅ VÉRIFIER SI C'EST LE JOUEUR COURANT QUI A RÉPONDU
    const isCurrentPlayer = (request.sid === data.player_sid); 
    
    // ❌ NON - utiliser sessionStorage à la place
    let myPlayerId = sessionStorage.getItem('myPlayerId');
    const isMe = (myPlayerId === data.player_sid);
    
    console.log(`Est-ce moi ? ${isMe}`);
    
    // ✅ DÉSACTIVER SEULEMENT SI C'EST MOI QUI AI RÉPONDU
    if (isMe) {
        const submitBtn = document.getElementById('duoSubmitBtn');
        if (submitBtn) {
            submitBtn.innerHTML = '<i class="fas fa-hourglass-start me-2"></i>En attente...';
            submitBtn.disabled = true;
        }
    }
    
    const feedback = document.getElementById('duoFeedback');
    if (feedback) {
        feedback.innerHTML = `
            <div style="
                text-align: center;
                padding: 2rem;
                background: linear-gradient(135deg, rgba(6, 168, 125, 0.1) 0%, rgba(6, 168, 125, 0.05) 100%);
                border-radius: 12px;
                border-left: 5px solid #06A77D;
                margin-top: 1.5rem;
            ">
                <i class="fas fa-check-circle" style="
                    font-size: 2rem;
                    color: #06A77D;
                    display: block;
                    margin-bottom: 0.8rem;
                    animation: bounce 0.6s infinite;
                "></i>
                <p style="color: #06A77D; font-weight: 600; margin: 0;">
                    ${data.player_name} a répondu !
                </p>
                <p style="color: ${isMe ? '#E63946' : '#0066CC'}; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                    ${isMe ? 
                        '⏳ En attente de l\'autre joueur...' : 
                        '👉 C\'est à vous de répondre !'}
                </p>
            </div>
        `;
    }
    
    // ✅ DÉSACTIVER SEULEMENT SI C'EST MOI QUI AI RÉPONDU
    if (isMe) {
        disableAllAnswerButtons();
    }
});

socket.on('duo_next_question', function(data) {
    console.log('➡️ Question suivante duo:', data);
    
    // Attendre 2 secondes avant d'afficher la prochaine
    setTimeout(() => {
        // Nettoyer le feedback
        const feedback = document.getElementById('duoFeedback');
        if (feedback) {
            feedback.innerHTML = '';
        }
        
        // ✅ RÉINITIALISER LE BOUTON
        const submitBtn = document.getElementById('duoSubmitBtn');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-check-circle me-2"></i>Valider';
        }
        
        // Mettre à jour le numéro de question
        const questionNum = document.getElementById('duoCurrentQuestion');
        if (questionNum) {
            questionNum.textContent = data.current_question;
        }
        
        // Mettre à jour la barre de progression
        const percentage = (data.current_question / data.total_questions) * 100;
        const progressBar = document.getElementById('duoProgressBar');
        if (progressBar) {
            progressBar.style.width = percentage + '%';
        }
        
        // Mettre à jour les joueurs
        updateDuoPlayers(data.players);
        
        // Afficher la nouvelle question
        displayDuoQuestion(data.question_data);
        
        console.log(`✅ Question ${data.current_question}/${data.total_questions} affichée`);
    }, 2000);
});

socket.on('duo_game_completed', function(data) {
    console.log('🏆 Partie duo terminée');
    showDuoResults(data.results);
});

socket.on('player_disconnected', function(data) {
    console.log('👋 Adversaire déconnecté');
    showAlert('Votre adversaire a quitté la partie', 'warning');
    document.getElementById('duoGameSection').style.display = 'none';
    document.getElementById('startSection').style.display = 'block';
});

// ========================================
// FONCTIONS QUIZ SOLO
// ========================================

function selectDifficulty(level) {
    quizState.difficulty = level;
    document.querySelectorAll('.difficulty-btn').forEach(btn => btn.classList.remove('active'));
    event.target.closest('.difficulty-btn').classList.add('active');
}

function selectMode(mode) {
    quizState.mode = mode;
    document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
    event.target.closest('.mode-btn').classList.add('active');
    
    const diffSection = document.getElementById('difficultySection');
    const duoSection = document.getElementById('duoActionSection');
    
    if (mode === 'solo') {
        diffSection.style.display = 'block';
        duoSection.style.display = 'none';
    } else {
        diffSection.style.display = 'none';
        duoSection.style.display = 'block';
    }
}

function startSoloQuiz() {
    quizState.sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    socket.emit('start_quiz', {
        session_id: quizState.sessionId,
        difficulty: quizState.difficulty
    });
}

function displayDuoQuestion(questionData) {
    const container = document.getElementById('duoQuestionContainer');
    
    container.innerHTML = `
        <div class="hero-info fade-enter">
            <i class="fas fa-user-circle"></i>
            <div>
                <strong>À propos de:</strong> ${questionData.hero_name}
            </div>
        </div>
        <div class="question-text">${questionData.question}</div>
        <div class="quiz-options">
            <button class="quiz-option" onclick="selectDuoAnswer(this, 'A')">
                <span class="option-label">A</span>
                <span>${questionData.options.A}</span>
            </button>
            <button class="quiz-option" onclick="selectDuoAnswer(this, 'B')">
                <span class="option-label">B</span>
                <span>${questionData.options.B}</span>
            </button>
            <button class="quiz-option" onclick="selectDuoAnswer(this, 'C')">
                <span class="option-label">C</span>
                <span>${questionData.options.C}</span>
            </button>
            <button class="quiz-option" onclick="selectDuoAnswer(this, 'D')">
                <span class="option-label">D</span>
                <span>${questionData.options.D}</span>
            </button>
        </div>
        <div class="text-center mt-4">
            <button class="btn btn-warning btn-lg" id="duoSubmitBtn" onclick="submitDuoAnswer()" disabled style="min-width: 200px;">
                <i class="fas fa-check-circle me-2"></i>Valider
            </button>
        </div>
        <div id="duoFeedback" style="margin-top: 1.5rem;"></div>
    `;
    
    // ✅ RÉINITIALISER L'ÉTAT
    quizState.selectedAnswer = null;
}

function selectAnswer(button, answer) {
    document.querySelectorAll('.quiz-option').forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');
    quizState.selectedAnswer = answer;
    document.getElementById('submitBtn').disabled = false;
}

function submitAnswer() {
    if (!quizState.selectedAnswer) return;
    
    socket.emit('submit_answer', {
        session_id: quizState.sessionId,
        answer: quizState.selectedAnswer
    });
}

function updateProgress(current, total) {
    const percentage = (current / total) * 100;
    document.getElementById('progressBar').style.width = percentage + '%';
    document.getElementById('currentQuestion').textContent = current;
}

function showQuizSection() {
    document.getElementById('startSection').style.display = 'none';
    document.getElementById('quizSection').style.display = 'block';
}

function showAnswerFeedback(isCorrect, correctAnswer) {
    const buttons = document.querySelectorAll('.quiz-option');
    buttons.forEach(btn => {
        const answer = btn.querySelector('.option-label').textContent;
        if (answer === correctAnswer) {
            btn.classList.add('correct');
        } else if (btn.classList.contains('selected') && !isCorrect) {
            btn.classList.add('incorrect');
        }
        btn.disabled = true;
        btn.classList.add('disabled');
    });
}

function disableAllAnswerButtons() {
    document.querySelectorAll('.quiz-option').forEach(btn => {
        btn.disabled = true;
        btn.classList.add('disabled');
    });
}

function showResults(score, total, percentage, answers) {
    document.getElementById('quizSection').style.display = 'none';
    document.getElementById('resultsSection').style.display = 'block';
    
    document.getElementById('finalScore').textContent = `${score}/${total}`;
    document.getElementById('finalPercentage').textContent = `${percentage.toFixed(1)}%`;
    
    let message = '';
    if (percentage === 100) {
        message = '🏆 Parfait! Vous êtes un expert!';
    } else if (percentage >= 80) {
        message = '⭐ Excellent travail!';
    } else if (percentage >= 60) {
        message = '👍 Bien joué!';
    } else {
        message = '📚 À bientôt pour une nouvelle tentative!';
    }
    document.getElementById('scoreMessage').textContent = message;
    
    let detailsHTML = '';
    answers.forEach((answer, index) => {
        const statusClass = answer.is_correct ? 'correct' : 'incorrect';
        const statusIcon = answer.is_correct ? 'fa-check-circle' : 'fa-times-circle';
        
        detailsHTML += `
            <div class="result-item ${statusClass}">
                <i class="fas ${statusIcon}"></i>
                <div>
                    <strong>Question ${index + 1}: ${answer.is_correct ? 'Correcte' : 'Incorrecte'}</strong>
                </div>
            </div>
        `;
    });
    
    document.getElementById('detailedResults').innerHTML = detailsHTML;
    window.scrollTo({top: 0, behavior: 'smooth'});
}

// ========================================
// FONCTIONS QUIZ DUO
// ========================================

function createDuoGame() {
    const playerName = prompt('Quel est votre pseudo?') || `Joueur_${Math.random().toString(36).substr(2, 5)}`;
    if (!playerName) return;
    
    socket.emit('create_duo_game', {
        difficulty: quizState.difficulty,
        player_name: playerName.trim()
    });
}

function joinDuoGamePrompt() {
    const gameCode = prompt('Entrez le code de la partie:')?.toUpperCase().trim();
    if (!gameCode) return;
    
    const playerName = prompt('Quel est votre pseudo?') || `Joueur_${Math.random().toString(36).substr(2, 5)}`;
    if (!playerName) return;
    
    socket.emit('join_duo_game', {
        game_id: gameCode,
        player_name: playerName.trim()
    });
}

function displayDuoQuestion(questionData) {
    const container = document.getElementById('duoQuestionContainer');
    
    container.innerHTML = `
        <div class="hero-info fade-enter">
            <i class="fas fa-user-circle"></i>
            <div>
                <strong>À propos de:</strong> ${questionData.hero_name}
            </div>
        </div>
        <div class="question-text">${questionData.question}</div>
        <div class="quiz-options">
            <button class="quiz-option" onclick="selectDuoAnswer(this, 'A')">
                <span class="option-label">A</span>
                <span>${questionData.options.A}</span>
            </button>
            <button class="quiz-option" onclick="selectDuoAnswer(this, 'B')">
                <span class="option-label">B</span>
                <span>${questionData.options.B}</span>
            </button>
            <button class="quiz-option" onclick="selectDuoAnswer(this, 'C')">
                <span class="option-label">C</span>
                <span>${questionData.options.C}</span>
            </button>
            <button class="quiz-option" onclick="selectDuoAnswer(this, 'D')">
                <span class="option-label">D</span>
                <span>${questionData.options.D}</span>
            </button>
        </div>
        <div class="text-center mt-4">
            <button class="btn btn-warning btn-lg" id="duoSubmitBtn" onclick="submitDuoAnswer()" disabled>
                <i class="fas fa-check-circle me-2"></i>Valider
            </button>
        </div>
        <div id="duoFeedback"></div>
    `;
}

function selectDuoAnswer(button, answer) {
    document.querySelectorAll('.quiz-option').forEach(btn => btn.classList.remove('selected'));
    button.classList.add('selected');
    quizState.selectedAnswer = answer;
    document.getElementById('duoSubmitBtn').disabled = false;
}

function submitDuoAnswer() {
    if (!quizState.selectedAnswer) {
        showAlert('Veuillez sélectionner une réponse', 'error');
        return;
    }
    
    // Afficher un message de chargement
    const submitBtn = document.getElementById('duoSubmitBtn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Envoi en cours...';
    
    socket.emit('submit_duo_answer', {
        game_id: duoGameState.gameId,
        answer: quizState.selectedAnswer
    });
    
    quizState.selectedAnswer = null;
}

function updateDuoPlayers(players) {
    const html = players.map(p => `
        <div class="duo-player-badge">
            <strong>${p.name}</strong>
            <span class="score" style="font-size: 1.3rem; color: #FFD700; font-weight: 700; display: block; margin-top: 0.5rem;">
                ${p.score} pts
            </span>
            <span style="
                font-size: 0.8rem;
                color: #06A77D;
                background: rgba(6, 168, 125, 0.1);
                padding: 0.3rem 0.6rem;
                border-radius: 5px;
                margin-top: 0.5rem;
                display: inline-block;
            ">
                ✅ Prêt
            </span>
        </div>
    `).join('');
    
    const container = document.getElementById('duoPlayersDisplay');
    if (container) {
        container.innerHTML = html;
    }
}

function showDuoResults(results) {
    document.getElementById('duoGameSection').style.display = 'none';
    document.getElementById('duoPodiumSection').style.display = 'block';
    
    const podium = document.getElementById('duoPodium');
    const medals = ['🥇', '🥈', '🥉'];
    
    let html = '';
    results.forEach((result, index) => {
        html += `
            <div class="text-center" style="flex: 1;">
                <div style="font-size: 3rem;">${medals[index] || '🎖️'}</div>
                <div style="background: linear-gradient(135deg, #FFD700, #FFC700); 
                            color: white; padding: 1.5rem; border-radius: 12px; margin: 1rem;">
                    <h4 style="margin: 0; font-weight: 700;">${result.name}</h4>
                    <div style="font-size: 1.8rem; font-weight: 700; margin: 0.5rem 0;">${result.score}/${result.total}</div>
                    <div style="font-size: 1.1rem;">${result.percentage}%</div>
                </div>
            </div>
        `;
    });
    
    podium.innerHTML = html;
}

function leaveQuiz() {
    if (confirm('Êtes-vous sûr de vouloir quitter?')) {
        location.reload();
    }
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert-custom alert-${type}`;
    alertDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <div>${message}</div>
    `;
    alertDiv.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => alertDiv.remove(), 300);
    }, 4000);
}

// ========================================
// STYLES MANQUANTS
// ========================================


// Ajouter les animations CSS
const animationStyle = document.createElement('style');
animationStyle.textContent = `
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
    }
`;
document.head.appendChild(animationStyle);
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(400px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideOutRight {
        from { opacity: 1; transform: translateX(0); }
        to { opacity: 0; transform: translateX(400px); }
    }
    
    .duo-player-badge {
        background: #f8f9fa;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        border: 2px solid #FFD700;
        text-align: center;
        min-width: 150px;
        margin: 0.5rem;
        display: inline-block;
    }
    
    .duo-player-badge strong {
        display: block;
        margin-bottom: 0.5rem;
        color: #1a1a1a;
    }
    
    .duo-player-badge .score {
        font-size: 1.3rem;
        color: #FFD700;
        font-weight: 700;
    }
    
    .fade-enter {
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(style);