from socket import socket
from journal_platform import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, debug=True)
