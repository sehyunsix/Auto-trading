package spring.trading.service;


import com.binance.connector.client.enums.DefaultUrls;
import com.binance.connector.client.impl.WebSocketApiClientImpl;
import com.binance.connector.client.utils.signaturegenerator.HmacSignatureGenerator;
import com.binance.connector.client.utils.websocketcallback.*;
import jakarta.transaction.Transactional;
import org.jetbrains.annotations.NotNull;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;
import spring.trading.domain.Member;
import spring.trading.domain.Request;
import spring.trading.repository.RequestRepository;

import java.io.IOException;
import java.sql.Timestamp;
import java.util.HashMap;


@Component
public class ContextWithOrder {

    private HashMap<String , Request > requestMap;
//    private HashMap<String ,String> orderMap;
    private final RequestRepository requestRepository;
    private HashMap<Long, WebSocketApiClientImpl> clientConnMap;
    private MessageArriveListner messageArriveListner;

    private WebSocketOpenCallback webSocketOpenCallback= (response )-> {
        System.out.println("open :" +response);
    };
    private WebSocketClosedCallback webSocketClosedCallback = (code, reason) -> {
        System.out.println("closed :"+Integer.toString(code) + reason);
    };
    private WebSocketFailureCallback webSocketFailureCallback = (throwable, response) -> {
        System.out.println("faile :"+ response);
    };

    private WebSocketClosingCallback webSocketClosingCallback = (code, reason) -> {
        System.out.println("closing :"+Integer.toString(code) + reason);

    };

    public ContextWithOrder(RequestRepository requestRepository) {
        requestMap = new HashMap<>();
        this.requestRepository = requestRepository;
        clientConnMap = new HashMap<>();
        messageArriveListner = (event) -> {System.out.println("event: " + event);};
    }

    public void setMessageArriveListner(MessageArriveListner messageArriveListner) {
        this.messageArriveListner = messageArriveListner;
    }

    public void saveResponse(String message){
        System.out.println(message);
        JSONObject result = new JSONObject(message);

        try {
            String requestId = result.getString("id");
            Request request = requestMap.get(requestId);
            System.out.println("requestId: " + requestId);
            if (result.getInt("status") == 200) {

                request.setStatus("SUCCESS");
                requestMap.put(requestId, request);

            }
            else{
                request.setStatus("SUCCESS");
                requestMap.put(requestId, request);
            }
            request.setResult(result);
            requestRepository.save(request);
            messageArriveListner.messageArrived(requestId);

        } catch (org.json.JSONException e) {
            System.out.println("JSONException");
        }

    }

    private WebSocketMessageCallback webSocketMessageCallback = (response) -> {
        saveResponse(response);
    };

    public WebSocketApiClientImpl connect(Member member) throws InterruptedException {
        String privateKey = member.getSecretkey();
        String publickey = member.getPublickey();

        HmacSignatureGenerator signatureGenerator = new HmacSignatureGenerator(privateKey);

        WebSocketApiClientImpl client = new WebSocketApiClientImpl(publickey, signatureGenerator, DefaultUrls.TESTNET_WS_API_URL);
        //call back function
        client.connect( webSocketOpenCallback, webSocketMessageCallback,webSocketClosingCallback, webSocketClosedCallback ,webSocketFailureCallback);
        clientConnMap.put(member.getId(),client);
        System.out.println("put member id");
        return client;

    }

    public String getRequestResult(String requestId){
        return requestMap.get(requestId).getStatus();
    }

    public String makeRequestID(){
        Timestamp timestamp = new Timestamp(System.currentTimeMillis());
        return Integer.toString(timestamp.hashCode());
    }

    public void closeConnect(Long memberID) throws InterruptedException {

        WebSocketApiClientImpl client =clientConnMap.get(memberID);
        client.close();
    }
    public String orderWithContext(OrderStragey orderStragey ,Member member) throws InterruptedException{


        WebSocketApiClientImpl client = clientConnMap.get(member.getId());
        try {
        if (client == null) {
            connect(member);
            Thread.sleep(2000);
            client = clientConnMap.get(member.getId());
        }

            JSONObject params = new JSONObject();
            String requestId = makeRequestID();
            params.put("requestId", requestId);

            Request request =new Request();

            request.setRequestId(requestId);
            request.setMemberId(member.getId());
            requestMap.put(requestId,request);

            orderStragey.makeOrder(client, params);
            return requestId;

        }catch(InterruptedException e){
            throw e;
        }
    }
}
