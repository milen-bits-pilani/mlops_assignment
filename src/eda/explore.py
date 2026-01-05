"""
Exploratory Data Analysis for Heart Disease dataset
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def perform_eda(data_path: str, output_dir: str = "data/eda"):
    """
    Perform comprehensive EDA on Heart Disease dataset
    
    Args:
        data_path: Path to the dataset CSV
        output_dir: Directory to save visualizations
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load data
    df = pd.read_csv(data_path)
    
    # Convert target to binary
    df['target'] = (df['target'] > 0).astype(int)
    
    print("=" * 80)
    print("EXPLORATORY DATA ANALYSIS - Heart Disease Dataset")
    print("=" * 80)
    
    # Basic statistics
    print("\n1. Dataset Overview")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
    print(f"\n   First few rows:")
    print(df.head())
    
    print("\n2. Data Types and Missing Values")
    print(df.info())
    print(f"\n   Missing values per column:")
    print(df.isnull().sum())
    
    print("\n3. Statistical Summary")
    print(df.describe())
    
    print("\n4. Class Distribution")
    class_dist = df['target'].value_counts()
    print(class_dist)
    print(f"   Class balance: {class_dist[0] / len(df):.2%} (No Disease) vs {class_dist[1] / len(df):.2%} (Disease)")
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    
    # 1. Class Balance Visualization
    plt.figure(figsize=(8, 6))
    class_dist.plot(kind='bar', color=['skyblue', 'salmon'])
    plt.title('Class Distribution (Target Variable)', fontsize=16, fontweight='bold')
    plt.xlabel('Target (0=No Disease, 1=Disease)', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/class_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"\n   Saved: {output_dir}/class_distribution.png")
    
    # 2. Histograms for all numeric features
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    n_cols = 4
    n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
    axes = axes.flatten()
    
    for idx, col in enumerate(numeric_cols):
        axes[idx].hist(df[col].dropna(), bins=30, edgecolor='black', alpha=0.7)
        axes[idx].set_title(f'{col}', fontsize=10, fontweight='bold')
        axes[idx].set_xlabel('Value')
        axes[idx].set_ylabel('Frequency')
        axes[idx].grid(True, alpha=0.3)
    
    # Hide extra subplots
    for idx in range(len(numeric_cols), len(axes)):
        axes[idx].axis('off')
    
    plt.suptitle('Feature Distributions (Histograms)', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/feature_histograms.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {output_dir}/feature_histograms.png")
    
    # 3. Correlation Heatmap
    plt.figure(figsize=(14, 12))
    correlation_matrix = df[numeric_cols].corr()
    mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
    sns.heatmap(
        correlation_matrix,
        mask=mask,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        linewidths=1,
        cbar_kws={"shrink": 0.8}
    )
    plt.title('Correlation Heatmap of Features', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/correlation_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {output_dir}/correlation_heatmap.png")
    
    # 4. Feature distributions by target class
    key_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    n_features = len(key_features)
    
    fig, axes = plt.subplots(1, n_features, figsize=(20, 4))
    for idx, feature in enumerate(key_features):
        if feature in df.columns:
            df[df['target'] == 0][feature].hist(ax=axes[idx], alpha=0.5, label='No Disease', bins=20)
            df[df['target'] == 1][feature].hist(ax=axes[idx], alpha=0.5, label='Disease', bins=20)
            axes[idx].set_title(f'{feature}', fontweight='bold')
            axes[idx].set_xlabel('Value')
            axes[idx].set_ylabel('Frequency')
            axes[idx].legend()
            axes[idx].grid(True, alpha=0.3)
    
    plt.suptitle('Feature Distributions by Target Class', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/feature_distributions_by_class.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {output_dir}/feature_distributions_by_class.png")
    
    # 5. Box plots for key features
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    key_features_extended = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'cp']
    for idx, feature in enumerate(key_features_extended[:6]):
        if feature in df.columns:
            df.boxplot(column=feature, by='target', ax=axes[idx])
            axes[idx].set_title(f'{feature} by Target', fontweight='bold')
            axes[idx].set_xlabel('Target')
            axes[idx].set_ylabel(feature)
    
    plt.suptitle('Box Plots: Key Features by Target Class', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f"{output_dir}/boxplots_by_class.png", dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   Saved: {output_dir}/boxplots_by_class.png")
    
    print("\n" + "=" * 80)
    print("EDA Complete! All visualizations saved to", output_dir)
    print("=" * 80)


if __name__ == "__main__":
    import sys
    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/heart_disease.csv"
    perform_eda(data_path)

