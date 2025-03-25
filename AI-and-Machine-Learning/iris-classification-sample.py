# Импорт необходимых библиотек
from sklearn.neighbors import KNeighborsClassifier
import sklearn.datasets as datasets
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import label_binarize
from itertools import cycle

# Загрузка данных Iris
iris = datasets.load_iris()
X, Y = iris.data, iris.target

# Разделение данных на тренировочные и тестовые
X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.05, random_state=42)

# Создание модели взвешенного KNN
model = KNeighborsClassifier(n_neighbors=5, weights='distance')  # weights='distance' включает взвешивание

# Обучение модели
model.fit(X_train, y_train)

# Предсказание на тестовых данных
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)  # Вероятности для каждого класса

# Применение PCA для уменьшения размерности до 2D
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# Визуализация тренировочных данных
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_train_pca[:, 0], y=X_train_pca[:, 1], hue=y_train, palette='viridis', s=100)
plt.title('Train Data Visualization (2D PCA)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title="Classes", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Визуализация тестовых данных с предсказаниями
plt.figure(figsize=(10, 6))
# Истинные классы
sns.scatterplot(x=X_test_pca[:, 0], y=X_test_pca[:, 1], hue=y_test, palette='viridis', s=100, marker='o', legend='full')
# Предсказанные классы
sns.scatterplot(x=X_test_pca[:, 0], y=X_test_pca[:, 1], hue=y_pred, palette='cool', s=200, marker='X', legend='full')
plt.title('Test Data Visualization with Predictions (2D PCA)')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.legend(title="Classes", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Матрица ошибок
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=iris.target_names, yticklabels=iris.target_names)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Отчет о классификации
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

# Построение ROC-AUC кривой для многоклассовой классификации
# Бинаризация меток для многоклассового ROC-AUC
y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
n_classes = y_test_bin.shape[1]

# Вычисление ROC-AUC для каждого класса
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_pred_proba[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Визуализация ROC-AUC кривой для каждого класса
plt.figure(figsize=(8, 6))
colors = cycle(['blue', 'red', 'green'])
for i, color in zip(range(n_classes), colors):
    plt.plot(fpr[i], tpr[i], color=color, lw=2,
             label='ROC curve of class {0} (area = {1:0.2f})'
             ''.format(iris.target_names[i], roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=2)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC-AUC for Multi-Class Classification')
plt.legend(loc="lower right")
plt.show()