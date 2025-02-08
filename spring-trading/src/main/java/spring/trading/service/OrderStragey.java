package spring.trading.service;

import com.binance.connector.client.impl.WebSocketApiClientImpl;
import org.json.JSONObject;

public interface OrderStragey {

    public void makeOrder(WebSocketApiClientImpl client, JSONObject params) throws InterruptedException;
}
