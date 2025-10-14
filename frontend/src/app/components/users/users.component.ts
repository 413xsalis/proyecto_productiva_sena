import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-users',
  standalone: true, // 👈 importante
  imports: [CommonModule], // 👈 para que *ngIf y *ngFor funcionen
  templateUrl: './users.component.html'
})
export class UsersComponent implements OnInit {
  users: any[] = [];
  error = '';

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.userService.getUsers().subscribe({
      next: (res) => (this.users = res),
      error: (err) => (this.error = err.error?.detail || err.message)
    });
  }
}
