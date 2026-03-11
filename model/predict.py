from catboost import CatBoostRegressor
import pandas as pd
import  joblib

model_catboost = CatBoostRegressor()
model_catboost.load_model('model/catboost_model.cbm')

model_rf = joblib.load('model/rf_model.pkl')

model_lgbm = joblib.load('model/lgbm.pkl')

# 'name', 'year', 'moto_type', 'volume', 'distance', 'fuel'
my_moto = pd.DataFrame({
    'name': ['Suzuki SV 650'],
    'year': [1998],
    'moto_type': ['Классический мотоцикл'],
    'volume': [650],
    'distance': [30_000],
    'fuel': ['бензин']
})

cat_cols = ['name', 'moto_type', 'fuel']

print('catboost')
print(model_catboost.predict(my_moto)[0])
print('')
print('rf')
print(model_rf.predict(my_moto)[0])
print('')
print('lgbm')
for col in cat_cols:
    my_moto[col] = my_moto[col].astype('category')
print(model_lgbm.predict(my_moto)[0])