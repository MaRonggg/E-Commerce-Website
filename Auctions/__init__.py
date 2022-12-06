# import time
#
# from flask import Flask, Blueprint, render_template, Response
# from flask_socketio import send
# from app import app, socketio
#
# auction = Blueprint("auction", __name__)
#
# app.register_blueprint(auction)
# #
# # socketio.init_app(app)
#
#
# # @app.route('/hey', methods=['GET'])
# # def page():
# #     return render_template('main_page.html')
#
# # from Auctions import WebSockets
#
# # @auction.on('message', namespace='/auction_page/<product_id>')
# @auction.route("/hey", methods=['GET', 'POST'])
# def auction():
#     return render_template('main_page.html')