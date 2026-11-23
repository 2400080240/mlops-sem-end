# Customer Churn Prediction System

## Components
- Streamlit: login, registration and dashboard
- FastAPI: prediction endpoint
- Scikit-learn: Logistic Regression model pipeline
- MLflow: experiment tracking
- DVC: dataset/model pipeline versioning
- Evidently AI: data drift report
- Docker Compose: run API and dashboard in containers
- GitHub Actions: basic CI syntax check

## 1. Prepare the data
Put the Telco customer churn CSV at `data/churn.csv`. It must contain the target column `Churn` with Yes/No values and the customer features used by the dashboard. The script drops `customerID` if present.

## 2. Install and train (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python src/train.py
```

Training creates `models/churn_model.pkl`, `data/reference.csv`, `data/current.csv`, MLflow runs and `reports/metrics.json`.

## 3. Run locally (two terminals)
Terminal 1:
```powershell
uvicorn api.main:app --reload
```
Terminal 2:
```powershell
streamlit run app/app.py
```
Open http://localhost:8501. For local execution the dashboard defaults to `http://localhost:8000`; Docker Compose sets `API_URL=http://api:8000` automatically.

API docs: http://localhost:8000/docs

## 4. MLflow
```powershell
mlflow ui --backend-store-uri ./mlruns
```
Open http://localhost:5000.

## 5. Data drift
```powershell
python monitoring/data_drift.py
```
Open `reports/data_drift_report.html`. The training script creates reference/current split files as a demonstration. For meaningful production drift monitoring, replace `data/current.csv` with newly collected, recent customer data using the same feature schema.

## 6. DVC
Initialize DVC once:
```powershell
dvc init
dvc add data/churn.csv
dvc repro
dvc metrics show
```
Configure a remote before pushing DVC-tracked data:
```powershell
dvc remote add -d storage <YOUR_REMOTE_URL>
dvc push
```
Do not commit private customer data to a public Git repository.

## 7. Docker
First ensure `models/churn_model.pkl` exists:
```powershell
docker compose up --build
```
Open http://localhost:8501. Stop with Ctrl+C, then `docker compose down`.

## Notes
- The initial user database is local SQLite and intended for a classroom demo. Use HTTPS, secure secrets, rate limiting and a production identity provider before real deployment.
- GitHub Actions currently performs a basic compile check; extend it with automated unit/integration tests for a production CI/CD pipeline.
- Docker Compose uses the same image for the API and dashboard, with different commands.
