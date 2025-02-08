package spring.trading.domain.order;

import com.fasterxml.jackson.annotation.JsonInclude;
import jakarta.validation.constraints.Min;
import lombok.*;
import org.jetbrains.annotations.NotNull;
import org.json.JSONObject;


@NoArgsConstructor
@AllArgsConstructor
@Getter
@Setter
@ToString
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
@Conditional.List({
        @Conditional(
                selected = "type",
                values = {"LIMIT"},
                required = {"timeInForce", "price"}),


        @Conditional(
                selected = "type",
                values = {"STOP_LOSS"},
                required = {"trailingDelta"}),

        @Conditional(
                selected = "type",
                values = {"OCO"},
                required={"price","trailingDelta"}
        ),

        @Conditional(
                selected = "type",
                values = {"STOP_LOSS_LIMIT"},
                required={"price","trailingDelta"}
        )
}


)
public class OrderDTO {


    @EnumValue( values ={ "BUY","SELL"}, message = "유효하지 않는 side 값입니다. " )
    @NotNull
    private String side;

    @EnumValue( values ={ "STOP_LOSS","MARKET","LIMIT","STOP_LOSS_LIMIT"}, message = " 유효하지 않은 type 값입니다." )
    @NotNull
    private String type;


    @NotNull
    private double quantitiy;

    @EnumValue( values ={ "ETHUSDT","BTCUSDT"}, message = " 유효하지 않은 symbol 값입니다." )
    @NotNull
    private String symbol;

    @Min(0)
    private Double price;

    private String timeInForce;

    @Min(0)
    private Integer trailingDelta;

    private JSONObject params;
}
