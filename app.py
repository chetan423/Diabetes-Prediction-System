from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Load the trained model
with open('trained_model.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

# Define recommendations
recommendations = {
    1: "You're in a normal state. Maintain a healthy lifestyle with regular exercise and a balanced diet. <a href='https://www.focusphysiotherapy.com/how-to-maintain-a-healthy-lifestyle/' target='_blank'>Maintain it properly for a healthy life</a>.",
    2: "You're showing symptoms of prediabetes. Regular monitoring, a healthy diet, and some medication may help. <a href='https://my.clevelandclinic.org/health/diseases/21498-prediabetes' target='_blank'>Contact a doctor</a>.",
    3: "You have diabetes. It's recommended to follow a strict treatment plan including insulin therapy, regular monitoring, and medical checkups. You must have to contact the Doctor. <a href='https://diabetesjournals.org/care/article/45/Supplement_1/S244/138924/16-Diabetes-Care-in-the-Hospital-Standards-of' target='_blank'>Contact a doctor</a>."
}

# Define labels for predictions
prediction_labels = {
    1: "Normal",
    2: "Have Symptoms",
    3: "Have Diabetes"
}


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Predict and recommend
@app.route('/predict', methods=['POST'])
def predict():
    # Extract data from the form
    Age = float(request.form['Age'])
    Gender = int(request.form['Gender'])  # 0 for male, 1 for female
    BMI = float(request.form['BMI'])
    BloodPressure = float(request.form['BloodPressure'])
    Glucose = float(request.form['Glucose'])
    Insulin = float(request.form['Insulin'])
    FamilyHistory = int(request.form['FamilyHistory'])
    PhysicalActivity = int(request.form['PhysicalActivity'])
    Cholesterol = float(request.form['Cholesterol'])
    HbA1c = float(request.form['HbA1c'])


    # Create the input data array
    input_data = np.array([[Age, Gender, BMI, BloodPressure, Glucose, Insulin, FamilyHistory, PhysicalActivity,
                            Cholesterol, HbA1c]])

    # Predict using the loaded model
    prediction = model.predict(input_data)[0]

    # Get label and recommendation based on the prediction
    prediction_text = prediction_labels[prediction]
    recommendation = recommendations[prediction]

    return render_template('result.html', prediction=prediction_text, recommendation=recommendation)


if __name__ == '__main__':
    app.run(debug=True)
