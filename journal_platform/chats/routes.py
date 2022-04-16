from flask import Blueprint, render_template
from flask_login import current_user
from flask_socketio import send
from journal_platform import socketio, db
from journal_platform.models import Chat, Message

chats = Blueprint('chats', __name__)


@socketio.on("send_message")
def send_message(json):
    print("hello")
    print(json)
    print(json['message'])
    print(json['chat_id'])
    send(json['message'])
    message = Message(content=json['message'], user_id=current_user.id, chat_id=json['chat_id'])
    db.session.add(message)
    db.session.commit()

@chats.route('/chat')
def chat_list():
    chat_list = Chat.query.filter(Chat.chat_users.any(id=current_user.id))
    return render_template('chats/chat_list.html', chat_list=chat_list)

@chats.route('/chat/<int:chat_id>')
def chat(chat_id):
    # TODO: load chat messages
    chat = Chat.query.filter_by(id=chat_id).first()
    messages = chat.messages
    chat_users = chat.chat_users

    return render_template('chats/chat.html', chat=chat, messages=messages, chat_users=chat_users)
    # return render_template('chats/chat.html')
