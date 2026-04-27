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
    if X is None or not isinstance(X, np.ndarray):
        raise ValueError("[Features] X phải là numpy array.")
    if X.ndim != 2:
        raise ValueError("[Features] X phải là ma trận 2 chiều (n_samples, n_features).")

    variance_threshold = config.get("variance_threshold", 0.95)
    print(f"[Features] Áp dụng PCA với variance_threshold={variance_threshold}")
    
    pca = PCA(n_components=variance_threshold, svd_solver='full')
    X_pca = pca.fit_transform(X)
    
    explained = pca.explained_variance_ratio_
    cumulative = explained.cumsum()
    
    pca_info = {
        "variance_threshold": variance_threshold,
        "original_dim": X.shape[1],
        "reduced_dim": X_pca.shape[1],
        "explained_variance_ratio": explained,
        "cumulative_variance": cumulative,
        "n_components": pca.n_components_
        #"pca_model": pca 
    }
    
    print(f"[Features] PCA completed: {X.shape[1]} -> {X_pca.shape[1]} dimensions")
    print(f"[Features] Cumulative explained variance: {cumulative[-1]:.4f}")
    return X_pca, pca_info

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
    
    format_type = config.get('format', 'npy')
    base_path = config.get("path", "features/processed_features")

    # Tạo thư mục nếu chưa tồn tại
    dir_name = os.path.dirname(base_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)

    if format_type == "npy":
        x_path = f"{base_path}_X.npy"
        y_path = f"{base_path}_y.npy"
        np.save(x_path, X)
        np.save(y_path, y)
        print(f"[Features] Đã lưu X vào: {x_path}")
        print(f"[Features] Đã lưu y vào: {y_path}")
        return base_path

    elif format_type == "h5":
        h5_path = f"{base_path}.h5"
        with h5py.File(h5_path, "w") as f:
            f.create_dataset("X", data=X)
            f.create_dataset("y", data=y)
        print(f"[Features] Đã lưu X,y vào: {h5_path}")
        return h5_path

    else:
        raise ValueError(f"[Features] Format '{format_type}' không được hỗ trợ.")


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
    if format_type == "npy":
        x_path = f"{file_path}_X.npy"
        y_path = f"{file_path}_y.npy"
        if not os.path.exists(x_path) or not os.path.exists(y_path):
            raise FileNotFoundError("[Features] Không tìm thấy file .npy cần load.")
        X = np.load(x_path, allow_pickle=False)
        y = np.load(y_path, allow_pickle=False)
        print(f"[Features] Đã load X từ: {x_path}")
        print(f"[Features] Đã load y từ: {y_path}")
        return X, y

    elif format_type == "h5":
        h5_path = f"{file_path}.h5"
        if not os.path.exists(h5_path):
            raise FileNotFoundError("[Features] Không tìm thấy file .h5 cần load.")
        with h5py.File(h5_path, "r") as f:
            X = f["X"][:]
            y = f["y"][:]
        print(f"[Features] Đã load X,y từ: {h5_path}")
        return X, y

    else:
        raise ValueError(f"[Features] Format '{format_type}' không được hỗ trợ.")

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
    pca_config = config.get("pca", {})
    pca_enabled = pca_config.get("enabled", False)
    
    if pca_enabled:
        X_out, pca_meta = apply_pca(X, pca_config)
    else:
        print("PCA bị tắt trong config, giữ nguên X")
        X_out = X
        pca_meta = {}
    metadata = {"pca": pca_meta}
    return X_out, metadata


# TODO: Thêm các hàm feature engineering khác nếu cần
# - Feature selection (SelectKBest, RFE, etc.)
# - Feature interaction (polynomial, cross features)
# - Feature binning/discretization
