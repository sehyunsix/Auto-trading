package spring.trading.domain.order;


import jakarta.validation.Constraint;
import jakarta.validation.Payload;

import java.lang.annotation.Documented;
import java.lang.annotation.Repeatable;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.ElementType.TYPE;
import static java.lang.annotation.RetentionPolicy.RUNTIME;

@Repeatable(Conditional.List.class)
@Target(TYPE)
@Retention(RUNTIME)
@Constraint(validatedBy = ConditionalValidation.class)
public @interface Conditional {
    String message() default "this field is required";

    Class<?>[] groups() default {};

    //조건부 대상이 되는 필드명
    String selected();

    //조건부 대상이 요구되는 값
    String[] values();

    //값이 존재해야 하는 필드명
    String[] required();

    Class<? extends Payload>[] payload() default {};


    @Target({ TYPE })
    @Retention(RUNTIME)
    @Documented
    @interface List {
        Conditional[] value();
    }
}
