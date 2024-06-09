import { Component, OnInit } from '@angular/core';
import { BlogService } from '../../services/blog.service';
import { Blog } from '../../models/blog.models';
import { CommonModule } from '@angular/common';
import { DatePipe } from '../../../util/pipes/date-pipe.pipe';
import { Router } from '@angular/router';

@Component({
  selector: 'app-blog-list',
  standalone: true,
  templateUrl: './blog-list.component.html',
  styleUrl: './blog-list.component.css',
  imports: [DatePipe, CommonModule],
})
export class BlogListComponent implements OnInit {
  constructor(private blogService: BlogService, private router: Router) {}

  blogs: Blog[] = [];

  ngOnInit(): void {
    this.blogService.getBlogs().subscribe((blogs) => {
      this.blogs = blogs;
    });
  }

  goToBlog(blog: number): void {
    this.router.navigate(['/details', blog]);
  }
}
