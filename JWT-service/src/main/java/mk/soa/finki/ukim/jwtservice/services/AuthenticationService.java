package mk.soa.finki.ukim.jwtservice.services;

import lombok.RequiredArgsConstructor;
import mk.soa.finki.ukim.jwtservice.models.User;
import mk.soa.finki.ukim.jwtservice.models.dto.JwtAuthenticationResponse;
import mk.soa.finki.ukim.jwtservice.models.dto.LoginUserDto;
import mk.soa.finki.ukim.jwtservice.models.dto.RegisterUserDto;
import mk.soa.finki.ukim.jwtservice.models.enums.UserRole;
import mk.soa.finki.ukim.jwtservice.repository.UserRepository;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class AuthenticationService {

    private final UserRepository userRepository;
    private final UserService userService;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final AuthenticationManager authenticationManager;


    public JwtAuthenticationResponse register(RegisterUserDto request) {
        var user = User
                .builder()
                .firstName(request.getFirstName())
                .lastName(request.getLastName())
                .email(request.getEmail())
                .password(passwordEncoder.encode(request.getPassword()))
                .role(UserRole.ROLE_USER)
                .build();

        user = userService.save(user);
        var jwt = jwtService.generateToken(user);
        return JwtAuthenticationResponse.builder().token(jwt).build();
    }


    public JwtAuthenticationResponse login(LoginUserDto request) {
        authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword()));
        var user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new IllegalArgumentException("Invalid email or password."));
        var jwt = jwtService.generateToken(user);
        return JwtAuthenticationResponse.builder().token(jwt).date(jwtService.extractExpiration(jwt)).build();
    }

}