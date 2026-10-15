from app import ml

ml.load_model()
print(ml.predict_price({ "Area_sqft": 2921, "Bedrooms": 1, "Bathrooms": 2,"Age_years" : 25, "Distance_city_km": 4}))