import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { BlogService } from '../../services/blog.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-create-blog',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './create-blog.component.html',
  styleUrl: './create-blog.component.css',
})
export class CreateBlogComponent {
  constructor(private blogService: BlogService, private router: Router) {}

  createBlogForm = new FormGroup({
    title: new FormControl(),
    blogText: new FormControl(),
  });

  public createBlog(): void {
    this.blogService
      .createBlog(
        this.createBlogForm.value['title'],
        this.createBlogForm.value['blogText']
      )
      .subscribe(() => {
        this.router.navigate(['/list']);
      });
  }
}
