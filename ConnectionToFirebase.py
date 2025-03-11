import firebase_admin
import numpy as np
from firebase_admin import credentials, firestore,db

from app import model

# Path to your Firebase private key JSON file
cred = credentials.Certificate("credentials.json")

# Initialize Firebase app
firebase_admin.initialize_app(cred, {"databaseURL":"https://diabetes-cd7a0-default-rtdb.firebaseio.com/"})

# Initialize Firestore
db = firestore.client()
# or for Realtime Database
# from firebase_admin import db
# ref = db.reference('/')

def store_prediction_in_firestore(data, prediction, recommendation):
    # Create a document with the patient data and prediction
    doc_ref = db.collection('diabetes_predictions').add({
        'age': data['age'],
        'gender': data['gender'],
        'bmi': data['bmi'],
        'blood_pressure': data['blood_pressure'],
        'glucose': data['glucose_level'],
        'insulin': data['insulin_level'],
        'hba1c': data['hba1c'],
        'diabetes_pedigree': data['diabetes_pedigree'],
        'prediction': prediction,
        'recommendation': recommendation
    })
    print(f"Data stored successfully with ID: {doc_ref[1].id}")

# Example patient data
data = {
    'age': 45,
    'gender': 0,
    'bmi': 25.6,
    'blood_pressure': 120,
    'glucose_level': 85,
    'insulin_level': 15,
    'hba1c': 5.6,
    'diabetes_pedigree': 0.5
}

# Assuming `model` is your trained machine learning model
input_data = [[data['age'], data['gender'], data['bmi'], data['blood_pressure'],
               data['glucose_level'], data['insulin_level'], data['hba1c'], data['diabetes_pedigree']]]
prediction = model.predict(input_data)[0]

# Define a recommendation based on the prediction (Normal = 1, Symptoms = 2, Disease = 3)
recommendations = {
    1: "Maintain a healthy lifestyle with regular exercise and a balanced diet.",
    2: "Regular monitoring, healthy diet, and oral medication may be recommended.",
    3: "Follow a treatment plan including insulin therapy, medical checkups, and lifestyle changes. Contact to the Doctor"
}
recommendation = recommendations[prediction]

# Store the data and prediction in Firestore
store_prediction_in_firestore(data, prediction, recommendation)


def store_prediction_in_realtime_db(data, prediction, recommendation):
    # Reference to the database root
    ref = db.reference('diabetes_predictions')

    # Store the data under a new unique key
    ref.push({
        'age': data['age'],
        'gender': data['gender'],
        'bmi': data['bmi'],
        'blood_pressure': data['blood_pressure'],
        'glucose': data['glucose_level'],
        'insulin': data['insulin_level'],
        'hba1c': data['hba1c'],
        'diabetes_pedigree': data['diabetes_pedigree'],
        'prediction': prediction,
        'recommendation': recommendation
    })
    print("Data stored successfully in Realtime Database")


# Use the same data and prediction logic as above
store_prediction_in_realtime_db(data, prediction, recommendation)
