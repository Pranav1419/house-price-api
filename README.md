# House Price Prediction API

A REST API built with **FastAPI** that predicts house prices using a trained **linear regression** model. Every prediction is saved to a **MySQL** database, and the saved history can be listed, fetched, and deleted through the API. The project is containerised with **Docker**.

```
Client -> FastAPI -> input validation (Pydantic) -> ML model -> save to MySQL -> JSON response
```

## Features

- Predict a house price from five input features
- Automatic input validation with clear `422` errors for bad data
- Model loaded once at startup (FastAPI `lifespan`), not on every request
- Every prediction stored in MySQL with a timestamp
- History endpoints with pagination (`limit` and `skip`)
- Interactive API docs generated automatically at `/docs`
- Dockerfile for running the app in a container

## Tech stack

| Area | Tool |
|---|---|
| API framework | FastAPI, Uvicorn |
| Validation | Pydantic |
| ML model | scikit-learn (Linear Regression), joblib |
| Database | MySQL, SQLAlchemy, PyMySQL |
| Configuration | python-dotenv |
| Containers | Docker |

## Project structure

```
house-price-api/
├── app/
│   ├── main.py            # app creation, startup (model loading), router registration
│   ├── database.py        # MySQL engine, session, get_db dependency
│   ├── models.py          # SQLAlchemy table (prediction log)
│   ├── schemas.py         # Pydantic request and response models
│   ├── ml.py              # model loading and prediction logic
│   └── router/
│       ├── predict.py     # POST /predict
│       └── history.py     # /predictions endpoints
├── tests/
├── houseprice.joblib      # trained model
├── requirements.txt
├── Dockerfile
├── .env.example           # template for environment variables
└── .gitignore
```

## Input features

| Field | Type | Allowed range |
|---|---|---|
| `Area_sqft` | float | greater than 0, up to 100000 |
| `Bedrooms` | integer | 1 to 10 |
| `Bathrooms` | integer | 1 to 10 |
| `Age_years` | integer | 0 to 100 |
| `Distance_city_km` | float | 0 to 1000 |

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/predict` | Predict a price and save it to the database |
| GET | `/predictions` | List saved predictions, newest first (`?limit=10&skip=0`) |
| GET | `/predictions/{id}` | Get one saved prediction (404 if not found) |
| DELETE | `/predictions/{id}` | Delete a saved prediction and return a confirmation message |

### POST /predict: example request

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Area_sqft": 1200,
    "Bedrooms": 3,
    "Bathrooms": 2,
    "Age_years": 10,
    "Distance_city_km": 5
  }'
```

### POST /predict: example response

The values below are illustrative and will differ with your trained model.

```json
{
  "Area_sqft": 1200,
  "Bedrooms": 3,
  "Bathrooms": 2,
  "Age_years": 10,
  "Distance_city_km": 5,
  "predicted_price": 5234000.0
}
```

### POST /predict: invalid input

If a value is outside the allowed range or a field is missing, the API rejects the request with a `422` error before the model runs.

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Area_sqft": 1200, "Bedrooms": 50, "Bathrooms": 2, "Age_years": 10, "Distance_city_km": 5}'
```

The response names the field that failed (here `Bedrooms`) and the rule it broke.

### GET /predictions: list with query parameters

`limit` sets how many records to return (1 to 100, default 10) and `skip` sets how many to skip from the start (default 0). Results are newest first.

```bash
curl "http://127.0.0.1:8000/predictions?limit=2&skip=0"
```

Example response (values are illustrative):

```json
[
  {
    "id": 2,
    "area_sqft": 1500.0,
    "bedrooms": 3,
    "bathrooms": 2,
    "age_years": 5,
    "distance_city_km": 8.0,
    "predicted_price": 6120000.0,
    "created_at": "2026-10-15T12:40:10"
  },
  {
    "id": 1,
    "area_sqft": 1200.0,
    "bedrooms": 3,
    "bathrooms": 2,
    "age_years": 10,
    "distance_city_km": 5.0,
    "predicted_price": 5234000.0,
    "created_at": "2026-10-15T12:34:56"
  }
]
```

To get the next page, use `?limit=2&skip=2`. A `limit` above 100 returns a `422` error.

### GET /predictions/{id}: get one prediction

```bash
curl http://127.0.0.1:8000/predictions/1
```

This returns a single record in the same format as above. If the id does not exist, the API returns `404`:

```json
{
  "detail": "Prediction not found"
}
```

### DELETE /predictions/{id}: delete a prediction

```bash
curl -X DELETE http://127.0.0.1:8000/predictions/1
```

Response when the record exists:

```json
{
  "detail": "Prediction with id 1 deleted successfully"
}
```

Response when the id does not exist (`404`):

```json
{
  "detail": "Prediction not found"
}
```

## Getting started (local)

### Prerequisites

- Python 3.11 or newer
- MySQL server running locally

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/Pranav1419/house-price-api.git
cd house-price-api

python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

python -m pip install -r requirements.txt
```

### 2. Create the database

```sql
CREATE DATABASE house_price_db CHARACTER SET utf8mb4;
```

The table itself is created automatically when the app starts.

### 3. Configure environment variables

Copy `.env.example` to `.env` and fill in your own values:

```
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=house_price_db
```

The `.env` file is ignored by Git and must never be committed.

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs to try the endpoints.

## Running with Docker

```bash
docker build -t house-price-api .
docker run -p 8000:8000 --env-file .env -e DB_HOST=host.docker.internal house-price-api
```

Inside a container, `localhost` refers to the container itself, so `DB_HOST` is set to `host.docker.internal` to reach MySQL running on your own computer (Docker Desktop on Windows or macOS). Your MySQL user must be allowed to connect from outside `localhost`.

## Notes and limitations

- The model is a linear regression, so predictions are only reliable for inputs inside the range of the training data. Very small or unusual inputs can produce unrealistic results. Negative predictions are returned as `0`.
- The input limits above are general bounds. Tightening them to the minimum and maximum of the training data would reject out-of-range inputs more strictly.
- Authentication is not enabled, since the API has no user accounts. Before exposing it publicly, add an API key check.

## Possible improvements

- API key authentication
- Filter predictions by price (`min_price` query parameter)
- Batch prediction endpoint
- Automated tests with pytest and `TestClient`
- Database migrations with Alembic
- Deployment to a cloud platform with a hosted database

## Author

Pranav