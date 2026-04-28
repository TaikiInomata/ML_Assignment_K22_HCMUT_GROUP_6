"""
Module: Feature Engineering

Module này cung cấp các hàm cho feature engineering và dimensionality reduction:
- PCA với configurable variance threshold
- Lưu và load features artifacts (.npy, .h5)
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Tuple

import h5py
import numpy as np
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
    variance_threshold = float(config.get('variance_threshold', 0.95))
    if X.size == 0:
        raise ValueError('[Features] Input X rỗng, không thể áp dụng PCA.')

    print(f"[Features] Áp dụng PCA với variance_threshold={variance_threshold}")
    pca = PCA(n_components=variance_threshold, svd_solver='full')
    X_pca = pca.fit_transform(X)

    explained_variance_ratio = pca.explained_variance_ratio_.tolist()
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_).tolist()

    print(f"[Features] PCA hoàn tất: {X.shape[1]} → {X_pca.shape[1]} components")
    print(f"[Features] Tổng explained variance: {float(np.sum(pca.explained_variance_ratio_)):.4f}")

    pca_info = {
        'enabled': True,
        'variance_threshold': variance_threshold,
        'n_components': int(pca.n_components_),
        'input_dim': int(X.shape[1]),
        'output_dim': int(X_pca.shape[1]),
        'explained_variance_ratio': explained_variance_ratio,
        'cumulative_variance': cumulative_variance,
        'pca_model': pca,
    }
    return X_pca, pca_info

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
    format_type = config.get('format', 'npy').lower()
    base_path = Path(config.get('path', 'features/processed_features'))
    base_path.parent.mkdir(parents=True, exist_ok=True)

    if format_type == 'npy':
        x_path = base_path.with_name(f'{base_path.name}_X.npy')
        y_path = base_path.with_name(f'{base_path.name}_y.npy')
        np.save(x_path, X)
        np.save(y_path, y)
        print(f"[Features] Đã lưu X tại: {x_path}")
        print(f"[Features] Đã lưu y tại: {y_path}")
        return str(base_path)

    if format_type == 'h5':
        h5_path = base_path.with_suffix('.h5')
        with h5py.File(h5_path, 'w') as h5_file:
            h5_file.create_dataset('X', data=X, compression='gzip')
            h5_file.create_dataset('y', data=y, compression='gzip')
            h5_file.attrs['x_shape'] = X.shape
            h5_file.attrs['y_shape'] = y.shape
        print(f"[Features] Đã lưu features tại: {h5_path}")
        return str(h5_path)

    raise ValueError("[Features] format phải là 'npy' hoặc 'h5'.")


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
    format_type = format_type.lower()
    base_path = Path(file_path)

    if format_type == 'npy':
        x_path = base_path.with_name(f'{base_path.name}_X.npy')
        y_path = base_path.with_name(f'{base_path.name}_y.npy')
        if not x_path.exists() or not y_path.exists():
            raise FileNotFoundError(f"[Features] Không tìm thấy file .npy tại {x_path} hoặc {y_path}")
        X = np.load(x_path, allow_pickle=False)
        y = np.load(y_path, allow_pickle=False)
        return X, y

    if format_type == 'h5':
        h5_path = base_path if base_path.suffix == '.h5' else base_path.with_suffix('.h5')
        if not h5_path.exists():
            raise FileNotFoundError(f"[Features] Không tìm thấy file .h5 tại {h5_path}")
        with h5py.File(h5_path, 'r') as h5_file:
            X = h5_file['X'][()]
            y = h5_file['y'][()]
        return X, y

    raise ValueError("[Features] format_type phải là 'npy' hoặc 'h5'.")

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
    print("[Features] Chạy feature engineering pipeline")

    metadata: Dict[str, Any] = {
        'pca': {
            'enabled': False,
            'n_components': None,
        },
        'output': config.get('output', {}),
    }

    X_engineered = np.asarray(X)
    pca_config = config.get('pca', {})

    if pca_config.get('enabled', False):
        X_engineered, pca_info = apply_pca(X_engineered, pca_config)
        metadata['pca'] = pca_info

    output_config = config.get('output', {})
    metadata['saved_path'] = None
    if output_config:
        y_placeholder = np.zeros(X_engineered.shape[0], dtype=np.int64)
        metadata['saved_path'] = save_features(X_engineered, y_placeholder, output_config)

    return X_engineered, metadata


# TODO: Thêm các hàm feature engineering khác nếu cần
# - Feature selection (SelectKBest, RFE, etc.)
# - Feature interaction (polynomial, cross features)
# - Feature binning/discretization
