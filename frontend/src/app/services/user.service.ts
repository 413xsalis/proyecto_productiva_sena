import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  // ✅ URL directa - sin environments
  private baseUrl = 'http://localhost:8000/api/users';

  constructor(private http: HttpClient) {}

  // Tus métodos aquí...
  getUsers(): Observable<any> {
    return this.http.get(this.baseUrl);
  }
}