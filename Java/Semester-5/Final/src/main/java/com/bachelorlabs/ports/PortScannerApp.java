package com.bachelorlabs.ports;

import java.time.Duration;
import java.util.List;
import java.util.Locale;
import java.util.Scanner;

/**
 * Место, где начинается работа приложения для сканирования порта с консоли
 */
public class PortScannerApp {
    private static final int MIN_PORT = 1;
    private static final int MAX_PORT = 65_535;

    public static void main(String[] args) {
        PortScanner scanner = new PortScanner(Duration.ofMillis(1000));
        try (Scanner input = new Scanner(System.in)) {
            System.out.println("Консольный сканер TCP-портов. Введите 'help' для справки.");
            while (true) {
                System.out.print("> ");
                if (!input.hasNextLine()) {
                    break;
                }
                String line = input.nextLine().trim();
                if (line.isEmpty()) {
                    continue;
                }

                String[] tokens = line.split("\\s+");
                String command = tokens[0].toLowerCase(Locale.ROOT);

                switch (command) {
                    case "help":
                        printHelp();
                        break;
                    case "quit":
                        System.out.println("Завершение работы приложения.");
                        return;
                    case "scan":
                        handleScanCommand(scanner, tokens); // Решил вынести обработку сканирования в отдельный метод, чтобы main не разрастался
                        break;
                    default:
                        System.out.println("Неизвестная команда. Введите 'help' для списка команд.");
                        break;
                }
            }
        }
    }

    private static void handleScanCommand(PortScanner scanner, String[] tokens) {
        if (tokens.length != 4) {
            System.out.println("Неверное количество аргументов. Использование: scan <хост> <начальный_порт> <конечный_порт>");
            return;
        }

        String host = tokens[1];
        Integer startPort = parsePort(tokens[2]);
        Integer endPort = parsePort(tokens[3]);

        if (startPort == null || endPort == null) {
            return;
        }

        if (!isValidRange(startPort, endPort)) {
            System.out.println("Некорректный диапазон портов");
            return;
        }

        try {
            List<PortScanResult> openPorts = scanner.scan(host, startPort, endPort);
            printResults(host, openPorts);
        } catch (PortScanner.HostResolutionException e) {
            System.out.println(e.getMessage()); // Решил показать пользователю понятный текст ошибки вместо стека
        }
    }

    private static void printResults(String host, List<PortScanResult> openPorts) {
        if (openPorts.isEmpty()) {
            System.out.println("Нет открытых портов в указанном диапазоне");
            return;
        }

        System.out.println("Открытые порты на хосте " + host + ":");
        for (PortScanResult result : openPorts) {
            StringBuilder line = new StringBuilder("+ ").append(result.getPort());
            result.getServiceName().ifPresent(name -> line.append(" (").append(name).append(")")); // Решил подписывать популярные сервисы, чтобы было понятнее что нашли
            System.out.println(line);
        }
    }

    private static Integer parsePort(String value) {
        try {
            int port = Integer.parseInt(value);
            if (port < MIN_PORT || port > MAX_PORT) {
                System.out.println("Порт должен быть в диапазоне от " + MIN_PORT + " до " + MAX_PORT);
                return null;
            }
            return port;
        } catch (NumberFormatException e) {
            System.out.println("Порт должен быть числом");
            return null;
        }
    }

    private static boolean isValidRange(int startPort, int endPort) {
        return startPort <= endPort;
    }

    private static void printHelp() {
        System.out.println("Доступные команды:");
        System.out.println("  help                         — показать эту справку");
        System.out.println("  scan <хост> <начальный_порт> <конечный_порт> — сканировать диапазон портов");
        System.out.println("  quit                         — выйти из приложения");
        System.out.println();
        System.out.println("Пример: scan example.com 80 443");
    }
}
