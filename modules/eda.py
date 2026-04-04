"""
Module: Exploratory Data Analysis (EDA)

Module này cung cấp các hàm để phân tích mô tả và trực quan hóa dữ liệu.

Chức năng chính:
- Tạo báo cáo thống kê mô tả
- Vẽ correlation heatmap
- Vẽ biểu đồ missing values
- Vẽ phân phối class cho classification
- Phân tích categorical features và tương quan với target
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
from typing import Optional, Dict, Any, List
import os


def generate_eda_report(df: pd.DataFrame, output_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    Tạo báo cáo thống kê mô tả toàn diện cho dataset.

    Args:
        df: DataFrame cần phân tích
        output_dir: Thư mục lưu báo cáo (optional)

    Returns:
        Dictionary chứa các thống kê tóm tắt

    TODO: Implement logic tạo báo cáo
    - Tính toán thống kê mô tả (describe)
    - Phân tích missing values
    - Phân loại numeric/categorical columns
    - Tính unique values cho mỗi cột
    - Lưu báo cáo ra file nếu có output_dir
    """
    # TODO: Implement EDA report generation
    print("[EDA] Tạo báo cáo thống kê mô tả")

    # 1. Phân loại numeric/categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    # 2. Phân tích missing values
    missing_values = df.isnull().sum()
    missing_dict = missing_values[missing_values > 0].to_dict()

    specific_missing = {col: int(count) for col, count in missing_dict.items()}

    # 3. Tính unique values cho mỗi cột
    unique_values = df.nunique().to_dict()

    # 4. Tính toán thống kê mô tả (describe)
    # Bao gồm cả numeric và categorical
    describe_stats = df.describe(include='all').to_dict()

    # Tổng hợp báo cáo thành Dictionary
    report = {
        "dataset_info": {
            "total_rows": len(df),
            "total_columns": len(df.columns)
        },
        "column_classification": {
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols
        },
        "missing_values_analysis": {
            "all_missing": missing_dict,
            "target_columns_missing": specific_missing
        },
        "unique_values_count": unique_values,
        "descriptive_statistics": describe_stats
    }

    # 5. Lưu báo cáo ra file nếu có output_dir
    if output_dir:
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, "eda_report.json")

        # Xử lý các kiểu dữ liệu không mặc định serialize được (ví dụ: np.int64, float NaN)
        def json_converter(obj):
            if pd.isna(obj):
                return None
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj) if isinstance(obj, np.floating) else int(obj)
            return str(obj)

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False,
                      default=json_converter)

        print(f"[EDA] Đã lưu báo cáo thống kê mô tả tại: {report_path}")
    else:
        print("[EDA] Hoàn tất tạo báo cáo (không lưu file do không có output_dir).")

    return report


def plot_correlation_heatmap(df: pd.DataFrame, output_path: str,
                             figsize: tuple = (12, 10)) -> str:
    """
    Vẽ và lưu correlation heatmap cho các cột numeric.

    Args:
        df: DataFrame cần phân tích
        output_path: Đường dẫn lưu hình ảnh heatmap
        figsize: Kích thước figure (mặc định: (12, 10))

    Returns:
        Đường dẫn đến file hình ảnh đã lưu

    TODO: Implement logic vẽ heatmap
    - Chọn các cột numeric
    - Tính correlation matrix
    - Vẽ heatmap với seaborn
    - Lưu hình ảnh với DPI cao
    """
    # TODO: Implement correlation heatmap
    print(f"[EDA] TODO: Vẽ correlation heatmap và lưu vào {output_path}")
    pass


