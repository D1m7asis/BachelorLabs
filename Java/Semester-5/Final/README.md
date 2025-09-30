# Сканер TCP-портов

Проект: консольная утилита на Java для проверки открытых TCP-портов.

## Условия
- Требуется Java 11+.
- Внешние библиотеки не применяются.

## Сборка
```bash
cd Java/Semester-5/Final
javac -d out $(find src -name "*.java")
```

## Запуск
```bash
java -cp out com.bachelorlabs.ports.PortScannerApp
```

## Команды
- `scan <хост> <начальный_порт> <конечный_порт>` — запускает проверку диапазона.
- `help` — выводит памятку по управлению.
- `quit` — завершает программу.

## Пример
```
> scan example.com 80 443
Открытые порты на хосте example.com:
+ 80 (HTTP)
+ 443 (HTTPS)
```
