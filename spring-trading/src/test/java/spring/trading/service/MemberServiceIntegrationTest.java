package spring.trading.service;

import spring.trading.domain.Member;
import spring.trading.repository.MemberRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.transaction.annotation.Transactional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

@SpringBootTest
@Transactional
class MemberServiceIntegrationTest {

    @Autowired
    MemberService memberService;
    @Autowired
    MemberRepository memberRepository;


    @Test
    void join() {
        //given
        Member member = new Member();
        member.setName("ffff");
        member.setSecretkey("111");
        member.setPublickey("222");
        //when
        Long saveID = memberService.join(member);

        //then
        Member result = memberService.findone(saveID).get();
        assertThat(member.getName()).isEqualTo(result.getName());
        assertThat(member.getPublickey()).isEqualTo(result.getPublickey());
        assertThat(member.getSecretkey()).isEqualTo(result.getSecretkey());
    }

    @Test
    public void 중복_회원_예와() {
        //given
        Member member1 = new Member();
        member1.setName("hello100");

        Member member2 = new Member();
        member2.setName("hello100");
        //when
        memberService.join(member1);
        assertThrows(IllegalStateException.class, () -> memberService.join(member2));

//        try {
//            memberService.join(member1);
//            fail("예외 발생 실패");
//
//        }
//        catch (IllegalStateException e){
//            assertThat(e.getMessage()).isEqualTo("이미 존재하는 회원입니다.");
//        }
        //then


    }
}