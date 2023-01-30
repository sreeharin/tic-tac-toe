import logging
from flask import Flask, render_template

logging.basicConfig(
        filename='ttt-client.log', level=logging.DEBUG,
        format="%(asctime)s  %(levelname)s : %(message)s"
        ) 

app = Flask(__name__)
app.config['DEBUG'] = True

app.logger.info('Starting tic tac toe client')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/host')
def host():
    return render_template('host.html')

@app.route('/game')
def game():
    return render_template('game.html')