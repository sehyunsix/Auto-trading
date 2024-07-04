package spring.trading.service;

import com.binance.connector.client.enums.DefaultUrls;
import com.binance.connector.client.impl.WebSocketApiClientImpl;
import com.binance.connector.client.utils.signaturegenerator.HmacSignatureGenerator;
import spring.trading.domain.Member;
import spring.trading.domain.Order;
import org.json.JSONObject;

import java.sql.Timestamp;
import java.util.HashMap;


public class OrderService {
    private static final double quantity = 0.01;

    private HashMap<Long,WebSocketApiClientImpl> connectClientMap = new HashMap<>();
    private HashMap<String,String> orderMap = new HashMap<>();
    private HashMap<String, JSONObject> resultMap = new HashMap<>();

    public void saveResult(String message){
        JSONObject result = new JSONObject(message);
        resultMap.put(result.getString("id"),result);
    }

    public void checkSuccess(String message){
        try {
            JSONObject result = new JSONObject(message);

            if (result.getInt("status") == 200) {
                orderMap.put(result.getString("id"),"SUCCESS");
                saveResult(message);
            }
            else{
                orderMap.put(result.getString("id"),"FAIL");
            }

        } catch (org.json.JSONException e) {
            throw e;
        }

    }

    public static String makeRequestID(){
        Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        return Integer.toString(timestamp.hashCode());
    }

    public void connect(Member member) throws InterruptedException {
        String privateKey = member.getSecretkey();
        String publickey = member.getPublickey();

        HmacSignatureGenerator signatureGenerator = new HmacSignatureGenerator(privateKey);

        WebSocketApiClientImpl client = new WebSocketApiClientImpl(publickey, signatureGenerator, DefaultUrls.TESTNET_WS_API_URL);
        //call back function
        client.connect(((message) -> {
            System.out.println(message);
            checkSuccess(message);
        }));
        connectClientMap.put(member.getId(), client );

    }
    public String newOrder(Order order , Long memberID) throws InterruptedException {

        String requestID = makeRequestID();

        JSONObject params = new JSONObject();
        params.put("requestId", requestID);
        params.put("quantity", quantity);

        if (order.getType().equals("LIMIT")){
            params.put("price",order.getPrice());
            params.put("timeInForce",order.getTimeInForce());
        }

        WebSocketApiClientImpl client = connectClientMap.get(memberID);

        orderMap.put(requestID, "PUSH");


        client.trade().newOrder(order.getStock(), order.getSide(), order.getType(), params);
        Thread.sleep(1000);
        return requestID;
    }

    public String getOpenOrders(Long memberID) throws InterruptedException {

        String requestId = makeRequestID();
        WebSocketApiClientImpl client = connectClientMap.get(memberID);
        JSONObject params = new JSONObject();
        params.put("requestId", requestId);
        orderMap.put(requestId, "PUSH");
        client.trade().getOpenOrders(params);
        Thread.sleep(1000);

        return requestId;
    }

    public String cancelAllOrder(Long memberID) throws InterruptedException {

        String requestId = makeRequestID();
        WebSocketApiClientImpl client = connectClientMap.get(memberID);
        JSONObject params = new JSONObject();
        params.put("requestId", requestId);
        orderMap.put(requestId, "PUSH");
        client.trade().cancelAllOpenOrders("BTCUSDT",params);
        Thread.sleep(10000);
        return requestId;

    }

    public String cancelOrder(Long memberID ,String orderId) throws InterruptedException {
        String requestId = makeRequestID();
        WebSocketApiClientImpl client = connectClientMap.get(memberID);
        JSONObject params = new JSONObject();
        params.put("requestId", requestId);
        params.put("orderId", orderId);
        orderMap.put(requestId, "PUSH");
        client.trade().cancelOrder("BTCUSDT",params);
        Thread.sleep(10000);
        return requestId;

    }
    public void closeConnect(Long memberID) throws InterruptedException {

         WebSocketApiClientImpl client =connectClientMap.get(memberID);
         client.close();
    }

    public String getResult(String ID) {
        return orderMap.get(ID);
    }

    public String getOrderID(String requestId){
        return resultMap.get(requestId).getString("orderId");

    }

    public String getAccountStatus(Long memberID) throws InterruptedException {
        String requestId = makeRequestID();
        WebSocketApiClientImpl client = connectClientMap.get(memberID);
        JSONObject params = new JSONObject();
        params.put("requestId", requestId);

        orderMap.put(requestId, "PUSH");
        client.account().accountStatus(params);
        Thread.sleep(10000);

        return requestId;
    }

}

