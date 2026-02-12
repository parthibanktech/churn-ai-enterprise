# ChurnAI: Customer Intelligence Platform

A modern, enterprise-grade customer churn prediction system with advanced machine learning analytics and beautiful UI.

## 🚀 Features

### Backend (FastAPI)
- **Advanced ML Pipeline**: XGBoost-powered churn prediction with 84.37% AUC accuracy
- **Robust Error Handling**: Comprehensive validation and user-friendly error messages
- **RESTful API**: Clean, well-documented endpoints for predictions and analytics
- **Data Validation**: Input validation with detailed feedback for CSV uploads
- **Feature Engineering**: Automated feature extraction and transformation
- **Model Monitoring**: Performance metrics and system health endpoints

### Frontend (React + Vite)
- **Modern UI**: Beautiful, responsive design with dark theme
- **Interactive Dashboard**: Real-time analytics with charts and visualizations
- **Customer Analysis**: Detailed risk assessment with actionable insights
- **Performance Metrics**: Model evaluation with ROC curves and benchmarks
- **Algorithm Comparison**: Multi-algorithm performance benchmarking
- **Progress Tracking**: Real-time upload and processing progress

## 📊 Key Improvements Made

### Backend Enhancements
- ✅ **Professional API Design**: Clear, descriptive endpoints with proper HTTP status codes
- ✅ **Enhanced Error Handling**: User-friendly error messages instead of generic alerts
- ✅ **Input Validation**: Comprehensive CSV validation with specific column requirements
- ✅ **Better Data Structure**: Organized response format with summary statistics
- ✅ **Improved Documentation**: Clear docstrings and API descriptions
- ✅ **Risk Classification**: Intelligent risk categorization with actionable insights

### Frontend Improvements
- ✅ **Modern Design System**: Professional dark theme with consistent styling
- ✅ **Enhanced UX**: Better navigation, loading states, and error feedback
- ✅ **Interactive Visualizations**: Pie charts, progress bars, and animated components
- ✅ **Responsive Layout**: Grid-based design that works on all screen sizes
- ✅ **Component Architecture**: Well-organized, reusable React components
- ✅ **Accessibility**: Proper semantic HTML and keyboard navigation

### Content & UX Fixes
- ✅ **Professional Language**: Removed jargon and unclear terminology
- ✅ **Clear Instructions**: Better guidance for file uploads and system usage
- ✅ **Demo Credentials**: Clear indication of available login keys
- ✅ **Progress Indicators**: Visual feedback for all async operations
- ✅ **Error Messages**: Helpful, actionable error descriptions

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **XGBoost**: Gradient boosting framework for ML predictions
- **Pandas**: Data manipulation and analysis
- **Scikit-learn**: Machine learning utilities
- **Joblib**: Model serialization and parallel processing

### Frontend
- **React 19**: Modern UI library with hooks
- **Vite**: Fast build tool and development server
- **Recharts**: Data visualization library
- **Lucide React**: Beautiful icon library
- **Axios**: HTTP client for API requests

### Styling
- **CSS3**: Modern CSS with custom properties
- **Inter & JetBrains Mono**: Professional typography
- **CSS Grid & Flexbox**: Responsive layout system

## 📁 Project Structure

```
customer_problem/
├── app.py                    # FastAPI backend application
├── frontend/                  # React frontend application
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   └── index.css        # Global styles
│   ├── package.json         # Frontend dependencies
│   └── vite.config.js       # Vite configuration
├── src/                     # Backend utilities and configuration
├── features/                # Feature engineering modules
├── models/                  # Trained ML models
├── data/                    # Sample datasets
└── requirements.txt         # Python dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
1. Navigate to the project directory:
   ```bash
   cd d:\AI\customer_problem
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   python app.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173`

## 🔐 Authentication

Use one of the following demo keys to access the platform:
- `admin123`
- `churn2026`

## 📊 API Endpoints

### GET `/api/stats`
Returns model performance statistics and system health metrics.

### POST `/api/predict`
Accepts CSV file uploads and returns churn predictions with risk analysis.

### GET `/api/feature-importance`
Returns feature importance scores from the trained model.

### GET `/api/benchmark`
Returns model performance benchmark across different algorithms.

## 📈 Usage Guide

1. **Login**: Enter your authorization key on the login screen
2. **Upload Data**: Navigate to Data Upload Center and upload a CSV file
3. **Required Columns**: Ensure your CSV includes:
   - `customerID`: Unique customer identifier
   - `tenure`: Customer tenure in months
   - `MonthlyCharges`: Monthly billing amount
   - `Contract`: Contract type (Month-to-month, One year, Two year)
4. **View Results**: Check the Dashboard for comprehensive analytics
5. **Analyze Customers**: Review individual customer risk profiles
6. **Monitor Performance**: Track model metrics and benchmarks

## 🎯 Key Features

### Risk Classification
- **Critical**: >85% churn probability (Next 30 days)
- **At-Risk**: 60-85% churn probability (2-4 months)
- **Stable**: 15-60% churn probability (Baseline)
- **Loyal**: <15% churn probability (Strong retention)

### Key Risk Factors
1. **Contract Type**: Month-to-month contracts have highest risk
2. **Payment Method**: Electronic check payments correlate with churn
3. **Monthly Charges**: Higher charges increase churn probability
4. **Customer Tenure**: Longer tenure customers are more loyal

### Model Performance
- **AUC Score**: 84.37%
- **Accuracy**: 80.0%
- **Precision**: 78.0%
- **Recall**: 82.0%
- **F1-Score**: 80.0%

## 🔧 Configuration

### Environment Variables
- `API_BASE`: Base URL for API requests (default: `http://localhost:8000/api`)

### Model Configuration
- Model files are stored in the `models/` directory
- Feature engineering is handled by `features/feature_engineering.py`
- Configuration settings are in `src/config.py`

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the FastAPI server is running before accessing the frontend
2. **File Upload Errors**: Verify CSV format and required columns
3. **Model Loading**: Check that model files exist in the `models/` directory
4. **API Connection**: Confirm both backend and frontend are running on correct ports

### Error Messages
- **Invalid file format**: Please upload a CSV file only
- **Missing columns**: Ensure all required columns are present
- **Model offline**: Check if the model files are properly loaded

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions, please refer to the documentation or create an issue in the repository.

---

**ChurnAI: Customer Intelligence Platform** - Transform your customer retention strategy with AI-powered insights.
