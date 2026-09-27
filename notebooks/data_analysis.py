import pandas as pd

# Load dataset
df = pd.read_csv("data/fake_job_postings.csv")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nDataset information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nFraudulent job counts:")
print(df["fraudulent"].value_counts())
# Fill missing text values
text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits"
]

for col in text_columns:
    df[col] = df[col].fillna("")

# Combine important text columns into one column
df["combined_text"] = (
    df["title"] + " " +
    df["company_profile"] + " " +
    df["description"] + " " +
    df["requirements"] + " " +
    df["benefits"]
)

print("\nCombined text sample:")
print(df["combined_text"].head())

print("\nMissing values in selected text columns:")
print(df[text_columns].isnull().sum())
from sklearn.model_selection import train_test_split

# Input
X = df["combined_text"]

# Output / target
y = df["fraudulent"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining data size:")
print(X_train.shape)

print("\nTesting data size:")
print(X_test.shape)

print("\nTraining target distribution:")
print(y_train.value_counts())

print("\nTesting target distribution:")
print(y_test.value_counts())
from sklearn.feature_extraction.text import TfidfVectorizer

# Create TF-IDF converter
tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

# Learn vocabulary from training data and convert it to numbers
X_train_tfidf = tfidf.fit_transform(X_train)

# Convert testing data using the same vocabulary
X_test_tfidf = tfidf.transform(X_test)

print("\nTF-IDF completed successfully!")

print("\nTraining TF-IDF shape:")
print(X_train_tfidf.shape)

print("\nTesting TF-IDF shape:")
print(X_test_tfidf.shape)

print("\nSome words learned by TF-IDF:")
print(tfidf.get_feature_names_out()[:20])
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Create Logistic Regression model
model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

# Train model
model.fit(X_train_tfidf, y_train)

# Predict on testing data
y_pred = model.predict(X_test_tfidf)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Training Completed!")

print("\nAccuracy:")
print(accuracy)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
# Test model with a new job posting

new_job = """
Work from home and earn $5000 every week.
No experience required.
No interview needed.
Immediate joining.
Pay a registration fee to start working.
"""

# Convert new job text using the SAME TF-IDF
new_job_tfidf = tfidf.transform([new_job])

# Prediction
prediction = model.predict(new_job_tfidf)[0]

# Probability
probability = model.predict_proba(new_job_tfidf)[0]

print("\n--- New Job Prediction ---")

if prediction == 1:
    print("Result: FAKE / SUSPICIOUS JOB")
else:
    print("Result: LIKELY LEGITIMATE JOB")

print("Legitimate probability:", round(probability[0] * 100, 2), "%")
print("Fraud probability:", round(probability[1] * 100, 2), "%")
import joblib

# Save trained model
joblib.dump(model, "model/job_scam_model.pkl")

# Save TF-IDF vectorizer
joblib.dump(tfidf, "model/tfidf_vectorizer.pkl")

print("\nModel and TF-IDF vectorizer saved successfully!")
