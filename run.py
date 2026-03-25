import os
from app import create_app, socketio

if __name__ == '__main__':
    app = create_app()
    
    print("\n" + "="*60)
    print("🚀 DÉMARRAGE DU SERVEUR")
    print("="*60)
    print(f"🌐 URL: http://localhost:5000")
    print(f"🔌 SocketIO: http://localhost:5000/socket.io")
    print(f"🧪 Test SocketIO: http://localhost:5000/socketio-test")
    print("="*60 + "\n")
    
    # Lancer avec SocketIO
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True,
        use_reloader=False  # Éviter les problèmes avec le reloader
    )