import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AdmissionService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
  }

  // Request-Response Loop Step 1: Angular calls http.post
  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/register`, userData);
  }

  login(credentials: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/auth/login`, credentials);
  }

  uploadDocument(file: File): Observable<any> {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    formData.append('document', file);
    return this.http.post(`${this.apiUrl}/student/application/upload`, formData, {
      headers: new HttpHeaders({ 'Authorization': `Bearer ${token}` })
    });
  }

  getAdminMetrics(): Observable<any> {
    return this.http.get(`${this.apiUrl}/admin/metrics`, { headers: this.getHeaders() });
  }
}
