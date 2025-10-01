package com.bachelorlabs.ports;

import java.util.Objects;
import java.util.Optional;

/**
 * Представление результата сканирования порта
 */
public final class PortScanResult {
    private final int port;
    private final String serviceName;

    /**
     * Создает результат сканирования порта в виде объекта.
     *
     * @param port        номер порта
     * @param serviceName имя сервиса, если известно, иначе null
     */
    public PortScanResult(int port, String serviceName) {
        this.port = port;
        this.serviceName = serviceName;
    }

    /**
     * Возвращает номер порта.
     *
     * @return номер порта
     */
    public int getPort() {
        return port;
    }

    /**
     * Возвращает имя сервиса, если оно известно.
     *
     * @return Optional с именем сервиса или пустой Optional, если сервис неизвестен
     */
    public Optional<String> getServiceName() {
        return Optional.ofNullable(serviceName); // Optional для подписывания известных сервисов
    }

    /**
     * Override для удобного логирования и отладки.
     *
     * @return строковое представление объекта
     */
    @Override
    public String toString() {
        return "PortScanResult{" +
                "port=" + port +
                ", serviceName='" + serviceName + '\'' +
                '}';
    }

    /**
     * Override для сравнения экхемпляров объекта PortScanResult.
     *
     * @param o объект для сравнения
     * @return true, если объекты равны, иначе false
     */
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

    /**
     * Override для корректной работы equals и hashCode.
     *
     * @return хэш-код объекта
     */
    @Override
    public int hashCode() {
        return Objects.hash(port, serviceName);
    }
}
