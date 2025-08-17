from flask import Flask, render_template, request, jsonify
from data_processing import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_rep', methods=['POST'])
def check_rep():
    wallet_address = request.form['wallet_address']
    result = calc_rep(wallet_address)

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

