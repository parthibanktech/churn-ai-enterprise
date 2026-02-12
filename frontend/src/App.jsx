import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  Cell, AreaChart, Area, CartesianGrid, LineChart, Line, Legend, Label, PieChart, Pie
} from 'recharts';
import {
  LayoutDashboard, Database, Activity,
  Upload, Rocket, LogOut, FileText, ChevronRight,
  Zap, ShieldCheck, Globe, Cpu, Bot, TrendingUp, AlertTriangle,
  Filter, BarChart3, Binary, Settings2, HelpCircle, CheckCircle,
  Users, Lightbulb, Shield, ClipboardList, Info, ArrowRight, Target, Lock, Key,
  TrendingDown, UserCheck, Clock, DollarSign, Calendar, Star
} from 'lucide-react';

const API_BASE = "http://localhost:8080/api";

function App() {
  const [step, setStep] = useState('LOGIN');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [authKey, setAuthKey] = useState('');
  const [passkey, setPasskey] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [predictions, setPredictions] = useState(null);
  const [stats, setStats] = useState({ auc_score: 0.8437, ks_stat: 0.45, engine: 'XGBoost' });
  const [benchmark, setBenchmark] = useState([]);
  const [features, setFeatures] = useState([]);
  const [error, setError] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterRisk, setFilterRisk] = useState('ALL');
  const [displayLimit, setDisplayLimit] = useState(100);

  useEffect(() => {
    setDisplayLimit(100);
  }, [filterRisk, searchTerm]);

  // Mock ROC Data
  const rocData = [
    { x: 0, y: 0 }, { x: 0.1, y: 0.7 }, { x: 0.2, y: 0.85 },
    { x: 0.4, y: 0.92 }, { x: 0.7, y: 0.97 }, { x: 1, y: 1 }
  ];

  useEffect(() => {
    if (step === 'DASHBOARD') {
      const fetchData = async () => {
        try {
          const [s, b, f] = await Promise.all([
            axios.get(`${API_BASE}/stats`),
            axios.get(`${API_BASE}/benchmark`),
            axios.get(`${API_BASE}/feature-importance`)
          ]);
          setStats(s.data);
          setBenchmark(b.data);
          setFeatures(f.data);
        } catch (e) {
          console.error("API Error", e);
          setError('Failed to connect to the server. Please check your connection.');
        }
      };
      fetchData();
    }
  }, [step]);

  const handleLogin = (e) => {
    e.preventDefault();
    if (authKey === 'admin123' || authKey === 'churn2026') {
      setStep('CHOICE');
      setError('');
    } else {
      setError('Invalid authorization key. Contact system administrator.');
    }
  };

  const handleTestSample = async () => {
    setStep('PROCESSING');
    setIsProcessing(true);
    setError('');
    setUploadProgress(0);

    const progressInterval = setInterval(() => {
      setUploadProgress(prev => (prev >= 90 ? 90 : prev + 10));
    }, 200);

    try {
      const res = await axios.post(`${API_BASE}/test-sample`);
      setUploadProgress(100);
      setPredictions(res.data);
      setStep('DASHBOARD');
    } catch (err) {
      setError('Failed to load sample data. Please try uploading your own.');
      setStep('CHOICE');
    } finally {
      setIsProcessing(false);
      clearInterval(progressInterval);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file only.');
      return;
    }

    setStep('PROCESSING');
    setIsProcessing(true);
    setError('');
    setUploadProgress(0);

    // Simulate progress
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + 10;
      });
    }, 200);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await axios.post(`${API_BASE}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadProgress(100);
      setPredictions(res.data);
      setStep('DASHBOARD');
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please check the file format and try again.');
      setStep('UPLOAD');
    } finally {
      setIsProcessing(false);
      clearInterval(progressInterval);
    }
  };

  // --- SCREENS ---

  if (step === 'LOGIN') {
    return (
      <div className="auth-wrapper animate-in">
        <div className="auth-card">
          <div className="auth-header">
            <div className="auth-icon"><ShieldCheck size={32} /></div>
            <h2 className="auth-title">ChurnAI Platform</h2>
            <p className="auth-desc">Customer Intelligence & Churn Prediction System</p>
          </div>
          {error && (
            <div className="error-message">
              <AlertTriangle size={16} />
              {error}
            </div>
          )}
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="form-group">
              <label className="form-label">Authorization Key</label>
              <div style={{ position: 'relative' }}>
                <Key size={16} style={{ position: 'absolute', left: '1rem', top: '1rem', color: 'var(--text-muted)' }} />
                <input
                  type="password"
                  className="form-input"
                  style={{ paddingLeft: '2.5rem' }}
                  placeholder="Enter your authorization key..."
                  value={authKey}
                  onChange={e => setAuthKey(e.target.value)}
                />
              </div>
            </div>
            <button type="submit" className="btn-primary">
              <Lock size={16} style={{ marginRight: '0.5rem' }} />
              Secure Login
            </button>
          </form>
          <div style={{ marginTop: '2rem', textAlign: 'center', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            <div style={{ marginBottom: '0.5rem' }}>Demo Keys: admin123 or churn2026</div>
            <div style={{ fontSize: '0.65rem', textTransform: 'uppercase', letterSpacing: '0.1em' }}>
              Enterprise-Grade Security • ML-Powered Analytics
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (step === 'CHOICE') {
    return (
      <div className="auth-wrapper animate-in">
        <div className="auth-card" style={{ maxWidth: '600px' }}>
          <div className="auth-header">
            <div className="auth-icon" style={{ background: 'var(--accent-glow)', color: 'var(--accent)' }}>
              <Zap size={32} />
            </div>
            <h2 className="auth-title">Analysis Mode Selection</h2>
            <p className="auth-desc">Choose how you want to interact with the prediction engine</p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginTop: '2rem' }}>
            <div
              className="upload-zone"
              onClick={handleTestSample}
              style={{ cursor: 'pointer', borderColor: 'var(--success)', padding: '2rem' }}
            >
              <Users size={40} style={{ color: 'var(--success)', marginBottom: '1rem' }} />
              <h4 style={{ color: '#fff' }}>Test Sample Data</h4>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                Quickly explore system features using pre-trained historical records.
              </p>
            </div>

            <div
              className="upload-zone"
              onClick={() => setStep('UPLOAD')}
              style={{ cursor: 'pointer', padding: '2rem' }}
            >
              <Database size={40} style={{ color: 'var(--accent)', marginBottom: '1rem' }} />
              <h4 style={{ color: '#fff' }}>New Dataset Upload</h4>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.5rem' }}>
                Analyze your own customer files for live, enterprise-grade insights.
              </p>
            </div>
          </div>

          <button onClick={() => setStep('LOGIN')} className="btn-secondary" style={{ marginTop: '2rem' }}>
            Sign Out
          </button>
        </div>
      </div>
    );
  }

  if (step === 'UPLOAD') {
    return (
      <div className="auth-wrapper animate-in">
        <div className="auth-card" style={{ maxWidth: '500px' }}>
          <div className="auth-header">
            <div className="auth-icon" style={{ background: 'var(--success-glow)', color: 'var(--success)' }}>
              <Database size={32} />
            </div>
            <h2 className="auth-title">Data Upload Center</h2>
            <p className="auth-desc">Upload customer data for churn analysis and prediction</p>
          </div>
          {error && (
            <div className="error-message">
              <AlertTriangle size={16} />
              {error}
            </div>
          )}
          <label className="upload-zone">
            <Upload size={48} style={{ color: 'var(--accent)', marginBottom: '1.5rem' }} />
            <p style={{ fontWeight: '700', marginBottom: '0.5rem' }}>Click to browse or drag and drop</p>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>CSV files only • Max 10MB</p>
            <input type="file" hidden accept=".csv" onChange={handleUpload} />
          </label>
          <div className="upload-requirements">
            <h4 style={{ fontSize: '0.875rem', fontWeight: '700', marginBottom: '1rem', color: 'var(--text-main)' }}>
              Required Dataset: IBM Telco Churn Format
            </h4>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
              The system requires the standard 21-column enterprise dataset including:
            </p>
            <div className="req-list" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
              <div className="req-item"><CheckCircle size={12} /> gender</div>
              <div className="req-item"><CheckCircle size={12} /> SeniorCitizen</div>
              <div className="req-item"><CheckCircle size={12} /> tenure</div>
              <div className="req-item"><CheckCircle size={12} /> Contract</div>
              <div className="req-item"><CheckCircle size={12} /> MonthlyCharges</div>
              <div className="req-item"><CheckCircle size={12} /> TotalCharges</div>
              <div className="req-item"><CheckCircle size={12} /> InternetService</div>
              <div className="req-item"><CheckCircle size={12} /> PaymentMethod</div>
            </div>
          </div>
          <button onClick={() => setStep('LOGIN')} className="btn-secondary">
            <ArrowRight size={16} style={{ transform: 'rotate(180deg)', marginRight: '0.5rem' }} />
            Back to Login
          </button>
        </div>
      </div>
    );
  }

  if (step === 'PROCESSING') {
    return (
      <div className="auth-wrapper animate-in">
        <div className="auth-card" style={{ textAlign: 'center' }}>
          <div className="neural-loader">
            <div className="loader-ring"></div>
            <Bot size={40} className="pulse" />
          </div>
          <h2 className="auth-title" style={{ marginTop: '2rem' }}>Processing Your Data</h2>
          <p className="auth-desc">Analyzing customer patterns and generating churn predictions...</p>

          <div className="progress-container" style={{ marginTop: '2rem' }}>
            <div className="progress-label">
              <span>Processing Progress</span>
              <span>{uploadProgress}%</span>
            </div>
            <div className="progress-bar-container">
              <div className="progress-bar-fill" style={{ width: `${uploadProgress}%` }}></div>
            </div>
          </div>

          <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
            <div className={`op-tag ${uploadProgress >= 25 ? 'active' : ''}`}>
              <Database size={12} style={{ marginRight: '0.25rem' }} />
              Data Validation
            </div>
            <div className={`op-tag ${uploadProgress >= 50 ? 'active' : ''}`}>
              <Zap size={12} style={{ marginRight: '0.25rem' }} />
              Feature Engineering
            </div>
            <div className={`op-tag ${uploadProgress >= 75 ? 'active' : ''}`}>
              <Cpu size={12} style={{ marginRight: '0.25rem' }} />
              ML Prediction
            </div>
            <div className={`op-tag ${uploadProgress >= 95 ? 'active' : ''}`}>
              <CheckCircle size={12} style={{ marginRight: '0.25rem' }} />
              Finalizing Results
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-shell">
      <aside className="sidebar">
        <div className="logo-container">
          <div className="logo-icon"><TrendingUp size={18} /></div>
          <span className="logo-text">ChurnAI <span style={{ color: 'var(--accent)' }}>Pro</span></span>
        </div>
        <nav className="flex-1 space-y-2">
          <NavLink icon={<LayoutDashboard size={18} />} label="Dashboard" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <NavLink icon={<Users size={18} />} label="Customer Analysis" active={activeTab === 'customers'} onClick={() => setActiveTab('customers')} />
          <NavLink icon={<BarChart3 size={18} />} label="Model Performance" active={activeTab === 'performance'} onClick={() => setActiveTab('performance')} />
          <NavLink icon={<Binary size={18} />} label="Algorithm Benchmarks" active={activeTab === 'benchmark'} onClick={() => setActiveTab('benchmark')} />
        </nav>
        <button onClick={() => setStep('UPLOAD')} className="nav-link" style={{ marginTop: '2rem', color: 'var(--accent)' }}>
          <Upload size={18} /> New Analysis
        </button>
        <button onClick={() => window.location.reload()} className="nav-link" style={{ color: 'var(--danger)' }}>
          <LogOut size={18} /> Logout
        </button>
      </aside>

      <main className="main-view">
        <header className="top-header">
          <div className="header-titles">
            <h1 style={{ color: '#fff' }}>
              {activeTab === 'dashboard' ? 'Analytics Dashboard' :
                activeTab === 'customers' ? 'Customer Insights' :
                  activeTab === 'performance' ? 'Model Performance' : 'Algorithm Benchmarks'}
            </h1>
            <p>Customer Intelligence Platform • {stats.engine || 'XGBoost'} Engine</p>
          </div>
          <div className="header-meta">
            <div className="status-indicator">
              <div className="dot"></div>
              <span style={{ fontSize: '0.65rem', fontWeight: '800', color: 'var(--text-muted)' }}>SYSTEM ONLINE</span>
            </div>
          </div>
        </header>

        {activeTab === 'dashboard' && (
          <div className="space-y-6 animate-in">
            {predictions && (
              <div className="stats-row" style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '1.5rem' }}>
                <SummaryTile
                  label="Total Customers"
                  val={predictions.summary?.total_customers || 0}
                  icon={<Users size={20} />}
                  color="var(--accent)"
                />
                <SummaryTile
                  label="High Risk"
                  val={predictions.summary?.high_risk_count || 0}
                  icon={<AlertTriangle size={20} />}
                  color="var(--danger)"
                />
                <SummaryTile
                  label="Score Variance"
                  val={(predictions.summary?.prediction_variance || 0).toFixed(4)}
                  icon={<Binary size={20} />}
                  color="#818cf8"
                />
                <SummaryTile
                  label="Avg Churn Risk"
                  val={`${(predictions.summary?.average_probability || 0).toFixed(1)}%`}
                  icon={<TrendingUp size={20} />}
                  color="var(--warning)"
                />
                <SummaryTile
                  label="Model Accuracy"
                  val={`${(stats.auc_score * 100).toFixed(1)}%`}
                  icon={<ShieldCheck size={20} />}
                  color="var(--success)"
                />
              </div>
            )}

            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem' }}>
              <div className="section-card">
                <h3 className="section-title">
                  <BarChart3 size={20} style={{ color: 'var(--accent)' }} />
                  Risk Distribution Overview
                </h3>
                {predictions && (
                  <div className="chart-box">
                    <ResponsiveContainer width="100%" height="300">
                      <PieChart>
                        <Pie
                          data={[
                            { name: 'Critical', value: predictions.summary?.high_risk_count || 0, color: '#f43f5e' },
                            { name: 'At-Risk', value: predictions.summary?.medium_risk_count || 0, color: '#f59e0b' },
                            { name: 'Stable', value: predictions.summary?.stable_count || 0, color: '#eab308' },
                            { name: 'Loyal', value: predictions.summary?.low_risk_count || 0, color: '#10b981' }
                          ]}
                          cx="50%"
                          cy="50%"
                          innerRadius={60}
                          outerRadius={100}
                          paddingAngle={5}
                          dataKey="value"
                        >
                          {[
                            { name: 'Critical', color: '#f43f5e' },
                            { name: 'At-Risk', color: '#f59e0b' },
                            { name: 'Stable', color: '#eab308' },
                            { name: 'Loyal', color: '#10b981' }
                          ].map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Pie>
                        <Tooltip />
                        <Legend />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                )}
              </div>

              <div className="section-card">
                <h3 className="section-title">
                  <Zap size={20} style={{ color: 'var(--accent)' }} />
                  Key Risk Factors
                </h3>
                <div className="space-y-4">
                  {features.slice(0, 4).map((f, i) => (
                    <div key={i} className="feature-item">
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                        <span style={{ fontSize: '0.8rem', fontWeight: '600' }}>{f.feature}</span>
                        <span style={{ fontSize: '0.75rem', color: 'var(--accent)', fontWeight: '700' }}>
                          {(f.importance * 100).toFixed(0)}%
                        </span>
                      </div>
                      <div style={{ height: '6px', background: 'rgba(255,255,255,0.1)', borderRadius: '3px' }}>
                        <div
                          style={{
                            height: '100%',
                            background: `linear-gradient(90deg, var(--accent), #818cf8)`,
                            width: `${f.importance * 100}%`,
                            borderRadius: '3px',
                            transition: 'width 0.5s ease'
                          }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'customers' && (
          <div className="space-y-6 animate-in">
            <div className="section-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
                <h3 className="section-title" style={{ margin: 0 }}>
                  <Users size={20} style={{ color: 'var(--accent)' }} />
                  Customer Risk Analysis
                </h3>

                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
                  {/* Search Bar */}
                  <div style={{ position: 'relative' }}>
                    <Users size={16} style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                    <input
                      type="text"
                      placeholder="Search Customer ID..."
                      className="form-input"
                      style={{ paddingLeft: '2.5rem', width: '220px', height: '40px' }}
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                  </div>

                  {/* Filter Buttons */}
                  <div style={{ display: 'flex', background: 'rgba(255,255,255,0.05)', borderRadius: '0.75rem', padding: '0.25rem' }}>
                    {['ALL', 'CRITICAL', 'AT-RISK', 'STABLE', 'LOYAL'].map(risk => (
                      <button
                        key={risk}
                        onClick={() => setFilterRisk(risk)}
                        style={{
                          padding: '0.5rem 1rem',
                          borderRadius: '0.5rem',
                          fontSize: '0.7rem',
                          fontWeight: '800',
                          cursor: 'pointer',
                          transition: 'all 0.2s',
                          border: 'none',
                          background: filterRisk === risk ? 'var(--accent)' : 'transparent',
                          color: filterRisk === risk ? '#fff' : 'var(--text-muted)'
                        }}
                      >
                        {risk}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              <div style={{ padding: '0 1.5rem 1rem', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Total Dataset: {predictions?.summary?.total_customers || 0} records identified.
              </div>
              <div className="data-table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Customer ID</th>
                      <th>Tenure</th>
                      <th>Monthly Charges</th>
                      <th>Churn Risk</th>
                      <th>Risk Level</th>
                      <th>Primary Reason</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(() => {
                      const filtered = (predictions?.predictions || [])
                        .filter(c => {
                          const matchesSearch = c.customer_id.toLowerCase().includes(searchTerm.toLowerCase());
                          const matchesRisk = filterRisk === 'ALL' || c.risk_level.toUpperCase() === filterRisk;
                          return matchesSearch && matchesRisk;
                        })
                        .sort((a, b) => b.churn_probability - a.churn_probability);

                      return (
                        <>
                          {filtered.slice(0, displayLimit).map((customer, i) => (
                            <tr key={i}>
                              <td style={{ fontFamily: 'JetBrains Mono', fontWeight: 'bold', color: 'var(--accent)' }}>
                                {customer.customer_id}
                              </td>
                              <td>{customer.tenure_months} months</td>
                              <td>${customer.monthly_charges.toFixed(2)}</td>
                              <td style={{ fontWeight: '900' }}>{customer.churn_probability.toFixed(1)}%</td>
                              <td>
                                <span className={`risk-badge risk-${customer.risk_color.toLowerCase()}`}>
                                  {customer.risk_level}
                                </span>
                              </td>
                              <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                                {customer.primary_reason}
                              </td>
                            </tr>
                          ))}
                          {filtered.length > displayLimit && (
                            <tr>
                              <td colSpan="6" style={{ textAlign: 'center', padding: '1.5rem' }}>
                                <button
                                  onClick={() => setDisplayLimit(prev => prev + 200)}
                                  className="btn-secondary"
                                  style={{ width: 'auto', padding: '0.5rem 2rem' }}
                                >
                                  Load More (Showing {displayLimit} of {filtered.length})
                                </button>
                              </td>
                            </tr>
                          )}
                        </>
                      );
                    })()}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'performance' && (
          <div className="space-y-6 animate-in">
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
              <div className="section-card">
                <h3 className="section-title">Model Performance Metrics</h3>
                <div className="chart-box">
                  <ResponsiveContainer width="100%" height="300">
                    <AreaChart data={rocData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                      <XAxis dataKey="x" stroke="var(--text-muted)" fontSize={10} />
                      <YAxis stroke="var(--text-muted)" fontSize={10} />
                      <Tooltip />
                      <Area type="monotone" dataKey="y" stroke="var(--accent)" fill="var(--accent-glow)" strokeWidth={3} />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
              <div className="section-card">
                <h3 className="section-title">Performance Summary</h3>
                <div className="metrics-grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))' }}>
                  <div className="metric-item">
                    <div className="metric-label">AUC Score</div>
                    <div className="metric-value">{(stats.auc_score * 100).toFixed(1)}%</div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-label">KS Statistic</div>
                    <div className="metric-value">{(stats.ks_stat || 0.512).toFixed(3)}</div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-label">Prediction Variance</div>
                    <div className="metric-value">{(predictions?.summary?.prediction_variance || 0).toFixed(4)}</div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-label">Model Engine</div>
                    <div className="metric-value" style={{ fontSize: '0.9rem' }}>{stats.engine || 'XGBoost Champion'}</div>
                  </div>
                  <div className="metric-item">
                    <div className="metric-label">Total Predictions</div>
                    <div className="metric-value">{predictions?.summary?.total_customers || 7043}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'benchmark' && (
          <div className="animate-in">
            <div className="section-card">
              <h3 className="section-title">
                <Binary size={20} style={{ color: 'var(--accent)' }} />
                Algorithm Performance Benchmarks
              </h3>
              <div className="data-table-wrapper">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>Algorithm</th>
                      <th style={{ display: 'flex', alignItems: 'center' }}>
                        ROC-AUC <MetricHelp title="ROC-AUC" description="Ability to distinguish between churners and loyalists. 1.0 is perfect." />
                      </th>
                      <th>
                        Variance <MetricHelp title="Performance Variance" description="The performance gap compared to the top-ranking Champion model." />
                      </th>
                      <th>
                        Accuracy <MetricHelp title="Accuracy" description="Percentage of total predictions that were correct." />
                      </th>
                      <th>
                        Precision <MetricHelp title="Precision" description="Of all predicted churners, how many actually churned? (Avoids false alarms)." />
                      </th>
                      <th>
                        Recall <MetricHelp title="Recall" description="Of all actual churners, how many did we catch? (No churner left behind)." />
                      </th>
                      <th>
                        F1-Score <MetricHelp title="F1-Score" description="Balance between Precision and Recall. Best overall performance metric." />
                      </th>
                      <th>Training Time</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(() => {
                      const championScore = benchmark[0]?.roc_auc || 1;
                      return benchmark.map((algo, i) => {
                        const variance = i === 0 ? 0 : ((algo.roc_auc - championScore) / championScore) * 100;
                        return (
                          <tr key={i}>
                            <td style={{ fontWeight: '800' }}>#{i + 1}</td>
                            <td style={{ fontWeight: '700' }}>{algo.algorithm}</td>
                            <td style={{ fontFamily: 'JetBrains Mono', color: 'var(--accent)' }}>
                              {(algo.roc_auc || 0).toFixed(4)}
                            </td>
                            <td style={{
                              color: i === 0 ? 'var(--success)' : 'var(--danger)',
                              fontSize: '0.75rem',
                              fontWeight: '700'
                            }}>
                              {i === 0 ? '0.00%' : `${variance.toFixed(2)}%`}
                            </td>
                            <td>{((algo.accuracy || 0) * 100).toFixed(1)}%</td>
                            <td>{((algo.precision || 0) * 100).toFixed(1)}%</td>
                            <td>{((algo.recall || 0) * 100).toFixed(1)}%</td>
                            <td>{((algo.f1_score || 0) * 100).toFixed(1)}%</td>
                            <td style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                              {(algo.training_time || 0).toFixed(2)}s
                            </td>
                            <td>
                              {i === 0 ? (
                                <span className="risk-badge risk-low">Champion</span>
                              ) : (
                                <span className="risk-badge risk-med">Verified</span>
                              )}
                            </td>
                          </tr>
                        );
                      });
                    })()}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

// --- SUB COMPONENTS ---

const NavLink = ({ icon, label, active, onClick }) => (
  <button className={`nav-link ${active ? 'active' : ''}`} onClick={onClick}>
    {icon} <span>{label}</span>
  </button>
);

const MetricHelp = ({ title, description }) => (
  <div className="metric-help-tooltip">
    <HelpCircle size={10} style={{ marginLeft: '4px', cursor: 'help', color: 'var(--text-muted)' }} />
    <div className="tooltip-content">
      <strong>{title}</strong>
      <p>{description}</p>
    </div>
  </div>
);

const SummaryTile = ({ label, val, icon, color }) => (
  <div className="card-tile">
    <div style={{ background: color + '15', color, width: '40px', height: '40px', borderRadius: '0.75rem', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1rem' }}>{icon}</div>
    <div style={{ fontSize: '1.75rem', fontWeight: '900', color: '#fff' }}>{val}</div>
    <div style={{ fontSize: '0.65rem', color: 'var(--text-muted)', fontWeight: '800', textTransform: 'uppercase' }}>{label}</div>
  </div>
);

export default App;
