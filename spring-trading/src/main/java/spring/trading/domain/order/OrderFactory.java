package spring.trading.domain.order;

import com.binance.connector.client.utils.ParameterChecker;
import org.json.JSONException;
import org.json.JSONObject;
import org.springframework.stereotype.Component;


@Component
public class OrderFactory {



    public JSONObject createParams(OrderDTO orderDTO) throws JSONException {

        JSONObject params = new JSONObject();

        switch (orderDTO.getType()) {

            case "MARKET" :
                params.put("quantity", orderDTO.getQuantitiy());

            case "STOP_LOSS" :
                params.put("trailingDelta", orderDTO.getTrailingDelta());
                params.put("quantity", orderDTO.getQuantitiy());
                break;

            case "STOP_LOSS_LIMIT" :
                params.put("trailingDelta", orderDTO.getTrailingDelta());
                params.put("quantity", orderDTO.getQuantitiy());
                params.put("price", orderDTO.getPrice());
                params.put("timeInForce", orderDTO.getTimeInForce());
                break;

            case  "LIMIT" :
                params.put("timeInForce", orderDTO.getTimeInForce());
                params.put("price", orderDTO.getPrice());
                params.put("quantity", orderDTO.getQuantitiy());
                break;

            case  "OCO" :
                params.put("price", orderDTO.getPrice());
                params.put("quantity", orderDTO.getQuantitiy());
                params.put("trailingDelta", orderDTO.getTrailingDelta());
                break;

            default:
                break;
        }
        return params;
    }

    public OrderDTO createOrder(OrderDTO orderDTO) throws JSONException {
        String type = orderDTO.getType();
        JSONObject params = createParams(orderDTO);
        orderDTO.setParams(params);

        return orderDTO;

    }



}
