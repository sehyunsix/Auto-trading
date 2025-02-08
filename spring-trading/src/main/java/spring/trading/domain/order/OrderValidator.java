//package spring.trading.domain.order;
//
//import org.apache.tomcat.util.bcel.Const;
//import org.json.JSONException;
//import org.json.JSONObject;
//import spring.trading.service.Constants;
//
//import java.util.Arrays;
//import java.util.HashMap;
//import java.util.List;
//import java.util.Map;
//import java.util.function.Function;
//
//public class OrderValidator(JSONObject params) {
//
//     public final static  String [] SYMBOL = {"ETHUSDT", "BTCUSDT"};
//     public final static String[] TYPE = {"MARKET", "LIMIT", "STOP_LOSS"};
//     public final static String[] SIDE = {"BUY", "SELL"};
//     public final static String[] TIMEINFORCE={"GTC"};
//     public final static Map<String,Map<Class<?>,Function<Object,Object>>> PARAMETERS = new HashMap<>();
//     static {
//
//          PARAMETERS.put("side", String.class);
//          PARAMETERS.put("type", String.class);
//          PARAMETERS.put("symbol", String.class);
//          PARAMETERS.put("timeInforce", String.class);
//          PARAMETERS.put("price", Double.class);
//          PARAMETERS.put("quantity", Double.class);
//          PARAMETERS.put("trailingDelta", Long.class);
//     }
//
//     public class Params {
//
//          private String request_id;
//          private String timeInforce;
//          private String symbol;
//          private String side;
//          private String type;
//          private double price;
//          private double quantity;
//          private Long trailingDelta;
//     }
//
//     public final static String[] DEFAULT_PARAMS={ "side","type","quantity","symbol"};
//     public final static Map<String ,String[]> ADD_PARMAS= Map.ofEntries(
//             Map.entry("LIMIT" ,new String[]{"timeInforce","price"} ),
//             Map.entry("STOP_LOSS" ,new String[]{"timeInforce","price"} )
//             );
//
//
//
//     public void isVaild(JSONObject params) throws JSONException {
//
//          Arrays.stream(DEFAULT_PARAMS).forEach(param -> {})
//
//     }
//
//
//     public void typeVaild(String type) throws JSONException {
//         if(! Arrays.asList(TYPE).contains(type)){
//              throw new IllegalArgumentException("Invalid type");
//         };
//     }
//
//     public void  sideVaild(String side) throws JSONException {
//          if(! Arrays.asList(SIDE).contains(side)){
//               throw new IllegalArgumentException("Invalid side");
//          };
//     }
//
//     public void  symbolVaild(String symbol) throws JSONException {
//          if(! Arrays.asList(SYMBOL).contains(symbol)){
//               throw new IllegalArgumentException("Invalid symbol");
//          };
//     }
//
//     public void  quantityVaild(double quantity) throws JSONException {
//          if(quantity<0){
//               throw new IllegalArgumentException("Invalid quantity");
//          };
//     }
//
//     public void trailingDeltaVaild(Long trailingDelta) throws JSONException {
//          if(trailingDelta < 0){
//               throw new IllegalArgumentException("Invalid trailing delta");
//          }
//     }
//
//     public void price(double price) throws JSONException {
//          if(price<0){
//               throw new IllegalArgumentException("Invalid price");
//          }
//     }
//
//     public void timeInforceVaild(String timeInforce) throws JSONException {
//          if(! Arrays.asList(TIMEINFORCE).contains(timeInforce)){
//               throw new IllegalArgumentException("Invalid timeInforce");
//          };
//     }
//
//
//
//     public newOrderValid(JSONObject params) {
//
//          String type =params.getString("type");
//          String side =params.getString ("side");
//          String symbol = params.getString("symbol");
//          String quantity= params.getString("quantity");
//
//          if (!params.has("orderId")) {}
//     }
//
//
//}
