#hubert
from flask import Flask, render_template, request, jsonify
from data_processing import *
import time
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/check_reputation", methods=["POST"])
def check_reputation():
    wallet_address = request.form.get("wallet_address")
    
    start_time = time.time()

    reputation_score = calc_rep(wallet_address)

    processing_time = time.time() - start_time
    print(processing_time)
    
    return jsonify(
        reputation_score
    )

if __name__ == "__main__":
    app.run(debug=True)

