# 1. HTML: Понятие, стандарты, тэги и атрибуты

## Найдите и исправьте все ошибки в коде (использованы только изученные элементы). А так же поясните свои исправления. Знать структуру web-страницы пока не обязательно - задание больше на внимательность.

```html

<header>Узнай на все 100 %!</header>
    <section>
        <h1>Языки программирования</h1>
        <figure>
            <img src="https://www.python.org/static/img/python-
        logo.png">
            <figcaption>Логотип Python</figcaption>
        </figure>
        <article>
            <p>Изучать Python очень весело</p>
            <p>Но нужно читать и практиковаться</p>
            <p>И сильно-сильно стараться</p>
        </article>
    </section>
    <nav>
        <a href="#">Главная страница</a><br>
        <a href="#">Раздел 1</a><br>
        <a href="#">Раздел 2</a><br>
    </nav>
    <footer>Успехов в освоении</footer>
```

## Ошибки в первом HTML-коде и их исправления:
1. Тег `<header>` нельзя использовать вне `<body>`, 
нужно обернуть всё содержимое в `<body>`.

2. Тег `<img>` не закрыт и содержит разрыв строки в URL
 
3. Использование `<br>` между ссылками в `<nav>` - лучше использовать `<ul><li>` для лучшей семантики.

4. Отсутствует `<head>` с `<charset>` - возможно некорректное отображение русского текста.

## Исправленный код:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Узнай на все 100 %!</title>
</head>
<body>
    <header>
        <h1>Узнай на все 100 %!</h1>
    </header>

    <section>
        <h2>Языки программирования</h2>
        <figure>
            <img src="https://www.python.org/static/img/python-logo.png" alt="Логотип Python">
            <figcaption>Логотип Python</figcaption>
        </figure>
        <article>
            <p>Изучать Python очень весело.</p>
            <p>Но нужно читать и практиковаться.</p>
            <p>И сильно-сильно стараться.</p>
        </article>
    </section>

    <nav>
        <ul>
            <li><a href="#">Главная страница</a></li>
            <li><a href="#">Раздел 1</a></li>
            <li><a href="#">Раздел 2</a></li>
        </ul>
    </nav>

    <footer>
        <p>Успехов в освоении!</p>
    </footer>
</body>
</html>
```