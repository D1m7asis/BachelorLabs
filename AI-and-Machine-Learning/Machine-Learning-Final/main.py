import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

data = pd.read_csv("risk_factors_cervical_cancer.csv")
# Замена символов '?' на NaN
data.replace("?", np.nan, inplace=True)

# Преобразование столбцов в числовые
data = data.apply(pd.to_numeric, errors='ignore')

# Целевая переменная
target = "Dx:Cancer"

# Удаление пустых строк
data.dropna(how='all', inplace=True)

# Разделение на признаки и целевую переменную
X = data.drop(columns=[target])
y = data[target].fillna(0).astype(int)  # Заменяем пропуски в целевой переменной на 0

# Разделение наборов на тренировочный и тестовый
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Пайплайн для обработки данных и обучения модели
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),  # Заполнение пропусков
    ('scaler', StandardScaler()),  # Нормализация
    ('svc', SVC(probability=True))  # Модель SVM
])

# Перечень для подбора гиперпараметров
param_grid = {
    'svc__C': [0.1, 1, 10, 100],
    'svc__kernel': ['linear', 'rbf'],
    'svc__gamma': ['scale', 'auto']
}

# GridSearchCV для поиска лучших гиперпараметров
grid_search = GridSearchCV(pipeline, param_grid, scoring='roc_auc', cv=5, n_jobs=1, verbose=3)  # При n_jobs=-1 возможны зависания
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_

# Оценка модели
y_pred_proba = best_model.predict_proba(X_test)[:, 1]
roc_auc = roc_auc_score(y_test, y_pred_proba)

# Вывод результатов
print("Лучшая модель:", grid_search.best_params_)
print(f"ROC AUC на тестовой выборке: {roc_auc:.4f}")
