"""
Module: Exploratory Data Analysis (EDA)

Module này cung cấp các hàm để phân tích mô tả và trực quan hóa dữ liệu.

Chức năng chính:
- Tạo báo cáo thống kê mô tả
- Vẽ correlation heatmap
- Vẽ biểu đồ missing values
- Vẽ phân phối class cho classification
"""

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
    pass


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
    pass


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
    print(f"[EDA] TODO: Vẽ phân phối class cho '{target_column}' và lưu vào {output_path}")
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
