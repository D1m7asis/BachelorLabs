# Консольный сканер TCP-портов домена/IP на Java

Небольшая утилита на Java, которая проверяет диапазон TCP-портов и показывает, какие из них открыты.

## Требования
- Java 11 или новее;
- Стандартная библиотека Java.

## 1. Компиляция
Сначала собираем все файлы вместе с точкой входа `PortScannerApp.java`, в котором находится `public static void main`:
```bash
cd Java/Semester-5/Final
javac -d out src/main/java/com/bachelorlabs/ports/PortScannerApp.java src/main/java/com/bachelorlabs/ports/PortScanner.java src/main/java/com/bachelorlabs/ports/PortScanResult.java src/main/java/com/bachelorlabs/ports/PortServiceRegistry.java
```

## 2. Запуск
После компиляции запускаем класс с `main`:
```bash
java -cp out com.bachelorlabs.ports.PortScannerApp
```

## 3. Команды
- `scan <хост> <начальный_порт> <конечный_порт>` — проверить диапазон портов;
- `help` — показать подсказку;
- `quit` — завершить приложение.

## Пример
```
> scan example.com 80 443
Открытые порты на хосте example.com:
+ 80 (HTTP)
+ 443 (HTTPS)
```

Если ничего не найдено, программа выведет: `Нет открытых портов в указанном диапазоне`.
