import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css',
})
export class RegisterComponent {
  constructor(private authService: AuthService, private router: Router) {}

  registerForm = new FormGroup({
    firstName: new FormControl(),
    lastName: new FormControl(),
    email: new FormControl(),
    password: new FormControl(),
  });

  register() {
    const firstName = this.registerForm.value.firstName;
    const lastName = this.registerForm.value.lastName;
    const email = this.registerForm.value.email;
    const password = this.registerForm.value.password;

    this.authService.register(firstName, lastName, email, password).subscribe();

    this.router.navigateByUrl('/login');
  }
}
