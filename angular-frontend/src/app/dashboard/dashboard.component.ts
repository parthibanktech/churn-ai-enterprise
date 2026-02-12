import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ApiService, Stats, Feature, Benchmark, Prediction, PredictionResponse } from '../services/api.service';
import { provideHttpClient } from '@angular/common/http';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {
  activeTab: string = 'dashboard';
  predictions: PredictionResponse | null = null;
  stats: Stats | null = null;
  features: Feature[] = [];
  benchmark: Benchmark[] = [];
  error: string = '';

  // Mock ROC Data
  rocData = [
    { x: 0, y: 0 }, { x: 0.1, y: 0.7 }, { x: 0.2, y: 0.85 },
    { x: 0.4, y: 0.92 }, { x: 0.7, y: 0.97 }, { x: 1, y: 1 }
  ];

  constructor(private router: Router, private apiService: ApiService) {}

  ngOnInit(): void {
    this.loadData();
    this.loadStoredData();
  }

  loadData(): void {
    this.apiService.getStats().subscribe({
      next: (data) => {
        this.stats = data;
      },
      error: (errorMessage) => {
        this.error = errorMessage;
      }
    });

    this.apiService.getFeatureImportance().subscribe({
      next: (data) => {
        this.features = data;
      },
      error: (errorMessage) => {
        this.error = errorMessage;
      }
    });

    this.apiService.getBenchmark().subscribe({
      next: (data) => {
        this.benchmark = data;
      },
      error: (errorMessage) => {
        this.error = errorMessage;
      }
    });
  }

  loadStoredData(): void {
    const stored = sessionStorage.getItem('predictions');
    if (stored) {
      this.predictions = JSON.parse(stored);
    }
  }

  setActiveTab(tab: string): void {
    this.activeTab = tab;
  }

  newAnalysis(): void {
    sessionStorage.removeItem('predictions');
    this.router.navigate(['/upload']);
  }

  logout(): void {
    sessionStorage.removeItem('predictions');
    this.router.navigate(['/login']);
  }

  getRiskColor(color: string): string {
    switch (color.toLowerCase()) {
      case 'red': return 'risk-high';
      case 'orange': return 'risk-med';
      case 'green': return 'risk-low';
      default: return 'risk-low';
    }
  }
}
