from catboost import CatBoostRegressor
import pandas as pd

model = CatBoostRegressor()
model.load_model('model/catboost_model.cbm')

# 'name', 'year', 'moto_type', 'volume', 'distance', 'fuel'
my_moto = pd.Series({
    'name': 'Suzuki SV 650',
    'year': 1998,
    'moto_type': 'Классический мотоцикл',
    'volume': 650,
    'distance': 40,
    'fuel': 'бензин'
})

y_pred = model.predict(my_moto)

print(y_pred)