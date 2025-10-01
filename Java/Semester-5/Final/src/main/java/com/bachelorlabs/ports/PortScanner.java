package com.bachelorlabs.ports;

import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.Socket;
import java.net.UnknownHostException;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * TCP-сканер с параллельной проверкой портов
 */
public class PortScanner {
    private final Duration timeout;

    /**
     * Создает сканер с заданным таймаутом подключения.
     *
     * @param timeout время ожидания подключения к порту
     * @throws NullPointerException     если timeout равен null
     * @throws IllegalArgumentException если timeout отрицателен или равен нулю
     */
    public PortScanner(Duration timeout) {
        this.timeout = Objects.requireNonNull(timeout, "timeout"); // Защита от NPE

        if (timeout.isNegative() || timeout.isZero()) {
            throw new IllegalArgumentException("Timeout must be positive");
        }
    }

    /**
     * Сканирует указанный диапазон портов на заданном хосте.
     *
     * @param host      имя хоста для сканирования
     * @param startPort начальный порт диапазона (включительно)
     * @param endPort   конечный порт диапазона (включительно)
     * @return список PortScanResult для открытых портов
     * @throws HostResolutionException если хост не найден или недоступен
     */
    public List<PortScanResult> scan(String host, int startPort, int endPort) throws HostResolutionException {
        InetAddress[] addresses = resolveAll(host);
        int portsToCheck = endPort - startPort + 1;
        int threadCount = Math.min(Math.max(Runtime.getRuntime().availableProcessors(), 1), portsToCheck); // Ограничим количество потоков для защиты от падения на малом количестве портов

        try (ExecutorService executor = Executors.newFixedThreadPool(threadCount)) { // Для автоматического закрытия пула
            List<Future<PortScanResult>> futures = new ArrayList<>(portsToCheck);
            for (int port = startPort; port <= endPort; port++) {
                final int currentPort = port;
                futures.add(executor.submit(() -> buildResultIfOpen(addresses, currentPort)));
            }

            List<PortScanResult> results = new ArrayList<>();
            for (Future<PortScanResult> future : futures) { // Собираем результаты
                try {
                    PortScanResult result = future.get();
                    if (result != null) {
                        results.add(result);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                } catch (ExecutionException ignored) {
                    // Порт закрыт или недоступен
                }
            }
            return results;
        }
    }

    /**
     * Строит результат сканирования порта, если он открыт.
     *
     * @param addresses массив IP-адресов для проверки
     * @param port      порт для проверки
     * @return PortScanResult если порт открыт, иначе null
     */
    private PortScanResult buildResultIfOpen(InetAddress[] addresses, int port) {
        if (!isPortReachable(addresses, port)) {
            return null; // Чтобы потом просто отсеять закрытые порты по null
        }

        return new PortScanResult(port, PortServiceRegistry.findService(port).orElse(null));
    }

    /**
     * Проверяет, доступен ли хотя бы один из указанных IP-адресов на заданном порту.
     *
     * @param addresses массив IP-адресов для проверки
     * @param port      порт для проверки
     * @return true если хотя бы один адрес доступен на указанном порту, иначе false
     */
    private boolean isPortReachable(InetAddress[] addresses, int port) {
        for (InetAddress address : addresses) {
            if (tryConnect(address, port)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Пытается подключиться к указанному адресу и порту с заданным таймаутом.
     * Если подключение успешно, возвращает true, иначе false.
     *
     * @param address IP-адрес для подключения
     * @param port    порт для подключения
     * @return true если подключение успешно, иначе false
     */
    private boolean tryConnect(InetAddress address, int port) {
        try (Socket socket = new Socket(Proxy.NO_PROXY)) {  // Решил отключить прокси т.к. из-за них багалось корректное отображение портов
            socket.connect(new InetSocketAddress(address, port), (int) timeout.toMillis());
            return socket.isConnected();
        } catch (IOException ignored) {
            return false;
        }
    }

    /**
     * Ищет все IP-адреса для указанного хоста.
     *
     * @param host имя хоста для разрешения
     * @return массив InetAddress хоста
     * @throws HostResolutionException если хост не найден или недоступен
     */
    private InetAddress[] resolveAll(String host) throws HostResolutionException {
        try {
            return InetAddress.getAllByName(host);
        } catch (UnknownHostException e) {
            throw new HostResolutionException("Хост недоступен или не существует", e);
        }
    }

    /**
     * Ошибка разрешения хоста
     *
     * @see PortScanner#resolveAll(String)
     */
    public static class HostResolutionException extends Exception {
        public HostResolutionException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}
