package mk.soa.finki.ukim.jwtservice.controllers;


import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import mk.soa.finki.ukim.jwtservice.models.User;
import mk.soa.finki.ukim.jwtservice.models.dto.JwtAuthenticationResponse;
import mk.soa.finki.ukim.jwtservice.models.dto.LoginUserDto;
import mk.soa.finki.ukim.jwtservice.models.dto.RegisterUserDto;
import mk.soa.finki.ukim.jwtservice.models.dto.UserDto;
import mk.soa.finki.ukim.jwtservice.services.AuthenticationService;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class AuthenticationController {

    private final AuthenticationService authenticationService;

    public AuthenticationController(AuthenticationService authenticationService, ObjectMapper objectMapper) {
        this.authenticationService = authenticationService;
        this.objectMapper = objectMapper;
    }

    private final ObjectMapper objectMapper;


    @PostMapping("/register")
    public JwtAuthenticationResponse register(@RequestBody RegisterUserDto request) {
        return authenticationService.register(request);
    }

    @PostMapping("/login")
    public JwtAuthenticationResponse login(@RequestBody LoginUserDto request) {
        return authenticationService.login(request);
    }

    @GetMapping("/getUser")
    public String test() throws JsonProcessingException {
        Object user = SecurityContextHolder.getContext().getAuthentication()
                .getPrincipal();

        UserDto userDto = new UserDto();
        if (user instanceof User userDt) {
            userDto.setId(userDt.getId());
            userDto.setFirstName(userDt.getFirstName());
            userDto.setLastName(userDt.getLastName());
            userDto.setEmail(userDt.getEmail());
            userDto.setRole(userDt.getRole());
        }

        return objectMapper.writeValueAsString(userDto);
    }
}