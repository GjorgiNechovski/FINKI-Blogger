package mk.ukim.finki.soa.emailservice.controllers;

import mk.ukim.finki.soa.emailservice.models.EmailDto;
import mk.ukim.finki.soa.emailservice.services.EmailService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class EmailController {
    private final EmailService emailService;

    public EmailController(EmailService emailService) {
        this.emailService = emailService;
    }

    @PostMapping("/email")
    public ResponseEntity<Void> sendEmail(@RequestBody EmailDto email){
        this.emailService.sendEmail(email.getEmail(), email.getHeader(), email.getMessage());

        return ResponseEntity.ok().build();
    }
}
