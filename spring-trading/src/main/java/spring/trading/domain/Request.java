package spring.trading.domain;

import lombok.*;
import org.json.JSONObject;
import org.springframework.data.mongodb.core.mapping.Document;
import spring.trading.domain.order.OrderDTO;

@Setter
@Getter
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
@Document(collection = "request")
public class Request {
    private String requestId;
    private String status;
    private Long memberId;
    private OrderDTO order;
    private JSONObject result;
}
