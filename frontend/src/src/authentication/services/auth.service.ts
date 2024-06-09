import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../models/user';
import { authentication_url } from '../../../app/application.config';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private httpClient: HttpClient) {}

  login(
    email: string,
    password: string
  ): Observable<{ token: string; date: Date }> {
    return this.httpClient.post<{ token: string; date: Date }>(
      `${authentication_url}/login`,
      {
        email: email,
        password: password,
      }
    );
  }

  register(
    firstName: string,
    lastName: string,
    email: string,
    password: string
  ): Observable<{ token: string }> {
    return this.httpClient.post<{ token: string }>(
      `${authentication_url}/register`,
      {
        email: email,
        password: password,
        firstName: firstName,
        lastName: lastName,
      }
    );
  }

  getCurrentUser(): Observable<User> {
    return this.httpClient.get<User>(`${authentication_url}/getUser`);
  }

  storeToken(token: string): void {
    localStorage.setItem('jwtToken', token);
  }

  storeTokenDate(date: Date): void {
    localStorage.setItem('jwtTokenDate', date.toString());
  }

  getToken(): string | null {
    return localStorage.getItem('jwtToken');
  }

  clearToken(): void {
    localStorage.removeItem('jwtToken');
  }
}
