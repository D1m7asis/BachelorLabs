package com.bachelorlabs.ports;

import java.util.Map;
import java.util.Optional;

/**
 * Примеры под самые частые порты (для удобства).
 */
public final class PortServiceRegistry {
    private static final Map<Integer, String> PORT_SERVICES;

    static {
        PORT_SERVICES = Map.ofEntries(
                Map.entry(20, "FTP (Data)"),
                Map.entry(21, "FTP"),
                Map.entry(22, "SSH"),
                Map.entry(23, "Telnet"),
                Map.entry(25, "SMTP"),
                Map.entry(53, "DNS"),
                Map.entry(67, "DHCP (Server)"),
                Map.entry(68, "DHCP (Client)"),
                Map.entry(69, "TFTP"),
                Map.entry(80, "HTTP"),
                Map.entry(110, "POP3"),
                Map.entry(123, "NTP"),
                Map.entry(143, "IMAP"),
                Map.entry(161, "SNMP"),
                Map.entry(389, "LDAP"),
                Map.entry(443, "HTTPS"),
                Map.entry(445, "SMB"),
                Map.entry(465, "SMTPS"),
                Map.entry(1433, "MSSQL"),
                Map.entry(1521, "Oracle DB"),
                Map.entry(2375, "Docker"),
                Map.entry(3306, "MySQL"),
                Map.entry(3389, "RDP"),
                Map.entry(5432, "PostgreSQL"),
                Map.entry(6379, "Redis"),
                Map.entry(8080, "HTTP (Alt)"),
                Map.entry(8443, "HTTPS (Alt)"),
                Map.entry(9200, "Elasticsearch"),
                Map.entry(11211, "Memcached")
        );
    }

    private PortServiceRegistry() {
    }

    public static Optional<String> findService(int port) {
        return Optional.ofNullable(PORT_SERVICES.get(port)); // Optional для подписи известных сервисов
    }
}
