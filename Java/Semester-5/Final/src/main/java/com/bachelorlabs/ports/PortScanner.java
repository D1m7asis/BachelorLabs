package com.bachelorlabs.ports;

import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.Socket;
import java.net.UnknownHostException;
import java.time.Duration;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
 * TCP-сканер, который проверяет порты параллельно.
 */
public class PortScanner {
    private final Duration timeout;

    public PortScanner(Duration timeout) {
        this.timeout = Objects.requireNonNull(timeout, "timeout");
    }

    public List<PortScanResult> scan(String host, int startPort, int endPort) throws HostResolutionException {
        InetAddress[] addresses = resolveAll(host);

        return IntStream.rangeClosed(startPort, endPort)
                .parallel()
                .mapToObj(port -> isPortReachable(addresses, port)
                        ? new PortScanResult(port, PortServiceRegistry.findService(port).orElse(null))
                        : null)
                .filter(Objects::nonNull)
                .collect(Collectors.toList());
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
        try (Socket socket = new Socket(Proxy.NO_PROXY)) {  // Решил отключить прокси т.к. из-за них багалось корректное отобржение портов
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
