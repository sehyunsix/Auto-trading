package spring.trading.domain.order;

import jakarta.validation.ConstraintValidator;
import jakarta.validation.ConstraintValidatorContext;

import java.util.Arrays;

public class ValueOfEnumVailidation implements ConstraintValidator<EnumValue,String> {

    private EnumValue enumValue;
    private String[] values;

    @Override
    public void initialize(EnumValue constraintAnnotation) {
        this.enumValue = constraintAnnotation;
        this.values = constraintAnnotation.values();
    }

    @Override
    public boolean isValid(String value, ConstraintValidatorContext context) {
        boolean vaild = false;
        if (Arrays.asList(values).contains(value)) {
            vaild = true;
        }
        return vaild;
    }
}
