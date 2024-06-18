import { HttpHeaders } from '@angular/common/http';

export const authentication_url = 'http://localhost:8090/api';

export const blog_url = 'http://localhost:8086';
export const comment_url = 'http://localhost:8087';
export const like_url = 'http://localhost:8088';

export const headers = new HttpHeaders({
  'Content-Type': 'application/json',
  Accept: 'application/json',
});
