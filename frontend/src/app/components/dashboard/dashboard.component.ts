import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  userName: string = 'admin12';
  userEmail: string = 'admin@example.com';
  // Agrega este método a la clase DashboardComponent
  navigateToExcelUpload() {
    this.router.navigate(['/excel-upload']);
  }
  constructor(
    private authService: AuthService,
    private router: Router
  ) { }

  ngOnInit() {
    this.loadUserData();
  }

  loadUserData() {
    console.log('🔄 Cargando datos del dashboard...');
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
    console.log('🔐 Sesión cerrada');
  }

  getUserInitials(): string {
    return this.userName
      .split(' ')
      .map(name => name[0])
      .join('')
      .toUpperCase();
  }
}