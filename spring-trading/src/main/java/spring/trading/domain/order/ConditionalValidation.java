package spring.trading.domain.order;

import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;
import org.springframework.beans.PropertyAccessorFactory;
import org.springframework.util.ObjectUtils;

import java.util.Arrays;

public class ConditionalValidation implements ConstraintValidator<Conditional,Object>{
    private String selected;
    private String[] required;
    private String[] values;
    private String message;

    //지정된 Conditional 어노테이션 객체가 전달된다

    @Override
    public void initialize( Conditional constraintAnnotation) {
        ConstraintValidator.super.initialize(constraintAnnotation);
        this.selected = constraintAnnotation.selected();
        this.values = constraintAnnotation.values();
        this.required = constraintAnnotation.required();
        this.message = constraintAnnotation.message();
    }

    /**
     * @param object  validate 대상 객체
     * @param context 제약조건이 평가되는 context
     * @return validation 성공 여부
     */
        @Override
        public boolean isValid(Object object, ConstraintValidatorContext context) {
            boolean valid = true;
            Object actualValue = PropertyAccessorFactory
                    .forDirectFieldAccess(object)
                    .getPropertyValue(selected);

            if (actualValue != null) {
                Object selectedValue;
                if (actualValue instanceof Enum) {
                    selectedValue = ((Enum<?>) actualValue).name();
                } else {
                    selectedValue = actualValue;
                }


                if (Arrays.asList(values).contains((String) selectedValue)) {
                    for (String fieldName : required) {
                        Object requiredValue = PropertyAccessorFactory
                                .forDirectFieldAccess(object)
                                .getPropertyValue(fieldName);
                        //요구되는 필드의 값이 빈 값이거나 null 인 경우 validation 은 실패
                        boolean empty = ObjectUtils.isEmpty(requiredValue);
                        if (empty) {
                            context.disableDefaultConstraintViolation();
                            context
                                    .buildConstraintViolationWithTemplate(message)
                                    .addPropertyNode(fieldName)
                                    .addConstraintViolation();
                            valid = false;
                        }
                    }
                }
            }

                return valid;
        }

}