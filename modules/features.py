"""
Module: Feature Engineering

Module này cung cấp các hàm cho feature engineering và dimensionality reduction:
- PCA với configurable variance threshold
- Lưu và load features artifacts (.npy, .h5)
"""

import numpy as np
import pandas as pd
import h5py
from typing import Dict, Any, Tuple, Optional
from sklearn.decomposition import PCA


def apply_pca(X: np.ndarray, config: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Áp dụng PCA để giảm chiều dữ liệu theo ngưỡng explained variance.
    
    Args:
        X: Feature matrix (numpy array)
        config: Dictionary cấu hình với keys:
            - variance_threshold: Ngưỡng explained variance (ví dụ: 0.90, 0.95)
    
    Returns:
        Tuple chứa:
            - X_pca: Features đã giảm chiều
            - pca_info: Dictionary chứa thông tin về PCA
    
    TODO: Implement PCA
    - Fit PCA với n_components để đạt variance threshold
    - Transform dữ liệu
    - Log số chiều trước và sau
    - Log explained variance ratio
    - Trả về features và metadata
    """
    # TODO: Implement PCA logic
    print(f"[Features] TODO: Áp dụng PCA với variance_threshold={config.get('variance_threshold', 0.95)}")
    pass


def save_features(X: np.ndarray, y: np.ndarray, config: Dict[str, Any]) -> str:
    """
    Lưu processed features ra file (.npy hoặc .h5).
    
    Args:
        X: Feature matrix
        y: Target vector
        config: Dictionary cấu hình với keys:
            - format: 'npy' hoặc 'h5'
            - path: Đường dẫn base để lưu (không có extension)
    
    Returns:
        Đường dẫn đến file đã lưu
    
    TODO: Implement save logic
    - Tạo thư mục nếu chưa tồn tại
    - Lưu theo format được chọn:
        + Nếu .npy: Lưu X và y thành 2 file riêng
        + Nếu .h5: Lưu X và y trong cùng 1 file HDF5
    - Log thông tin về file đã lưu
    - Trả về đường dẫn
    """
    # TODO: Implement save logic
    format_type = config.get('format', 'npy')
    print(f"[Features] TODO: Lưu features với format={format_type}")
    pass


def load_features(file_path: str, format_type: str = 'npy') -> Tuple[np.ndarray, np.ndarray]:
    """
    Load processed features từ file.
    
    Args:
        file_path: Đường dẫn đến file (không có extension cho .npy)
        format_type: 'npy' hoặc 'h5'
    
    Returns:
        Tuple chứa (X, y)
    
    Raises:
        FileNotFoundError: Nếu file không tồn tại
    
    TODO: Implement load logic
    - Kiểm tra file tồn tại
    - Load theo format:
        + Nếu .npy: Load X và y từ 2 file riêng
        + Nếu .h5: Load X và y từ HDF5 file
    - Validate shape và dtype
    - Trả về X và y
    """
    # TODO: Implement load logic
    print(f"[Features] TODO: Load features từ {file_path} với format={format_type}")
    pass


def engineer_features(X: np.ndarray, config: Dict[str, Any]) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Pipeline feature engineering hoàn chỉnh.
    
    Args:
        X: Feature matrix gốc
        config: Dictionary cấu hình feature engineering
    
    Returns:
        Tuple chứa:
            - X_engineered: Features đã được engineer
            - metadata: Dictionary chứa thông tin về feature engineering
    
    TODO: Implement feature engineering pipeline
    - Kiểm tra PCA có enabled không
    - Nếu có, apply PCA
    - Có thể thêm các bước feature engineering khác:
        + Feature selection
        + Feature interaction
        + Polynomial features
    - Trả về features và metadata
    """
    # TODO: Implement feature engineering pipeline
    print("[Features] TODO: Chạy feature engineering pipeline")
    pass


# TODO: Thêm các hàm feature engineering khác nếu cần
# - Feature selection (SelectKBest, RFE, etc.)
# - Feature interaction (polynomial, cross features)
# - Feature binning/discretization
