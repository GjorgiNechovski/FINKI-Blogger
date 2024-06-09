package mk.soa.finki.ukim.jwtservice.models.dto;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import lombok.Setter;
import mk.soa.finki.ukim.jwtservice.models.enums.UserRole;

@AllArgsConstructor
@NoArgsConstructor
@Setter
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class UserDto {
    private Long id;
    private String firstName;
    private String lastName;
    private String email;
    private UserRole role;

}
