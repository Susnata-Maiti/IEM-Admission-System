import { Component, OnInit } from '@angular/core';
import { AdmissionService } from './admission.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'IEM Admission System';
  user: any = null;
  metrics: any = null;
  selectedFile: File | null = null;
  uploadMessage = '';

  constructor(private admissionService: AdmissionService) {}

  ngOnInit(): void {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      this.user = JSON.parse(savedUser);
      if (this.user.role === 'admin' || this.user.role === 'director') {
        this.fetchMetrics();
      }
    }
  }

  onFileSelected(event: any): void {
    if (event.target.files && event.target.files[0]) {
      this.selectedFile = event.target.files[0];
    }
  }

  uploadMarksheet(): void {
    if (!this.selectedFile) return;
    this.admissionService.uploadDocument(this.selectedFile).subscribe({
      next: (res) => {
        this.uploadMessage = 'Document uploaded successfully! File on disk, reference stored in MongoDB.';
      },
      error: (err) => {
        this.uploadMessage = 'Upload failed: ' + (err.error?.detail || err.message);
      }
    });
  }

  fetchMetrics(): void {
    this.admissionService.getAdminMetrics().subscribe({
      next: (res) => {
        this.metrics = res.metrics;
      },
      error: (err) => console.error(err)
    });
  }
}