def plot_missing_values(df: pd.DataFrame, output_path: str,
                        figsize: tuple = (12, 8)) -> str:
    """
    Vẽ và lưu biểu đồ phân tích missing values.

    Args:
        df: DataFrame cần phân tích
        output_path: Đường dẫn lưu hình ảnh
        figsize: Kích thước figure (mặc định: (12, 8))

    Returns:
        Đường dẫn đến file hình ảnh đã lưu

    TODO: Implement logic vẽ missing values chart
    - Tính số lượng missing values cho mỗi cột
    - Tính phần trăm missing
    - Vẽ bar chart hiển thị missing values
    - Lưu hình ảnh
    """
    # TODO: Implement missing values visualization
    print(f"[EDA] Vẽ biểu đồ missing values và lưu vào {output_path}")
    print(f"[EDA] Đang vẽ biểu đồ missing values và lưu vào {output_path}...")

    # 1. Tính số lượng missing values cho mỗi cột
    missing_counts = df.isnull().sum()

    # Chỉ giữ lại các cột thực sự có giá trị thiếu và sắp xếp giảm dần
    missing_counts = missing_counts[missing_counts > 0].sort_values(
        ascending=False)

    # Nếu không có dữ liệu thiếu, thông báo và bỏ qua vẽ
    if missing_counts.empty:
        print("[EDA] Dataset không có giá trị missing nào. Bỏ qua vẽ biểu đồ.")
        return ""

    # 2. Tính phần trăm missing
    missing_percentage = (missing_counts / len(df)) * 100

    # 3. Vẽ bar chart hiển thị missing values
    plt.figure(figsize=figsize)

    # Sử dụng seaborn để vẽ barplot
    ax = sns.barplot(x=missing_counts.index,
                     y=missing_counts.values, palette="viridis")

    # Cấu hình tiêu đề và nhãn
    plt.title('Số lượng và Phần trăm Dữ liệu Thiếu theo Cột',
              fontsize=16, pad=20)
    plt.xlabel('Tên Cột', fontsize=12)
    plt.ylabel('Số lượng Missing Values', fontsize=12)
    plt.xticks(rotation=45, ha='right')  # Xoay chữ ở trục x để dễ đọc

    # Thêm text hiển thị phần trăm lên đỉnh mỗi cột
    for i, count in enumerate(missing_counts.values):
        percent_text = f'{missing_percentage.iloc[i]:.1f}%'
        ax.text(i, count + (count * 0.01), percent_text,
                ha='center', va='bottom', fontsize=10)

    plt.tight_layout()

    # 4. Lưu hình ảnh
    # Tạo thư mục chứa file nếu chưa tồn tại
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()  # Đóng figure để giải phóng bộ nhớ

    print(f"[EDA] Hoàn tất lưu biểu đồ tại: {output_path}")
    return output_path


def plot_class_distribution(df: pd.DataFrame, target_column: str,
                            output_path: str, figsize: tuple = (10, 6)) -> str:
    """
    Vẽ và lưu biểu đồ phân phối class cho biến target.

    Args:
        df: DataFrame chứa dữ liệu
        target_column: Tên cột target
        output_path: Đường dẫn lưu hình ảnh
        figsize: Kích thước figure (mặc định: (10, 6))

    Returns:
        Đường dẫn đến file hình ảnh đã lưu

    Raises:
        ValueError: Nếu target column không tồn tại

    TODO: Implement logic vẽ class distribution
    - Kiểm tra target column tồn tại
    - Tính số lượng và phần trăm mỗi class
    - Vẽ bar chart và pie chart
    - Cảnh báo nếu có class imbalance
    - Lưu hình ảnh
    """
    # TODO: Implement class distribution visualization
    print(
        f"[EDA] TODO: Vẽ phân phối class cho '{target_column}' và lưu vào {output_path}")
    pass


def run_full_eda(df: pd.DataFrame, target_column: str, output_dir: str) -> Dict[str, Any]:
    """
    Chạy pipeline EDA hoàn chỉnh với tất cả visualizations.

    Args:
        df: DataFrame cần phân tích
        target_column: Tên cột target
        output_dir: Thư mục lưu tất cả outputs

    Returns:
        Dictionary chứa báo cáo và đường dẫn đến các visualizations

    TODO: Implement full EDA pipeline
    - Tạo thư mục output nếu chưa tồn tại
    - Gọi generate_eda_report
    - Gọi plot_correlation_heatmap
    - Gọi plot_missing_values
    - Gọi plot_class_distribution
    - Tổng hợp kết quả
    """
    # TODO: Implement full EDA pipeline
    print("[EDA] TODO: Chạy full EDA pipeline")
    pass


# TODO: Thêm các hàm visualization khác nếu cần
# - Histogram cho numeric features
# - Box plot để phát hiện outliers
# - Scatter plot cho feature relationships


# ============ CATEGORICAL FEATURES EDA ============

