import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  passkey: string = '';
  error: string = '';
  isSubmitting: boolean = false;

  constructor(private router: Router) {}

  onSubmit(): void {
    this.error = '';
    this.isSubmitting = true;

    // Simulate validation delay
    setTimeout(() => {
      if (this.passkey === 'admin123' || this.passkey === 'churn2026') {
        this.router.navigate(['/upload']);
      } else {
        this.error = 'Invalid authorization key. Please try again.';
      }
      this.isSubmitting = false;
    }, 500);
  }
}
