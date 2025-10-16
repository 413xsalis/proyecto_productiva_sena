import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(): boolean {
    const isLoggedIn = this.authService.isLoggedIn();
    console.log('🛡️ AuthGuard - Usuario autenticado:', isLoggedIn);
    
    if (isLoggedIn) {
      return true;
    } else {
      console.log('🛑 Acceso denegado - Redirigiendo al login');
      this.router.navigate(['/login']);
      return false;
    }
  }
}