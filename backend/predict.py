import joblib

# Load saved model
model = joblib.load("model/job_scam_model.pkl")

# Load saved TF-IDF vectorizer
tfidf = joblib.load("model/tfidf_vectorizer.pkl")

# Sample job advertisement
job_text = """
Work from home and earn $5000 every week.
No experience required.
No interview required.
Immediate joining.
Pay registration fee before starting the job.
"""

# Convert text into TF-IDF numbers
job_vector = tfidf.transform([job_text])

# Make prediction
prediction = model.predict(job_vector)[0]

# Get probabilities
probability = model.predict_proba(job_vector)[0]

print("\n--- Job Scam Detection Result ---")

if prediction == 1:
    print("Result: SUSPICIOUS / FRAUDULENT JOB")
else:
    print("Result: LIKELY LEGITIMATE JOB")

print("Legitimate Probability:", round(probability[0] * 100, 2), "%")
print("Fraud Probability:", round(probability[1] * 100, 2), "%")