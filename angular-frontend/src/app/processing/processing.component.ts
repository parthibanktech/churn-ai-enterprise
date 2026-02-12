import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, NavigationStart } from '@angular/router';

@Component({
  selector: 'app-processing',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './processing.component.html',
  styleUrl: './processing.component.css'
})
export class ProcessingComponent implements OnInit {
  uploadProgress: number = 0;
  progressInterval: any;

  constructor(private router: Router) {}

  ngOnInit(): void {
    this.startProgress();
  }

  startProgress(): void {
    this.uploadProgress = 0;
    
    this.progressInterval = setInterval(() => {
      this.uploadProgress += 10;
      if (this.uploadProgress >= 90) {
        clearInterval(this.progressInterval);
      }
    }, 200);
  }

  ngOnDestroy(): void {
    if (this.progressInterval) {
      clearInterval(this.progressInterval);
    }
  }
}
