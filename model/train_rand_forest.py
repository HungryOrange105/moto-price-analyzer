import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sqlalchemy import create_engine
from category_encoders import TargetEncoder
from sklearn.pipeline import Pipeline
import joblib


engine = create_engine('postgresql://hungryorange@localhost:5432/motos_db')

df = pd.read_sql('SELECT * FROM motos', engine)

x = df[['name', 'year', 'moto_type', 'volume', 'distance', 'fuel']]
y = df['price']

x_train, x_test,y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=52) 

te = TargetEncoder(cols=['name', 'moto_type', 'fuel'])
x_train = te.fit_transform(x_train, y_train)
x_test = te.transform(x_test)

pipe = Pipeline([
    ('preprocessor', TargetEncoder(cols=['name', 'moto_type', 'fuel'])),
    ('model', RandomForestRegressor(
        n_estimators=250, 
        max_depth=50, 
        min_samples_leaf=35, 
        max_features='sqrt',
        n_jobs=-1
    ))
])

# model = RandomForestRegressor(n_estimators=250, max_depth=50, min_samples_leaf=35, max_features='sqrt',criterion='absolute_error')

pipe.fit(x_train, y_train)

joblib.dump(pipe, 'model/rf_model.pkl')

# print(f'r2: {r2_score(y_test, pipe.predict(x_test))}')
# print(f'mse: {mean_squared_error(y_test, pipe.predict(x_test))}')
# print(f'mae: {mean_absolute_error(y_test, pipe.predict(x_test))}')

