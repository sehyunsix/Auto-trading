package spring.trading.service;

import spring.trading.domain.Member;
import spring.trading.domain.Order;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.assertj.core.api.Assertions;

class OrderServiceTest {

    private OrderService orderService =new OrderService();
    private String requestID;
    private final long ID =111;
    private final String orderId ="13479402";

    @BeforeEach
    void init() {

        try {
            Member member = new Member();
            member.setId(ID);
            member.setPublickey(PrivateConfig.TESTNET_API_KEY);
            member.setSecretkey(PrivateConfig.TESTNET_SECRET_KEY);
            orderService.connect(member);
        }catch(Exception e){
            System.out.println(e.getMessage());
        }

    }

    @Test
    public void newOrder() {
        String requestID;

        try {

            Order order = new Order("LIMIT" ,"BTCUSDT","50000","BUY");
//            Order order = new Order ("MARKET", "BTCUSDT","","SELL");

            requestID= orderService.newOrder(order, ID);
            Assertions.assertThat(orderService.getResult(requestID)).isEqualTo("SUCCESS");

            requestID = orderService.newOrder(order, ID);
            Assertions.assertThat(orderService.getResult(requestID)).isEqualTo("SUCCESS");

        }catch (Exception e){
            System.out.println(e);
        }
    }


    @Test
    public void getOpenOrders() {

        try{

            String requestId =orderService.getOpenOrders(ID);
            Assertions.assertThat(orderService.getResult(requestId)).isEqualTo("SUCCESS");
        }catch (Exception e){
            System.out.println(e);
        }

    }

    @Test
    public void cancelALLOrder() {
        try{
            String requestID =orderService.cancelAllOrder(ID);
            Assertions.assertThat(orderService.getResult(requestID)).isEqualTo("SUCCESS");
        }catch(Exception e){
            System.out.println(e);
        }
    }

    @Test
    public void cancelOrder() {
        try{
            String requestID =orderService.cancelOrder(ID,orderId);
            Assertions.assertThat(orderService.getResult(requestID)).isEqualTo("SUCCESS");
        }catch(Exception e){
            System.out.println(e);
        }
    }

    @Test
    public void getAccoountStatus(){
        try{
            String requestID=orderService.getAccountStatus(ID);
            Assertions.assertThat(orderService.getResult(requestID)).isEqualTo("SUCCESS");
        }catch(Exception e){
            System.out.println(e);
        }
    }


}