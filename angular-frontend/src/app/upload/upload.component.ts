import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-upload',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './upload.component.html',
  styleUrl: './upload.component.css'
})
export class UploadComponent {
  selectedFile: File | null = null;
  error: string = '';
  isUploading: boolean = false;

  constructor(private router: Router, private apiService: ApiService) {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      
      if (!file.name.endsWith('.csv')) {
        this.error = 'Please upload a CSV file only.';
        return;
      }
      
      this.selectedFile = file;
      this.error = '';
    }
  }

  onUpload(): void {
    if (!this.selectedFile) {
      this.error = 'Please select a file to upload.';
      return;
    }

    this.isUploading = true;
    this.error = '';

    // Navigate to processing page first
    this.router.navigate(['/processing']);

    // Then start the upload
    this.apiService.predict(this.selectedFile).subscribe({
      next: (response) => {
        // Store the response in sessionStorage for the dashboard
        sessionStorage.setItem('predictions', JSON.stringify(response));
        this.router.navigate(['/dashboard']);
      },
      error: (errorMessage) => {
        this.error = errorMessage;
        this.isUploading = false;
        this.router.navigate(['/upload']);
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/login']);
  }
}
