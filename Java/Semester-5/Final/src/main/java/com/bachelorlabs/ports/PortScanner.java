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
 * TCP-сканер, который проверяет порты параллельно.
 */
public class PortScanner {
    private final Duration timeout;

    public PortScanner(Duration timeout) {
        this.timeout = Objects.requireNonNull(timeout, "timeout"); // Решил перестраховаться от null, чтобы таймаут всегда был задан
    }

    public List<PortScanResult> scan(String host, int startPort, int endPort) throws HostResolutionException {
        InetAddress[] addresses = resolveAll(host);
        int portsToCheck = endPort - startPort + 1;
        int threadCount = Math.min(Math.max(Runtime.getRuntime().availableProcessors(), 1), portsToCheck); // Решил ограничить количество потоков, чтобы машина не ушла в ступор при маленьком диапазоне

        ExecutorService executor = Executors.newFixedThreadPool(threadCount); // Решил запустить пул, чтобы порты проверялись параллельно и без лишних сложностей
        try {
            List<Future<PortScanResult>> futures = new ArrayList<>(portsToCheck);
            for (int port = startPort; port <= endPort; port++) {
                final int currentPort = port;
                futures.add(executor.submit(() -> buildResultIfOpen(addresses, currentPort))); // Решил каждую задачу завернуть в Future, так проще собирать результаты
            }

            List<PortScanResult> results = new ArrayList<>();
            for (Future<PortScanResult> future : futures) {
                try {
                    PortScanResult result = future.get();
                    if (result != null) {
                        results.add(result);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break; // Решил прервать цикл, чтобы не зависнуть при остановке сканирования
                } catch (ExecutionException ignored) {
                    // Решил не пугать пользователя стеком, нам важен только факт, что порт закрыт или недоступен
                }
            }
            return results;
        } finally {
            executor.shutdown(); // Решил мягко остановить пул, чтобы не держать ресурсы лишними
        }
    }

    private PortScanResult buildResultIfOpen(InetAddress[] addresses, int port) {
        if (!isPortReachable(addresses, port)) {
            return null; // Решил вернуть null, чтобы потом просто отсеять закрытые порты
        }
        return new PortScanResult(port, PortServiceRegistry.findService(port).orElse(null));
    }

    private boolean isPortReachable(InetAddress[] addresses, int port) {
        for (InetAddress address : addresses) {
            if (tryConnect(address, port)) {
                return true;
            }
        }
        return false;
    }

    private boolean tryConnect(InetAddress address, int port) {
        try (Socket socket = new Socket(Proxy.NO_PROXY)) {  // Решил отключить прокси т.к. из-за них багалось корректное отображение портов
            socket.connect(new InetSocketAddress(address, port), (int) timeout.toMillis());
            return socket.isConnected();
        } catch (IOException ignored) {
            return false;
        }
    }

    private InetAddress[] resolveAll(String host) throws HostResolutionException {
        try {
            return InetAddress.getAllByName(host);
        } catch (UnknownHostException e) {
            throw new HostResolutionException("Хост недоступен или не существует", e);
        }
    }

    public static class HostResolutionException extends Exception {
        public HostResolutionException(String message, Throwable cause) {
            super(message, cause);
        }
    }
}
