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

/**
 *  TCP-сканер, который проверяет порты по очереди.
 */
public class PortScanner {
    private final Duration timeout;

    public PortScanner(Duration timeout) {
        this.timeout = Objects.requireNonNull(timeout, "timeout");
    }

    public List<PortScanResult> scan(String host, int startPort, int endPort) throws HostResolutionException {
        InetAddress[] addresses = resolveAll(host);
        List<PortScanResult> openPorts = new ArrayList<>();

        for (int port = startPort; port <= endPort; port++) {
            if (isPortReachable(addresses, port)) {
                String serviceName = PortServiceRegistry.findService(port).orElse(null);
                openPorts.add(new PortScanResult(port, serviceName));
            }
        }

        return openPorts;
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
