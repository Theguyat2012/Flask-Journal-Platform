from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from flask_socketio import send
from journal_platform import socketio, db
from journal_platform.models import Chat, Message

chats = Blueprint('chats', __name__)


@socketio.on('message')
def handle_message(json):
    send(json, broadcast=True)

@socketio.on("send_message")
def send_message(json):
    message = Message(content=json['message'], user_id=json['user_id'], chat_id=json['chat_id'])
    db.session.add(message)
    db.session.commit()

@chats.route('/chat')
def list():
    # FIXME: Rework the list of chats
    if current_user.is_authenticated:
        chat_list = Chat.query.filter(Chat.chat_users.any(id=current_user.id))
        return render_template('chats/list.html', chat_list=chat_list)

    return redirect(url_for('main.index'))

@chats.route('/chat/<int:chat_id>')
def chat(chat_id):
    # FIXME: Rework the individual chat page
    if current_user.is_authenticated:
        chat = Chat.query.filter_by(id=chat_id).first()
        if chat is not None and current_user in chat.chat_users:
            messages = chat.messages
            chat_users = chat.chat_users
            return render_template('chats/chat.html', chat=chat, messages=messages, chat_users=chat_users)
        return redirect(url_for('chats.list'))

    return redirect(url_for('main.index'))
