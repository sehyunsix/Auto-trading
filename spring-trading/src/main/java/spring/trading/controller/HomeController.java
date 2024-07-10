package spring.trading.controller;

import io.swagger.v3.oas.models.annotations.OpenAPI31;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@OpenAPI31
@Controller
public class HomeController {
    @GetMapping("/")
    public String home() {
        return "home";
    }
}
