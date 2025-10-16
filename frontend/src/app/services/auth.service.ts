import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private baseUrl = 'http://localhost:8000/api/users';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    const url = `${this.baseUrl}/login`;
    console.log('🔍 Enviando login a:', url);
    
    return this.http.post(url, { username, password }, {
      headers: {
        'Content-Type': 'application/json'
      }
    }).pipe(
      tap((response: any) => {
        console.log('✅ Respuesta del servidor:', response);
        if (response?.access_token) {
          localStorage.setItem('token', response.access_token);
          console.log('🔐 Token guardado');
        }
      })
    );
  }

  register(userData: { username: string; email: string; password: string }): Observable<any> {
    const url = `${this.baseUrl}/register`;
    console.log('🔍 Enviando registro a:', url, userData);
    
    return this.http.post(url, userData, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
  }

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  logout(): void {
    localStorage.removeItem('token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  checkHealth(): Observable<any> {
    return this.http.get('http://localhost:8000/health');
  }
}