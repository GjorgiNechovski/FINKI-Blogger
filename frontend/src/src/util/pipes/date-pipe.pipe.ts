import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'datePipe',
  standalone: true,
})
export class DatePipe implements PipeTransform {
  transform(value: Date): string {
    if (value) {
      return value.toString().split('T')[0];
    }
    return '';
  }
}
