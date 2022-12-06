# import time
#
# from flask import render_template
# from flask_socketio import send
#
# # from app import socketio
# from __init__ import socketio
#
# # socketio = SocketIO(auction)
#
#
# @socketio.on('message')
# def handle_message(msg):
#     print('message: ' + msg)
#     # send price offer if auction is not end
#     send(msg, broadcast=True)
# from app import app
#
# # app.config['SECRET_KEY'] = 'mysecret'
# # socketio = SocketIO(app)
#
# # @socketio.on('message')
# # def handleMessage(msg):
# # 	print('Message: ' + msg)
# # 	send(msg, broadcast=True)
#
#
# # @app.route('/')
# # def index():
# #     return render_template('index.html')
# #
# #
# # @socketio.on('connect', namespace='/')
# # def ws_conn():
# #     socketio.emit('msg', {'count': 1}, namespace='/')
#
#
# # @socketio.on('message', namespace='/auction/bidding')
# # def bidding(price):
# #     send(price)
# #     return
#
#
# def timer(t):
#     for i in range(t):
#         time.sleep(1)
#         yield str(i)
