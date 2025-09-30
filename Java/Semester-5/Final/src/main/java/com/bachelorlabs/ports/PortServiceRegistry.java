package com.bachelorlabs.ports;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * Provides human-readable names for common TCP ports.
 */
public final class PortServiceRegistry {
    private static final Map<Integer, String> PORT_SERVICES;

    static {
        Map<Integer, String> services = new HashMap<>();
        services.put(20, "FTP (Data)");
        services.put(21, "FTP");
        services.put(22, "SSH");
        services.put(23, "Telnet");
        services.put(25, "SMTP");
        services.put(53, "DNS");
        services.put(67, "DHCP (Server)");
        services.put(68, "DHCP (Client)");
        services.put(69, "TFTP");
        services.put(80, "HTTP");
        services.put(110, "POP3");
        services.put(123, "NTP");
        services.put(143, "IMAP");
        services.put(161, "SNMP");
        services.put(389, "LDAP");
        services.put(443, "HTTPS");
        services.put(445, "SMB");
        services.put(465, "SMTPS");
        services.put(587, "Submission");
        services.put(636, "LDAPS");
        services.put(993, "IMAPS");
        services.put(995, "POP3S");
        services.put(1433, "MSSQL");
        services.put(1521, "Oracle DB");
        services.put(1723, "PPTP");
        services.put(1883, "MQTT");
        services.put(2049, "NFS");
        services.put(2375, "Docker");
        services.put(3306, "MySQL");
        services.put(3389, "RDP");
        services.put(5432, "PostgreSQL");
        services.put(5900, "VNC");
        services.put(6379, "Redis");
        services.put(8080, "HTTP (Alt)");
        services.put(8443, "HTTPS (Alt)");
        services.put(9000, "SonarQube");
        services.put(9200, "Elasticsearch");
        services.put(11211, "Memcached");
        PORT_SERVICES = Collections.unmodifiableMap(services);
    }

    private PortServiceRegistry() {
    }

    public static Optional<String> findService(int port) {
        return Optional.ofNullable(PORT_SERVICES.get(port));
    }
}
