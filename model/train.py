import pandas as pd
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os
from sqlalchemy import create_engine

engine = create_engine('postgresql://hungryorange@localhost:5432/motos_db')

df = pd.read_sql('SELECT * FROM motos', engine)

x = df[['name', 'year', 'moto_type', 'volume', 'distance', 'fuel']]
y = df['price']
x_train, x_test,y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=52) 

features = ['name', 'moto_type', 'fuel']
model =CatBoostRegressor(iterations=350, learning_rate=0.1)
model.fit(x_train, y_train, cat_features=features)

model.save_model('model/catboost_model.cbm')

print(f'mae: {mean_absolute_error(y_test, model.predict(x_test))}')
print(f'mse: {mean_squared_error(y_test, model.predict(x_test))}')
print(f'r2: {r2_score(y_test, model.predict(x_test))}')



# 'name', 'year', 'moto_type', 'place', 'volume', 'distance', 'fuel'
# my_moto = pd.Series({
#     'name': 'Suzuki SV 650',
#     'year': 1998,
#     'moto_type': 'Классический мотоцикл',
#     'volume': 650,
#     'distance': 40,
#     'fuel': 'бензин'
# })
# y_pred = model.predict(my_moto)

# print(y_pred)
