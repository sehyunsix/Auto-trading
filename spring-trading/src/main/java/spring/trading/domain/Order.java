package spring.trading.domain;

import com.binance.connector.client.impl.WebSocketApiClientImpl;

public class Order {

    private String type="T";
    private String stock="BTC";
    private String price="0";
    private String side="BUY";
    private String timeInForce="GTC";



    public Order(String type, String stock, String price, String side) {
        this.type = type;
        this.stock = stock;
        this.price = price;
        this.side = side;
    }

    public Order(){

    }
    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getStock() {
        return stock;
    }

    public void setStock(String stock) {
        this.stock = stock;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    public String getSide() {
        return side;
    }

    public void setSide(String side) {
        this.side = side;
    }

    public String getTimeInForce() {
        return timeInForce;
    }

    public void setTimeInForce(String timeInForce) {
        this.timeInForce = timeInForce;
    }

}
