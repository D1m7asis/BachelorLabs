package com.bachelorlabs.ports;

import java.util.Objects;
import java.util.Optional;

/**
 * Показывает, что получилось при сканировании одного порта
 */
public final class PortScanResult {
    private final int port;
    private final String serviceName;

    public PortScanResult(int port, String serviceName) {
        this.port = port;
        this.serviceName = serviceName;
    }

    public int getPort() {
        return port;
    }

    public Optional<String> getServiceName() {
        return Optional.ofNullable(serviceName); // Решил не заставлять всех знать сервис, поэтому он опциональный
    }

    @Override
    public String toString() {
        return "PortScanResult{" +
                "port=" + port +
                ", serviceName='" + serviceName + '\'' +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof PortScanResult that)) {
            return false;
        }
        return port == that.port && Objects.equals(serviceName, that.serviceName);
    }

    @Override
    public int hashCode() {
        return Objects.hash(port, serviceName);
    }
}
