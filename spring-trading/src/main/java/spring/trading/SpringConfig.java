package spring.trading;

import spring.trading.domain.order.OrderFactory;
import spring.trading.repository.MemberRepository;
import spring.trading.repository.MemoryMemberRepository;
import spring.trading.repository.RequestRepository;
import spring.trading.service.ContextWithOrder;
import spring.trading.service.MemberService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import spring.trading.service.OrderService;

@Configuration
public class SpringConfig {



    private final MemberRepository memberRepository;

    @Autowired
    public SpringConfig(MemberRepository memberRepository) {

        this.memberRepository = new MemoryMemberRepository();

    }


    @Bean
    public MemberService memberService() {
        return new MemberService(memberRepository);
    }

    @Bean
    public OrderFactory orderFactory() {
        return new OrderFactory();
    }


    @Bean
    public MemberRepository memberRepository() {
        return new MemoryMemberRepository();
    }



}
