package spring.trading.service;

import spring.trading.domain.Member;
import spring.trading.repository.MemberRepository;

import java.util.List;
import java.util.Optional;


public class MemberService {

    private MemberRepository memberRepository;

    public MemberService(MemberRepository memberRepository) {
        this.memberRepository = memberRepository;
    }
    /**
     * 회원가입
     */
    public Long join(Member member) {
        //같은 이름이 있는 중복 회원x

        validateDuplicateMember(member);
        memberRepository.save(member);
        return member.getId();

    }

    private void validateDuplicateMember(Member member) {
        memberRepository.findByName(member.getName())
                .ifPresent(m -> {
                    throw new IllegalStateException("이미 존재하는 회원입니다.");
                });
    }
    /**
     * 전체회원조회
     */
    public List<Member> findMembers(){
        return memberRepository.findAll();
    }

    public Optional<Member> findone(Long memberId){
        return memberRepository.findById(memberId);

    }

    public Optional<Member> findoneByName(String memberName){
        return memberRepository.findByName(memberName);
    }
}
