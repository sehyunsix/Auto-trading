package spring.trading.service;

import com.binance.connector.client.enums.DefaultUrls;
import com.binance.connector.client.impl.WebSocketApiClientImpl;
import com.binance.connector.client.utils.signaturegenerator.HmacSignatureGenerator;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.web.client.HttpMessageConvertersRestClientCustomizer;
import org.springframework.stereotype.Component;
import spring.trading.domain.Member;
import spring.trading.domain.order.OrderDTO;
import org.json.JSONObject;

import java.sql.Timestamp;
import java.util.HashMap;


@Component
public class OrderService {


    private ContextWithOrder contextWithOrder;

    @Autowired
    public OrderService(ContextWithOrder contextWithOrder) {
        this.contextWithOrder = contextWithOrder;
    }
    public static String makeRequestID(){
        Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        return Integer.toString(timestamp.hashCode());
    }


    public String newOrder(OrderDTO order , Member member) throws InterruptedException {
      String requestId = contextWithOrder.orderWithContext(((client, params) -> {
          client.trade().newOrder(order.getSymbol(), order.getSide(), order.getType(),order.getParams().put("requestId",params.get("requestId")));
      }), member );
        return requestId;
    }

    public String newOcoOrder(OrderDTO order , Member member) throws InterruptedException {
        String requestId = contextWithOrder.orderWithContext(((client, params) -> {
            client.trade().newOcoOrder(order.getSymbol(), order.getSide(), order.getPrice(), order.getQuantitiy(),order.getParams().put("requestId",params.get("requestId")));
        }), member );
        return requestId;
    }


    public String getOpenOrders(Member member) throws InterruptedException {

        String requestId = contextWithOrder.orderWithContext(((client, params) -> {client.trade().getOpenOrders(params);}), member ); ;
        return requestId;
    }

    public String cancelAllOrder(Member member ,String symbol) throws InterruptedException {

        String requestId = contextWithOrder.orderWithContext((client, params)-> {client.trade().cancelAllOpenOrders(symbol,params);}, member);
        return requestId;
    }

    public String cancelOrder(Member member ,String orderId ,String symbol) throws InterruptedException {

        String requestId = contextWithOrder.orderWithContext(((client, params) -> {
            params.put("orderId", orderId);
            client.trade().cancelOrder(symbol,params);}),member);

        return requestId;

    }



    public String getAccountStatus(Member member ) throws InterruptedException {

        String requestId = contextWithOrder.orderWithContext(((client, params) -> client.account().accountStatus(params)),
                member);
        return requestId;
    }



}

