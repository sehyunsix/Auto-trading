package spring.trading.service;

import com.binance.connector.client.impl.WebSocketStreamClientImpl;
import com.binance.connector.client.utils.websocketcallback.WebSocketMessageCallback;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import spring.trading.domain.Member;

public class StreamingServiceTest {
    private Member member;
    WebSocketMessageCallback webSocketMessageCallback =(message)->{
        System.out.println(message);
    };


    @BeforeEach
    void init() {

        try {
            member = new Member();
            member.setPublickey(PrivateConfig.TESTNET_API_KEY);
            member.setSecretkey(PrivateConfig.TESTNET_SECRET_KEY);

        }catch(Exception e){
            System.out.println(e.getMessage());
        }

    }

    @Test
    public void streaming() throws InterruptedException {
        WebSocketStreamClientImpl client = new WebSocketStreamClientImpl();
        client.tradeStream("btcusdt",webSocketMessageCallback);
        Thread.sleep(10000000);
    }
}
