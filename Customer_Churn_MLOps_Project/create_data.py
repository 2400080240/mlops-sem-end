
import pandas as pd

data = {
    "gender": ["Female", "Male", "Female", "Male", "Male", "Female",
               "Male", "Female", "Male", "Female", "Male", "Female"],
    "SeniorCitizen": [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    "Partner": ["Yes", "No", "Yes", "No", "Yes", "No",
                "Yes", "Yes", "No", "No", "Yes", "No"],
    "Dependents": ["No", "No", "No", "Yes", "Yes", "No",
                   "No", "Yes", "No", "No", "Yes", "No"],
    "tenure": [2, 45, 8, 60, 24, 3, 55, 12, 6, 48, 30, 1],
    "PhoneService": ["Yes"] * 12,
    "MultipleLines": ["No", "Yes", "No", "Yes", "No", "No",
                      "Yes", "No", "Yes", "Yes", "No", "No"],
    "InternetService": ["Fiber optic", "DSL", "Fiber optic", "DSL",
                        "No", "Fiber optic", "DSL", "DSL",
                        "Fiber optic", "No", "DSL", "Fiber optic"],
    "OnlineSecurity": ["No", "Yes", "No", "Yes", "No", "No",
                       "Yes", "Yes", "No", "No", "Yes", "No"],
    "OnlineBackup": ["No", "Yes", "Yes", "No", "No", "No",
                     "Yes", "Yes", "No", "No", "Yes", "No"],
    "DeviceProtection": ["No", "Yes", "No", "Yes", "No", "No",
                         "Yes", "No", "No", "Yes", "Yes", "No"],
    "TechSupport": ["No", "Yes", "No", "Yes", "No", "No",
                    "Yes", "Yes", "No", "Yes", "Yes", "No"],
    "StreamingTV": ["Yes", "No", "Yes", "No", "No", "Yes",
                    "No", "No", "Yes", "No", "No", "Yes"],
    "StreamingMovies": ["Yes", "No", "No", "No", "No", "Yes",
                        "No", "Yes", "Yes", "No", "No", "Yes"],
    "Contract": ["Month-to-month", "Two year", "Month-to-month",
                 "One year", "Two year", "Month-to-month",
                 "One year", "Two year", "Month-to-month",
                 "Two year", "One year", "Month-to-month"],
    "PaperlessBilling": ["Yes", "No", "Yes", "No", "No", "Yes",
                         "No", "No", "Yes", "No", "No", "Yes"],
    "PaymentMethod": ["Electronic check", "Mailed check",
                      "Electronic check", "Bank transfer (automatic)",
                      "Credit card (automatic)", "Electronic check",
                      "Bank transfer (automatic)", "Credit card (automatic)",
                      "Electronic check", "Mailed check",
                      "Bank transfer (automatic)", "Electronic check"],
    "MonthlyCharges": [95.5, 55.2, 89.9, 60.0, 20.0, 99.0,
                       65.0, 50.0, 92.0, 25.0, 70.0, 100.0],
    "TotalCharges": ["191", "2484", "720", "3600", "480", "297",
                     "3575", "600", "552", "1200", "2100", "100"],
    "Churn": ["Yes", "No", "Yes", "No", "No", "Yes",
              "No", "No", "Yes", "No", "No", "Yes"]
}

df = pd.DataFrame(data)
df.to_csv("data/churn.csv", index=False)

print("Sample churn dataset created successfully!")
print("Dataset shape:", df.shape)
print(df.head())
