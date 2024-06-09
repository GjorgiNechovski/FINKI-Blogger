import { HttpHeaders } from '@angular/common/http';

export const authentication_url = 'http://localhost:8080/api';

export const blog_url = 'http://127.0.0.1:8081';
export const comment_url = 'http://127.0.0.1:8082';
export const like_url = 'http://127.0.0.1:8083';

export const headers = new HttpHeaders({
  'Content-Type': 'application/json',
  Accept: 'application/json',
});
