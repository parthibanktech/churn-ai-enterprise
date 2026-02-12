# ChurnAI Angular Frontend

A modern, enterprise-grade Angular application for customer churn prediction and analytics.

## 🚀 Features

- **Modern Angular 17**: Built with the latest Angular features and standalone components
- **Beautiful UI**: Professional dark theme with responsive design
- **TypeScript**: Full type safety and better development experience
- **Component Architecture**: Modular, reusable components
- **Routing**: Single-page application with smooth navigation
- **API Integration**: Comprehensive service layer for backend communication
- **Error Handling**: User-friendly error messages and validation
- **Loading States**: Professional loading animations and progress indicators

## 🛠️ Technology Stack

- **Angular 17**: Modern framework with standalone components
- **TypeScript**: Type-safe development
- **RxJS**: Reactive programming for API calls
- **CSS3**: Modern styling with custom properties
- **Angular HttpClient**: HTTP client for API communication

## 📁 Project Structure

```
angular-frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── login/           # Login component
│   │   │   ├── upload/          # File upload component
│   │   │   ├── processing/      # Processing animation component
│   │   │   └── dashboard/       # Main dashboard component
│   │   ├── services/
│   │   │   └── api.service.ts # API service
│   │   ├── app.component.ts     # Root component
│   │   ├── app.config.ts       # App configuration
│   │   └── app.routes.ts       # App routing
│   ├── styles.css              # Global styles
│   ├── index.html              # HTML template
│   └── main.ts                # Application entry point
├── package.json               # Dependencies
├── angular.json              # Angular configuration
├── tsconfig.json            # TypeScript configuration
└── README.md                # This file
```

## 🚀 Getting Started

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

1. Navigate to the Angular frontend directory:
   ```bash
   cd d:\AI\customer_problem\angular-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

   The application will be available at `http://localhost:4200`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## 🔐 Authentication

Use one of the following demo keys to access the platform:
- `admin123`
- `churn2026`

## 📊 Application Flow

1. **Login**: Enter authorization key to access the platform
2. **Upload**: Upload CSV file with customer data
3. **Processing**: View real-time processing progress
4. **Dashboard**: Analyze results with interactive visualizations

## 🎨 UI Components

### Login Component
- Secure authentication form
- Error handling and validation
- Loading states
- Professional design

### Upload Component
- Drag-and-drop file upload
- CSV validation
- File requirements display
- Progress tracking

### Processing Component
- Animated processing indicators
- Progress bar with percentage
- Step-by-step status updates
- Professional loading animation

### Dashboard Component
- Multi-tab interface
- Risk distribution visualization
- Customer analysis table
- Performance metrics
- Algorithm benchmarks

## 🔧 Configuration

### API Configuration
The API base URL is configured in `src/app/services/api.service.ts`:
```typescript
private readonly API_BASE = 'http://localhost:8000/api';
```

### Styling
Global styles are in `src/styles.css` with CSS custom properties for theming.

## 📱 Responsive Design

The application is fully responsive and works on:
- Desktop (1920x1080 and above)
- Tablet (768px and above)
- Mobile (320px and above)

## 🎯 Key Features

### Risk Classification
- **Critical**: >85% churn probability (Next 30 days)
- **At-Risk**: 60-85% churn probability (2-4 months)
- **Stable**: 15-60% churn probability (Baseline)
- **Loyal**: <15% churn probability (Strong retention)

### Dashboard Tabs
1. **Dashboard**: Overview with key metrics and risk distribution
2. **Customer Analysis**: Detailed customer risk profiles
3. **Model Performance**: ROC curves and performance metrics
4. **Algorithm Benchmarks**: Multi-algorithm comparison

### Data Visualization
- Risk distribution charts
- Feature importance bars
- Performance metrics
- Progress indicators
- Status badges

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure the backend is running on port 8000
2. **Module Not Found**: Run `npm install` to install dependencies
3. **Build Errors**: Check TypeScript configuration and dependencies
4. **API Connection**: Verify backend server is running

### Development Tips

- Use `ng serve` for development with hot reload
- Check browser console for any errors
- Verify API endpoints are accessible
- Test file upload with proper CSV format

## 📝 API Integration

The application integrates with the FastAPI backend through the `ApiService`:

```typescript
// Get model statistics
this.apiService.getStats().subscribe(data => {
  this.stats = data;
});

// Upload file for prediction
this.apiService.predict(file).subscribe(response => {
  this.predictions = response;
});
```

## 🎨 Customization

### Colors
Modify CSS custom properties in `styles.css`:
```css
:root {
  --accent: #6366f1;
  --success: #10b981;
  --danger: #f43f5e;
  --warning: #f59e0b;
}
```

### Typography
Font families are defined in `index.html` and used throughout the application.

## 📈 Performance

The application is optimized for:
- Fast initial load
- Smooth animations
- Efficient data handling
- Minimal bundle size
- Progressive enhancement

## 🔒 Security

- Input validation and sanitization
- Secure API communication
- Error handling without information leakage
- Professional authentication flow

---

**ChurnAI Angular Frontend** - Modern, type-safe, and beautiful customer intelligence platform.
