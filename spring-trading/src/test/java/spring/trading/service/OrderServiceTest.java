package spring.trading.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Commit;
import org.springframework.transaction.annotation.Transactional;
import spring.trading.domain.Member;
import spring.trading.domain.order.OrderDTO;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.assertj.core.api.Assertions;
import spring.trading.domain.order.OrderDTO;
import spring.trading.domain.order.OrderFactory;
import spring.trading.repository.RequestRepository;


@SpringBootTest
class OrderServiceTest {

    @Autowired
    private RequestRepository requestRepository;

    @Autowired
    private ContextWithOrder contextWithOrder = new ContextWithOrder(requestRepository);

    @Autowired
    private OrderService orderService =new OrderService(contextWithOrder);

    private String requestID;
    private final long ID =111;
    private final String orderId ="13479402";
    private Member member;

    @BeforeEach
    void init() {

        try {
            member = new Member();
            member.setId(ID);
            member.setPublickey(PrivateConfig.TESTNET_API_KEY);
            member.setSecretkey(PrivateConfig.TESTNET_SECRET_KEY);

        }catch(Exception e){
            System.out.println(e.getMessage());
        }

    }


    public void newOrder() {
        String requestID;

        try {

            OrderDTO order = new OrderDTO();
            order.setSide("BUY");
            order.setType("MARKET");
            order.setQuantitiy(0.001);
            order.setSymbol("BTCUSDT");
            order.setTimeInForce("GTC");
            order.setTrailingDelta(500);
            order.setPrice(50000.0);




            OrderFactory orderFactory = new OrderFactory();
            order= orderFactory.createOrder(order);
            requestID= orderService.newOrder(order ,member);

            System.out.println("id : "+requestID +" order pushed");
            Thread.sleep(3000);

            Assertions.assertThat(contextWithOrder.getRequestResult(requestID)).isEqualTo("SUCCESS");
            requestID = orderService.newOrder(order,member);
            System.out.println("id : "+requestID +" order pushed");
            Thread.sleep(3000);

        }catch (Exception e){
            System.out.println(e);
        }
    }


    @Test
    public void newOcoOrder() {
        String requestID;

        try {

            OrderDTO order = new OrderDTO();
            order.setSide("BUY");
            order.setType("OCO");
            order.setQuantitiy(0.0001);
            order.setSymbol("BTCUSDT");
            order.setTimeInForce("GTC");
            order.setTrailingDelta(500);
            order.setPrice(10000.0);
            ;

            contextWithOrder.setMessageArriveListner(request_id -> {
                Assertions.assertThat(contextWithOrder.getRequestResult(request_id)).isEqualTo("FAIL");
                System.out.println("TEST TEST TEST");
            });

            OrderFactory orderFactory = new OrderFactory();
            order= orderFactory.createOrder(order);

            requestID= orderService.newOcoOrder(order ,member);
            System.out.println("id : "+requestID +" order pushed");
            Thread.sleep(3000);

//            Assertions.assertThat(contextWithOrder.getRequestResult(requestID)).isEqualTo("SUCCESS");
            requestID = orderService.newOcoOrder(order,member);
            System.out.println("id : "+requestID +" order pushed");
            Thread.sleep(3000);

        }catch (Exception e){
            System.out.println(e);
        }
    }


    public void getOpenOrders() {

        try{
            String requestId =orderService.getOpenOrders(member);
            Thread.sleep(3000);
            Assertions.assertThat(contextWithOrder.getRequestResult(requestId)).isEqualTo("SUCCESS");
        }catch (Exception e){
            System.out.println(e);
        }

    }

    public void cancelALLOrder() {
        try{
            String requestID =orderService.cancelAllOrder(member,"BTCUSDT");
            Assertions.assertThat(contextWithOrder.getRequestResult(requestID)).isEqualTo("SUCCESS");
        }catch(Exception e){
            System.out.println(e);
        }
    }


    public void cancelOrder() {
        try{
            String requestID =orderService.cancelOrder(member,orderId,"BTCUSDT");
            Assertions.assertThat(contextWithOrder.getRequestResult(requestID)).isEqualTo("SUCCESS");
        }catch(Exception e){
            System.out.println(e);
        }
    }

    public void getAccoountStatus(){
        try{
            String requestID=orderService.getAccountStatus(member);
            Assertions.assertThat(contextWithOrder.getRequestResult(requestID)).isEqualTo("SUCCESS");
        }catch(Exception e){
            System.out.println(e);
        }
    }



}