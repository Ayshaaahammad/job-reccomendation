from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from models.recommendation_model import get_recommendations

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.json
    recommendations = get_recommendations(user_data)
    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)