import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from src.config import Config

def generate_production_figures(data_path):
    """Generates premium EDA figures for the production report."""
    if not os.path.exists(data_path):
        return
        
    df = pd.read_csv(data_path)
    sns.set_theme(style="whitegrid", palette="muted")
    
    # Figure 1: Risk Distribution
    plt.figure(figsize=(10, 6))
    df['Churn'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#45B39D', '#EC7063'])
    plt.title("Customer Retention Overview", fontsize=14, fontweight='bold')
    plt.savefig(os.path.join(Config.FIGURES_DIR, "retention_overview.png"), dpi=300)
    plt.close()

    # Figure 2: Tenure Risk
    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=df, x='tenure', hue='Churn', fill=True, palette=['#45B39D', '#EC7063'])
    plt.title("Churn Risk vs. Tenure (Months)", fontsize=14, fontweight='bold')
    plt.savefig(os.path.join(Config.FIGURES_DIR, "tenure_risk_distribution.png"), dpi=300)
    plt.close()
    
    print(f"✅ Figures generated in {Config.FIGURES_DIR}")
