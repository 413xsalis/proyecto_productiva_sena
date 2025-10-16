import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ExcelService {
  private baseUrl = 'http://localhost:8000/api/excel';

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  private getHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    console.log('🔐 Token obtenido:', token ? '✅ Presente' : '❌ Ausente');
    
    if (!token) {
      console.error('❌ No hay token disponible');
      throw new Error('No authentication token available');
    }
    
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
  }

  private getUploadHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    console.log('🔐 Token para upload:', token ? '✅ Presente' : '❌ Ausente');
    
    if (!token) {
      console.error('❌ No hay token disponible para upload');
      throw new Error('No authentication token available');
    }
    
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  uploadExcelFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file, file.name);

    console.log('📤 Enviando archivo a:', `${this.baseUrl}/upload`);
    
    return this.http.post(`${this.baseUrl}/upload`, formData, {
      headers: this.getUploadHeaders()
    });
  }

  processExcelFile(fileId: number): Observable<any> {
    console.log('🔄 Procesando archivo ID:', fileId);
    return this.http.post(`${this.baseUrl}/process/${fileId}`, {}, {
      headers: this.getHeaders()
    });
  }

  getMyFiles(): Observable<any> {
    console.log('📥 Obteniendo archivos del usuario');
    return this.http.get(`${this.baseUrl}/my-files`, {
      headers: this.getHeaders()
    });
  }

  getAllFiles(): Observable<any> {
    return this.http.get(`${this.baseUrl}/all-files`, {
      headers: this.getHeaders()
    });
  }

  getFile(fileId: number): Observable<any> {
    console.log('📥 Obteniendo archivo específico ID:', fileId);
    return this.http.get(`${this.baseUrl}/${fileId}`, {
      headers: this.getHeaders()
    });
  }

  deleteExcelFile(fileId: number): Observable<any> {
    console.log('🗑️ Eliminando archivo ID:', fileId);
    return this.http.delete(`${this.baseUrl}/${fileId}`, {
      headers: this.getHeaders()
    });
  }
}