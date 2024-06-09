package mk.soa.finki.ukim.jwtservice.models.dto;

import lombok.Getter;

@Getter
public class RegisterUserDto {
    String firstName;
    String lastName;
    String email;
    String password;
}
