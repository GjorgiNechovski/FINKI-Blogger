package mk.soa.finki.ukim.jwtservice.models.dto;

import lombok.Getter;

@Getter
public class LoginUserDto {
    private String email;

    private String password;
}
