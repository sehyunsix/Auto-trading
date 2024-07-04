package spring.trading.controller;

import spring.trading.domain.Order;
import org.springframework.ui.Model;
import spring.trading.domain.Member;
import spring.trading.service.MemberService;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import java.util.List;

@Controller
public class OrderController {


    private final MemberService memberService;

    public OrderController(MemberService memberService) {
        this.memberService = memberService;
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
    public String makeOrder(OrderForm form) {
        Order order = new Order();
        order.setStock(form.getStock());
        order.setType(form.getType());
        order.setPrice(form.getPrice());
        return "redirect:/";
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
