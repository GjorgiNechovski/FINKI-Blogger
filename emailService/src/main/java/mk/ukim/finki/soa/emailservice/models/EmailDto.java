package mk.ukim.finki.soa.emailservice.models;

import lombok.Getter;

@Getter
public class EmailDto {
    private String email;
    private String header;
    private String message;
}
