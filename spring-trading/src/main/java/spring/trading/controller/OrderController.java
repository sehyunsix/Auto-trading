package spring.trading.controller;

import io.micrometer.observation.annotation.Observed;
import io.swagger.v3.oas.models.annotations.OpenAPI31;
import jakarta.annotation.Nullable;
import jakarta.validation.Valid;
import org.apache.coyote.BadRequestException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.ResponseEntity;
import org.springframework.http.converter.HttpMessageNotReadableException;
import org.springframework.validation.BindingResult;
import org.springframework.validation.Errors;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.ErrorResponse;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;
import spring.trading.domain.Member;
import spring.trading.domain.order.OrderDTO;
import spring.trading.domain.order.OrderFactory;
import spring.trading.domain.order.RequestOrderDTO;
import spring.trading.service.ContextWithOrder;
import spring.trading.service.MemberService;
import org.springframework.stereotype.Controller;
import spring.trading.service.OrderService;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@OpenAPI31
@Controller
@RestController
public class OrderController {


    private final MemberService memberService;
    private final OrderFactory orderFactory;
    private final OrderService orderService;
    private final ContextWithOrder contextWithOrder;

    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<Map<String, Object>> onHttpMessageNotReadable(HttpMessageNotReadableException e) {
        Map<String, Object> body = new HashMap<>();
        body.put("message", e.getMessage());
        body.put("status", HttpStatus.BAD_REQUEST.value());
        return new ResponseEntity<>(body, HttpStatus.BAD_REQUEST);
    }

    @Autowired
    public OrderController(MemberService memberService , OrderService orderService , OrderFactory orderFactory, ContextWithOrder contextWithOrder) {
        this.orderService = orderService;
        this.memberService = memberService;
        this.orderFactory = orderFactory;
        this.contextWithOrder = contextWithOrder;
    }


    @GetMapping("/order/registerKey")
    public String creatForm( ) {
        return "order/registerKeyForm";
    }

    @GetMapping("/order/keys")
    public String findAll(Model model) {
        List<Member> members = memberService.findMembers();
        model.addAttribute ("members",members);
        return "order/listKeys";
    }

    @GetMapping("/order/makeOrder")
    public String creatOrderForm() {
        return "order/makeOrderForm";
    }


    @PostMapping("/order/makeOrder")
    public ResponseEntity makeOrder(@RequestBody @Validated RequestOrderDTO requestOrderDTO) {

        OrderDTO orderDTO1 = orderFactory.createOrder(requestOrderDTO.getOrder());
        try {
            orderService.newOrder(orderDTO1, requestOrderDTO.getMember());
        }catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(e.getMessage());
        }
        return new ResponseEntity<>(HttpStatus.CREATED);
    }


    @PostMapping("/order/registerKey")
    public String create(OrderForm form){
        Member member = new Member();
        member.setName(form.getName());
        member.setPublickey(form.getSecretkey());
        member.setSecretkey(form.getPublickey());
        memberService.join(member);
        return "redirect:/";
    }

}
