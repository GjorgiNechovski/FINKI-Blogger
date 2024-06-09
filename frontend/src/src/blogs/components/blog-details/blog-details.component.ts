import { Component, OnInit } from '@angular/core';
import { BlogService } from '../../services/blog.service';
import { Blog, Comment } from '../../models/blog.models';
import { ActivatedRoute, Router } from '@angular/router';
import { FormControl, FormGroup, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../../authentication/services/auth.service';
import { AsyncPipe } from '@angular/common';
import { User } from '../../../authentication/models/user';
import { finalize } from 'rxjs';

@Component({
  selector: 'app-blog-details',
  standalone: true,
  imports: [ReactiveFormsModule, AsyncPipe],
  templateUrl: './blog-details.component.html',
  styleUrl: './blog-details.component.css',
})
export class BlogDetailsComponent implements OnInit {
  blog: Blog | null = null;
  user: User | null = null;
  loading = false;

  createBlogForm = new FormGroup({
    commentText: new FormControl(),
  });

  constructor(
    public blogService: BlogService,
    public authService: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.getCurrentUser().subscribe((user) => (this.user = user));

    this.route.params.subscribe((params) => {
      const blogId = params['id'];
      this.blogService.getBlogDetails(blogId).subscribe((blog) => {
        this.blog = blog;
        this.loading = true;
      });
    });
  }

  deleteBlog(blogId: number): void {
    this.blogService.deleteBlog(blogId).subscribe(() => {
      this.router.navigate(['/list']);
    });
  }

  createComment() {
    const comment_text = this.createBlogForm.value['commentText'];

    this.blogService
      .createComment(this.blog!.id, comment_text)
      .subscribe(() => window.location.reload());
  }

  deleteComment(comment: Comment) {
    console.log(comment);

    this.blogService.deleteComment(comment.comment_id).subscribe(() => {
      window.location.reload();
    });
  }

  likeBlog(blog: Blog) {
    this.blogService
      .likeBlog(blog.id)
      .pipe(
        finalize(() => {
          window.location.reload();
        })
      )
      .subscribe();
  }
}
