import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

export interface Stats {
  auc_score: number;
  ks_stat: number;
  engine: string;
  total_predictions: number;
  model_version: string;
  last_updated: string;
  status?: string;
  message?: string;
}

export interface Feature {
  feature: string;
  importance: number;
  description: string;
}

export interface Benchmark {
  algorithm: string;
  roc_auc: number;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
}

export interface Prediction {
  customer_id: string;
  tenure_months: number;
  monthly_charges: number;
  churn_probability: number;
  risk_level: string;
  risk_timeframe: string;
  risk_color: string;
  primary_reason: string;
  contract_type: string;
}

export interface PredictionResponse {
  predictions: Prediction[];
  summary: {
    total_customers: number;
    high_risk_count: number;
    medium_risk_count: number;
    low_risk_count: number;
    average_probability: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly API_BASE = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getStats(): Observable<Stats> {
    return this.http.get<Stats>(`${this.API_BASE}/stats`).pipe(
      catchError(this.handleError)
    );
  }

  getFeatureImportance(): Observable<Feature[]> {
    return this.http.get<Feature[]>(`${this.API_BASE}/feature-importance`).pipe(
      catchError(this.handleError)
    );
  }

  getBenchmark(): Observable<Benchmark[]> {
    return this.http.get<Benchmark[]>(`${this.API_BASE}/benchmark`).pipe(
      catchError(this.handleError)
    );
  }

  predict(file: File): Observable<PredictionResponse> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post<PredictionResponse>(`${this.API_BASE}/predict`, formData).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An unknown error occurred';
    
    if (error.error instanceof ErrorEvent) {
      errorMessage = `Error: ${error.error.message}`;
    } else {
      errorMessage = error.error?.detail || `Server error: ${error.status}`;
    }

    return throwError(() => errorMessage);
  }
}
