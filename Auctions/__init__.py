import time

from flask import Flask, Blueprint, render_template, Response

from app import app, socketio

auction = Blueprint("auction", __name__)

app.register_blueprint(auction)
socketio.init_app(app)

from Auctions import WebSockets
