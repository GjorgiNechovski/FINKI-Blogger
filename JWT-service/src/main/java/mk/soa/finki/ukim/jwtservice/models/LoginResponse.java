package mk.soa.finki.ukim.jwtservice.models;

import lombok.AllArgsConstructor;

@AllArgsConstructor
public class LoginResponse {
    private String token;

    private long expiresIn;

}
