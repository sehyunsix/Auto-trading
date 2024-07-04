package spring.trading.domain;

import com.binance.connector.client.impl.WebSocketApiClientImpl;

import java.security.Timestamp;

public class Action {
    private WebSocketApiClientImpl apiClient;
    private Order order;
    private Timestamp timestamp;
}
