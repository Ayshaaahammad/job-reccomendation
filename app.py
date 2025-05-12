
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

app = Flask(__name__)

# Load the pre-trained KMeans model
model = pickle.load(open('kmeans_model.pkl', 'rb'))

def load_and_clean_data(file_path):
    retail = pd.read_csv(file_path, sep=",", encoding="ISO-8859-1", header=0)
    retail['CustomerID'] = retail['CustomerID'].astype(str)
    retail['Amount'] = retail['Quantity'] * retail['UnitPrice']

    rfm_m = retail.groupby('CustomerID')['Amount'].sum().reset_index()
    rfm_f = retail.groupby('CustomerID')['InvoiceNo'].count().reset_index()
    retail['InvoiceDate'] = pd.to_datetime(retail['InvoiceDate'], format='%d-%m-%Y %H:%M')
    max_date = max(retail['InvoiceDate'])
    retail['Diff'] = max_date - retail['InvoiceDate']
    rfm_p = retail.groupby('CustomerID')['Diff'].min().reset_index()
    rfm_p['Diff'] = rfm_p['Diff'].dt.days

    rfm = pd.merge(rfm_m, rfm_f, on='CustomerID', how='inner')
    rfm = pd.merge(rfm, rfm_p, on='CustomerID', how='inner')
    rfm.columns = ['CustomerID', 'Amount', 'Frequency', 'Recency']

    Q1 = rfm.quantile(0.05)
    Q3 = rfm.quantile(0.95)
    IQR = Q3 - Q1
    rfm = rfm[(rfm['Amount'] >= Q1['Amount'] - 1.5 * IQR['Amount']) & (rfm['Amount'] <= Q3['Amount'] + 1.5 * IQR['Amount'])]
    rfm = rfm[(rfm['Recency'] >= Q1['Recency'] - 1.5 * IQR['Recency']) & (rfm['Recency'] <= Q3['Recency'] + 1.5 * IQR['Recency'])]
    rfm = rfm[(rfm['Frequency'] >= Q1['Frequency'] - 1.5 * IQR['Frequency']) & (rfm['Frequency'] <= Q3['Frequency'] + 1.5 * IQR['Frequency'])]

    return rfm

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file and file.filename.endswith('.csv'):
        file_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(file_path)

        rfm_data = load_and_clean_data(file_path)
        X = rfm_data[['Amount', 'Frequency', 'Recency']]
        scaled_X = StandardScaler().fit_transform(X)
        predictions = model.predict(scaled_X)
        rfm_data['Cluster'] = predictions

        return jsonify(rfm_data.to_dict(orient='records'))

    return jsonify({"error": "Invalid file format. Only CSV files are allowed."})

if __name__ == '__main__':
    app.run(debug=True)
