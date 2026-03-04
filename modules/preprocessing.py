"""
Module: Preprocessing

Module này cung cấp các hàm tiền xử lý dữ liệu có thể cấu hình:
- Missing value imputation (SimpleImputer, KNNImputer)
- Categorical encoding (One-Hot, Label)
- Feature scaling (StandardScaler, MinMaxScaler)
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler, MinMaxScaler


def apply_imputation(df: pd.DataFrame, config: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Áp dụng imputation có thể cấu hình cho missing values.
    
    Args:
        df: DataFrame có missing values
        config: Dictionary cấu hình với các keys:
            - method: 'SimpleImputer' hoặc 'KNNImputer'
            - strategy: Cho SimpleImputer - 'mean', 'median', 'most_frequent'
            - n_neighbors: Cho KNNImputer - số lượng neighbors
    
    Returns:
        Tuple chứa:
            - DataFrame đã được impute
            - Dictionary chứa metadata về imputation
    
    TODO: Implement logic imputation
    - Phân tách numeric và categorical columns
    - Áp dụng imputation theo method được chọn
    - Log thông tin về missing values trước và sau
    - Trả về DataFrame và metadata
    """
    # TODO: Implement imputation logic
    print(f"[Preprocessing] TODO: Áp dụng imputation với method={config.get('method', 'SimpleImputer')}")
    pass


def apply_encoding(df: pd.DataFrame, config: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Áp dụng encoding có thể cấu hình cho categorical features.
    
    Args:
        df: DataFrame cần encode
        config: Dictionary cấu hình với các keys:
            - method: 'OneHot' hoặc 'Label'
            - drop_first: Cho OneHot - có drop first category không
    
    Returns:
        Tuple chứa:
            - DataFrame đã được encode
            - Dictionary chứa metadata về encoding
    
    TODO: Implement logic encoding
    - Phát hiện categorical columns
    - Áp dụng encoding theo method được chọn
    - Log thông tin về số features trước và sau
    - Lưu label mappings nếu dùng Label Encoding
    - Trả về DataFrame và metadata
    """
    # TODO: Implement encoding logic
    print(f"[Preprocessing] TODO: Áp dụng encoding với method={config.get('method', 'OneHot')}")
    pass


def apply_scaling(df: pd.DataFrame, config: Dict[str, Any]) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Áp dụng scaling có thể cấu hình cho numeric features.
    
    Args:
        df: DataFrame cần scale (nên là toàn numeric)
        config: Dictionary cấu hình với các keys:
            - method: 'StandardScaler' hoặc 'MinMaxScaler'
            - feature_range: Cho MinMaxScaler - tuple (min, max)
    
    Returns:
        Tuple chứa:
            - DataFrame đã được scale
            - Dictionary chứa metadata và fitted scaler
    
    TODO: Implement logic scaling
    - Đảm bảo tất cả columns là numeric
    - Áp dụng scaling theo method được chọn
    - Lưu fitted scaler để transform test data
    - Log thông tin về scaling parameters
    - Trả về DataFrame và metadata
    """
    # TODO: Implement scaling logic
    print(f"[Preprocessing] TODO: Áp dụng scaling với method={config.get('method', 'StandardScaler')}")
    pass


def preprocess_pipeline(df: pd.DataFrame, target_column: str, 
                       config: Dict[str, Any]) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Pipeline preprocessing hoàn chỉnh: imputation → encoding → scaling.
    
    Args:
        df: DataFrame gốc
        target_column: Tên cột target để tách ra
        config: Dictionary cấu hình với keys 'imputation', 'encoding', 'scaling'
    
    Returns:
        Tuple chứa:
            - X: Features đã được preprocess (numpy array)
            - y: Target values (numpy array)
            - metadata: Dictionary chứa tất cả preprocessing metadata
    
    TODO: Implement full preprocessing pipeline
    - Tách features và target
    - Gọi apply_imputation
    - Gọi apply_encoding
    - Gọi apply_scaling
    - Chuyển sang numpy array
    - Tổng hợp metadata
    """
    # TODO: Implement full preprocessing pipeline
    print("[Preprocessing] TODO: Chạy full preprocessing pipeline")
    pass


# TODO: Thêm các hàm utility khác nếu cần
# - Hàm lưu và load fitted transformers (scalers, encoders)
# - Hàm transform test data với fitted transformers
# - Hàm xử lý outliers
