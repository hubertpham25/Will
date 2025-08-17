#hubert
from flask import Flask, render_template, request, jsonify
from data_processing import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/check_reputation", methods=["POST"])
def check_reputation():
    wallet_address = request.form.get("wallet_address")
    
    reputation_score = calc_rep(wallet_address)

    return jsonify(
        reputation_score
    )

if __name__ == "__main__":
    app.run(debug=True)

