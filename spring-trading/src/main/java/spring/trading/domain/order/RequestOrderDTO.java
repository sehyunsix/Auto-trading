package spring.trading.domain.order;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.*;
import spring.trading.domain.Member;

@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@ToString
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class RequestOrderDTO  {
    private Member member;
    private OrderDTO order;

}
