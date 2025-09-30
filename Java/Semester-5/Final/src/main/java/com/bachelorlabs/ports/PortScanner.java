package com.bachelorlabs.ports;

import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * Performs TCP port scanning on the provided host.
 */
public class PortScanner {
    private final Duration timeout;

    public PortScanner(Duration timeout) {
        this.timeout = Objects.requireNonNull(timeout, "timeout");
    }

    public List<PortScanResult> scan(String host, int startPort, int endPort) throws HostResolutionException {
        InetAddress address = resolveHost(host);
        int tasks = endPort - startPort + 1;
        int threads = Math.min(Math.max(Runtime.getRuntime().availableProcessors() * 2, 4), 200);
        threads = Math.min(threads, tasks);
        if (threads <= 0) {
            threads = 1;
        }

        ExecutorService executor = Executors.newFixedThreadPool(threads);
        try {
            List<Future<PortScanResult>> futures = new ArrayList<>();
            for (int port = startPort; port <= endPort; port++) {
                final int currentPort = port;
                futures.add(executor.submit(createScanTask(address, currentPort)));
            }

            List<PortScanResult> openPorts = new ArrayList<>();
            for (Future<PortScanResult> future : futures) {
                try {
                    PortScanResult result = future.get();
                    if (result != null) {
                        openPorts.add(result);
                    }
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                } catch (ExecutionException e) {
                    // Ignore the port if scanning failed unexpectedly.
                }
            }

            Collections.sort(openPorts, (a, b) -> Integer.compare(a.getPort(), b.getPort()));
            return openPorts;
        } finally {
            executor.shutdownNow();
        }
    }

    private Callable<PortScanResult> createScanTask(InetAddress address, int port) {
        return () -> {
            try (Socket socket = new Socket()) {
                socket.connect(new InetSocketAddress(address, port), (int) timeout.toMillis());
                String serviceName = PortServiceRegistry.findService(port).orElse(null);
                return new PortScanResult(port, serviceName);
            } catch (IOException ignored) {
                return null;
            }
        };
    }

    private InetAddress resolveHost(String host) throws HostResolutionException {
        try {
            return InetAddress.getByName(host);
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
