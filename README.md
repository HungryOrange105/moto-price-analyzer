# Moto Price Analyzer

Парсер мотоциклов с Drom.ru + модель предсказания рыночной цены на основе CatBoost.

## Описание

Проект собирает объявления о продаже мотоциклов, сохраняет их в PostgreSQL и обучает модель которая предсказывает справедливую рыночную цену по характеристикам мотоцикла. Помогает находить выгодные объявления где цена ниже рыночной.

## Стек

- **Парсинг:** Python, BeautifulSoup4, Requests
- **Данные:** PostgreSQL, SQLAlchemy, Pandas
- **Модель:** CatBoost, Scikit-learn
- **Визуализация:** Matplotlib, Seaborn

## Структура проекта
```
moto_project/
├── parser/
│   └── drom.py          # Парсер Drom.ru
├── data/
│   ├── database.py      # Работа с PostgreSQL
│   └── motos_drom.csv   # Сырые данные
├── model/
│   └── train.py         # Обучение модели
└── README.md
```
## Результаты моделей
### catboost
| Метрика | Значение |
|---|---|
| MAE | 120,123 ₽ |
| R² | 0.852 |
### LightGBM
| Метрика | Значение |
|---|---|
| MAE | 122,303 ₽ |
| R² | 0.789 |
### Random Forest
| Метрика | Значение |
|---|---|
| MAE | 225,459 ₽ |
| R² | 0.375 |

## Ключевые выводы

- Объём двигателя — главный фактор цены (41.5% важности)
- Год выпуска на втором месте (30.1%)
- Эндуро и питбайки значительно дешевле стритфайтеров и круизеров

## Запуск bash
# Установка зависимостей
pip install -r requirements.txt

# Парсинг данных
python parser/drom.py

# Обучение модели
python model/train_catboost.py
python model/train_LGBM.py
python model/train_rand_forest.py

## Зависимости
```
requests
beautifulsoup4
lxml
pandas
sqlalchemy
psycopg2-binary
catboost
lightgbm
scikit-learn
joblib
```
## Data analyze
![Correlation Heatmap](images/heatmap.png)
![Correlation Heatmap](images/boxplot.png)
![Correlation Heatmap](images/scatter.png)