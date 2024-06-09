import { User } from '../../authentication/models/user';

export class Blog {
  constructor(
    public id: number,
    public title: string,
    public blog_text: string,
    public date_created: Date,
    public comments: Comment[],
    public number_of_likes: number
  ) {}
}

export class Comment {
  constructor(
    public comment_id: string,
    public blog: Blog,
    public userId: number,
    public comment_text: string,
    public dateCreate: Date
  ) {}
}
