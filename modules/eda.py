"""
Module: Exploratory Data Analysis (EDA)

Module này cung cấp các hàm để phân tích mô tả và trực quan hóa dữ liệu.

Chức năng chính:
- Tạo báo cáo thống kê mô tả
- Vẽ correlation heatmap
- Vẽ biểu đồ missing values
- Vẽ phân phối class cho classification
"""

import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, Dict, Any


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
    print("[EDA] TODO: Tạo báo cáo thống kê mô tả")

    # 1. Phân loại numeric/categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    # 2. Phân tích missing values
    missing_values = df.isnull().sum()
    missing_dict = missing_values[missing_values > 0].to_dict()

    # Ghi nhận riêng các cột cần chú ý (như bạn yêu cầu ở task trước)
    cols_to_check = ['agent', 'company', 'children']
    specific_missing = {
        col: int(df[col].isnull().sum())
        for col in cols_to_check if col in df.columns
    }

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
    print(f"[EDA] TODO: Vẽ biểu đồ missing values và lưu vào {output_path}")
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
