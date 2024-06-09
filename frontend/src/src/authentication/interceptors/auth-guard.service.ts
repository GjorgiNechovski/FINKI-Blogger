import { Injectable } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  Router,
  RouterStateSnapshot,
  UrlTree,
} from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthGuard {
  constructor(private router: Router) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean | UrlTree {
    let token = localStorage.getItem('jwtToken');
    const jwtTokenDate = localStorage.getItem('jwtTokenDate');
    let date;

    if (jwtTokenDate) {
      date = new Date(jwtTokenDate);
    }

    if (date && date?.getTime() < Date.now()) {
      localStorage.removeItem('jwtToken');
      localStorage.removeItem('jwtTokenDate');
      token = null;

      return this.router.parseUrl('/login');
    }

    return true;
  }
}