def analyze_categorical_features_distribution(df: pd.DataFrame, 
                                              categorical_columns: Optional[List[str]] = None,
                                              output_dir: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """
    Phân tích distribution của categorical features.
    
    Args:
        df: DataFrame cần phân tích
        categorical_columns: Danh sách các cột categorical (nếu None thì auto-detect)
        output_dir: Thư mục lưu báo cáo (optional)
    
    Returns:
        Dictionary chứa thông tin distribution cho mỗi categorical column
        Ví dụ:
        {
            'hotel': {
                'unique_values': 2,
                'value_counts': {'Resort Hotel': 50000, 'City Hotel': 50000},
                'missing_percentage': 0.0
            },
            'meal': {...}
        }
    """
    # Auto-detect categorical columns nếu không được cung cấp
    if categorical_columns is None:
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    
    analysis_results = {}
    
    for col in categorical_columns:
        if col not in df.columns:
            print(f"[WARNING] Column '{col}' not found in DataFrame")
            continue
        
        missing_count = df[col].isna().sum()
        missing_percentage = (missing_count / len(df)) * 100
        
        value_counts = df[col].value_counts(dropna=False).to_dict()
        
        analysis_results[col] = {
            'unique_values': df[col].nunique(),
            'value_counts': value_counts,
            'missing_count': missing_count,
            'missing_percentage': missing_percentage,
            'most_common': df[col].value_counts().index[0] if len(df[col].value_counts()) > 0 else None,
            'least_common': df[col].value_counts().index[-1] if len(df[col].value_counts()) > 0 else None
        }
    
    # Lưu báo cáo nếu có output_dir
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        report_text = "CATEGORICAL FEATURES DISTRIBUTION ANALYSIS\n"
        report_text += "=" * 80 + "\n\n"
        
        for col, stats in analysis_results.items():
            report_text += f"Column: {col}\n"
            report_text += f"  - Unique values: {stats['unique_values']}\n"
            report_text += f"  - Missing: {stats['missing_count']} ({stats['missing_percentage']:.2f}%)\n"
            report_text += f"  - Most common: {stats['most_common']}\n"
            report_text += f"  - Least common: {stats['least_common']}\n"
            report_text += f"  - Value counts:\n"
            for val, count in stats['value_counts'].items():
                pct = (count / len(df)) * 100
                report_text += f"      {val}: {count} ({pct:.2f}%)\n"
            report_text += "\n"
        
        report_path = os.path.join(output_dir, "categorical_distribution_analysis.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"[INFO] Categorical distribution report saved to {report_path}")
    
    return analysis_results


def cramers_v(x: pd.Series, y: pd.Series) -> float:
    """
    Tính Cramér's V - measure of association giữa hai categorical variables.
    
    Giá trị từ 0 (no association) đến 1 (perfect association).
    """
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    min_dim = min(confusion_matrix.shape) - 1
    
    if min_dim == 0:
        return 0.0
    
    return np.sqrt(chi2 / (n * min_dim))


def analyze_categorical_target_relationship(df: pd.DataFrame, 
                                            target_column: str,
                                            categorical_columns: Optional[List[str]] = None,
                                            output_dir: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """
    Phân tích mối quan hệ giữa categorical features và target variable.
    
    Tính:
    - Cancellation rate cho mỗi category
    - Chi-square test p-value
    - Cramér's V (measure of association)
    
    Args:
        df: DataFrame cần phân tích
        target_column: Tên cột target (biến phân loại)
        categorical_columns: Danh sách các cột categorical (nếu None thì auto-detect)
        output_dir: Thư mục lưu báo cáo (optional)
    
    Returns:
        Dictionary chứa relationship analysis cho mỗi categorical column
    """
    if categorical_columns is None:
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        # Loại bỏ target column khỏi danh sách
        if target_column in categorical_columns:
            categorical_columns.remove(target_column)
    
    relationship_results = {}
    
    for col in categorical_columns:
        if col not in df.columns or col == target_column:
            continue
        
        # Tính crosstab
        crosstab = pd.crosstab(df[col], df[target_column], margins=True)
        
        # Tính tỷ lệ cancellation cho mỗi category
        cancellation_rate_by_category = df.groupby(col)[target_column].agg(['count', 'sum', 'mean'])
        cancellation_rate_by_category.columns = ['total_bookings', 'cancellations', 'cancellation_rate']
        
        # Chi-square test
        try:
            chi2, p_value, dof, expected = chi2_contingency(pd.crosstab(df[col], df[target_column]))
            cramers = cramers_v(df[col].dropna(), df[target_column])
        except:
            p_value = np.nan
            cramers = np.nan
            chi2 = np.nan
        
        relationship_results[col] = {
            'chi2_statistic': chi2,
            'p_value': p_value,
            'cramers_v': cramers,
            'cancellation_by_category': cancellation_rate_by_category.to_dict(),
            'crosstab': crosstab
        }
    
    # Lưu báo cáo nếu có output_dir
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        report_text = "CATEGORICAL FEATURES - TARGET RELATIONSHIP ANALYSIS\n"
        report_text += "=" * 80 + "\n\n"
        
        for col, stats in relationship_results.items():
            report_text += f"Column: {col}\n"
            report_text += f"  - Chi-square statistic: {stats['chi2_statistic']:.4f}\n"
            report_text += f"  - P-value: {stats['p_value']:.6f}\n"
            report_text += f"  - Cramér's V: {stats['cramers_v']:.4f}\n"
            report_text += f"  - Cancellation rate by category:\n"
            
            cancelation_dict = stats['cancellation_by_category']
            for idx, (cat_val, metrics) in enumerate(zip(
                cancelation_dict['total_bookings'].keys(),
                zip(cancelation_dict['total_bookings'].values(),
                    cancelation_dict['cancellations'].values(),
                    cancelation_dict['cancellation_rate'].values())
            )):
                total, cancel, rate = metrics
                report_text += f"      {cat_val}: {total} bookings, {cancel} cancellations ({rate*100:.2f}%)\n"
            report_text += "\n"
        
        report_path = os.path.join(output_dir, "categorical_target_analysis.txt")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"[INFO] Categorical-target relationship report saved to {report_path}")
    
    return relationship_results


def plot_categorical_distribution(df: pd.DataFrame, 
                                  column: str,
                                  output_path: Optional[str] = None,
                                  figsize: tuple = (12, 6)) -> Optional[str]:
    """
    Vẽ countplot cho một categorical feature.
    
    Args:
        df: DataFrame chứa dữ liệu
        column: Tên cột categorical
        output_path: Đường dẫn lưu hình ảnh (optional)
        figsize: Kích thước figure
    
    Returns:
        Đường dẫn đến file hình ảnh đã lưu (hoặc None nếu không save)
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Sort by value counts để dễ đọc
    value_counts = df[column].value_counts()
    ax = sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax, palette='viridis')
    
    ax.set_title(f'Distribution of {column}', fontsize=14, fontweight='bold')
    ax.set_xlabel(column, fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    
    # Rotate x labels nếu có quá nhiều categories
    if len(value_counts) > 10:
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Thêm values trên top của bars
    for i, v in enumerate(value_counts.values):
        ax.text(i, v + max(value_counts.values)*0.01, str(v), ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"[INFO] Categorical distribution plot saved to {output_path}")
    
    plt.close()
    return output_path


def plot_categorical_with_target(df: pd.DataFrame,
                                 categorical_column: str,
                                 target_column: str,
                                 output_path: Optional[str] = None,
                                 figsize: tuple = (12, 6)) -> Optional[str]:
    """
    Vẽ barplot showing cancellation rate (hoặc target distribution) per category.
    
    Args:
        df: DataFrame chứa dữ liệu
        categorical_column: Tên cột categorical feature
        target_column: Tên cột target
        output_path: Đường dẫn lưu hình ảnh
        figsize: Kích thước figure
    
    Returns:
        Đường dẫn đến file hình ảnh đã lưu
    """
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    
    # Plot 1: Stacked bar chart (total bookings and cancellations)
    crosstab = pd.crosstab(df[categorical_column], df[target_column])
    crosstab.plot(kind='bar', stacked=True, ax=axes[0], color=['#2ecc71', '#e74c3c'])
    axes[0].set_title(f'Booking Status by {categorical_column}', fontsize=12, fontweight='bold')
    axes[0].set_xlabel(categorical_column, fontsize=11)
    axes[0].set_ylabel('Count', fontsize=11)
    axes[0].legend(['Not Canceled', 'Canceled'], loc='upper right')
    axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=45, ha='right')
    
    # Plot 2: Cancellation rate per category
    cancel_rate = df.groupby(categorical_column)[target_column].mean() * 100
    ax = axes[1]
    cancel_rate.plot(kind='bar', ax=ax, color='#e67e22')
    ax.set_title(f'Cancellation Rate by {categorical_column}', fontsize=12, fontweight='bold')
    ax.set_xlabel(categorical_column, fontsize=11)
    ax.set_ylabel('Cancellation Rate (%)', fontsize=11)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Thêm values trên top của bars
    for i, v in enumerate(cancel_rate.values):
        ax.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"[INFO] Categorical-target plot saved to {output_path}")
    
    plt.close()
    return output_path


def plot_categorical_association_heatmap(analysis_results: Dict[str, Dict[str, Any]],
                                         output_path: Optional[str] = None,
                                         figsize: tuple = (10, 8)) -> Optional[str]:
    """
    Vẽ heatmap showing Cramér's V values (association strength) giữa
    categorical features và target variable.
    
    Args:
        analysis_results: Dictionary từ analyze_categorical_target_relationship()
        output_path: Đường dẫn lưu hình ảnh
        figsize: Kích thước figure
    
    Returns:
        Đường dẫn đến file hình ảnh đã lưu
    """
    if not analysis_results:
        print("[WARNING] No analysis results to plot")
        return None
    
    # Extract Cramér's V values
    cramers_data = {col: stats['cramers_v'] for col, stats in analysis_results.items()}
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Sort by association strength
    sorted_data = dict(sorted(cramers_data.items(), key=lambda x: x[1], reverse=True))
    
    # Create horizontal bar chart
    ax.barh(list(sorted_data.keys()), list(sorted_data.values()), color='#3498db')
    ax.set_xlabel("Cramér's V (Association Strength)", fontsize=12)
    ax.set_title("Categorical Features - Target Association Strength", fontsize=14, fontweight='bold')
    ax.set_xlim(0, 1)
    
    # Add values on bars
    for i, (col, v) in enumerate(sorted_data.items()):
        ax.text(v + 0.02, i, f'{v:.4f}', va='center', fontsize=10)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"[INFO] Association heatmap saved to {output_path}")
    
    plt.close()
    return output_path


def run_categorical_eda(df: pd.DataFrame,
                        target_column: str,
                        categorical_columns: Optional[List[str]] = None,
                        output_dir: str = 'reports/eda/') -> Dict[str, Any]:
    """
    Chạy toàn bộ categorical EDA pipeline.
    
    Args:
        df: DataFrame cần phân tích
        target_column: Tên cột target
        categorical_columns: Danh sách categorical columns (nếu None thì auto-detect)
        output_dir: Thư mục lưu outputs
    
    Returns:
        Dictionary chứa tất cả results và paths to outputs
    """
    print("[INFO] Starting Categorical EDA Pipeline...")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Analyze distribution
    print("[STEP 1] Analyzing categorical distribution...")
    dist_results = analyze_categorical_features_distribution(
        df, categorical_columns, output_dir
    )
    
    # Determine categorical columns if not provided
    if categorical_columns is None:
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        if target_column in categorical_columns:
            categorical_columns.remove(target_column)
    
    # Step 2: Analyze target relationship
    print("[STEP 2] Analyzing categorical features - target relationship...")
    relationship_results = analyze_categorical_target_relationship(
        df, target_column, categorical_columns, output_dir
    )
    
    # Step 3: Generate visualizations
    print("[STEP 3] Generating visualizations...")
    
    # Individual categorical distributions
    for col in categorical_columns:
        if col in df.columns:
            plot_categorical_distribution(
                df, col,
                output_path=os.path.join(output_dir, f'cat_dist_{col}.png')
            )
    
    # Categorical with target
    for col in categorical_columns:
        if col in df.columns:
            plot_categorical_with_target(
                df, col, target_column,
                output_path=os.path.join(output_dir, f'cat_target_{col}.png')
            )
    
    # Association heatmap
    plot_categorical_association_heatmap(
        relationship_results,
        output_path=os.path.join(output_dir, 'categorical_association_heatmap.png')
    )
    
    print(f"[INFO] Categorical EDA completed! Results saved to {output_dir}")
    
    return {
        'distribution_analysis': dist_results,
        'target_relationship': relationship_results,
        'output_directory': output_dir
    }
