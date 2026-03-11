import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sqlalchemy import create_engine
import joblib

engine = create_engine('postgresql://hungryorange@localhost:5432/motos_db')
df = pd.read_sql('SELECT * FROM motos', engine)

x = df[['name', 'year', 'moto_type', 'volume', 'distance', 'fuel']]
y = df['price']
x_train, x_test,y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=52) 

for col in ['name', 'moto_type', 'fuel']:
    x_train[col] = x_train[col].astype('category')
    x_test[col] = x_test[col].astype('category')


model= LGBMRegressor(n_estimators=400,learning_rate=0.01,num_leaves=20, min_child_samples=1)

model.fit(x_train,y_train)

joblib.dump(model, 'model/lgbm.pkl')

# print(f'r2: {r2_score(y_test, model.predict(x_test))}')
# print(f'mse: {mean_squared_error(y_test, model.predict(x_test))}')
# print(f'mae: {mean_absolute_error(y_test, model.predict(x_test))}')
