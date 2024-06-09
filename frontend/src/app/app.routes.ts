import { Routes } from '@angular/router';
import { RegisterComponent } from '../src/authentication/components/register/register.component';
import { LoginComponent } from '../src/authentication/components/login/login.component';
import { CreateBlogComponent } from '../src/blogs/components/create-blog/create-blog.component';
import { BlogListComponent } from '../src/blogs/components/blog-list/blog-list.component';
import { BlogDetailsComponent } from '../src/blogs/components/blog-details/blog-details.component';
import { NavigationBarComponent } from '../src/navigation/components/navigation-bar/navigation-bar.component';
import { AuthGuard } from '../src/authentication/interceptors/auth-guard.service';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'list',
    pathMatch: 'full',
  },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },
  {
    path: 'list',
    component: NavigationBarComponent,
    children: [
      { path: '', component: BlogListComponent, canActivate: [AuthGuard] },
    ],
  },
  {
    path: 'details/:id',
    component: NavigationBarComponent,
    children: [
      { path: '', component: BlogDetailsComponent, canActivate: [AuthGuard] },
    ],
  },
  {
    path: 'createBlog',
    component: NavigationBarComponent,
    children: [
      { path: '', component: CreateBlogComponent, canActivate: [AuthGuard] },
    ],
  },
  {
    path: '**',
    redirectTo: 'list',
  },
];
