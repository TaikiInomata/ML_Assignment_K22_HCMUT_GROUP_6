"""
Module: Preprocessing

Module này cung cấp các hàm tiền xử lý dữ liệu có thể cấu hình:
- Missing value imputation (SimpleImputer, KNNImputer)
- Categorical encoding (One-Hot, Label)
- Feature scaling (StandardScaler, MinMaxScaler)
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple, Optional
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split


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
    df_imputed = df.copy()

    # Ghi nhận số lượng missing values trước khi xử lý
    missing_before = df_imputed.isnull().sum()
    missing_before = missing_before[missing_before > 0].to_dict()

    # --- ĐOẠN CODE BỔ SUNG: XỬ LÝ CÁC CỘT ĐẶC BIỆT DỰA TRÊN EDA ---
    # 1. Xóa các cột được chỉ định (như 'company')
    drop_cols = config.get('drop_columns', [])
    if drop_cols:
        cols_to_drop = [col for col in drop_cols if col in df_imputed.columns]
        df_imputed = df_imputed.drop(columns=cols_to_drop)
        print(
            f"[Preprocessing] Đã xoá các cột do missing values quá cao: {cols_to_drop}")

    # 2. Điền hằng số cho các cột đặc biệt (như 'agent')
    constant_fill = config.get('constant_fill', {})
    for col, value in constant_fill.items():
        if col in df_imputed.columns and df_imputed[col].isnull().sum() > 0:
            df_imputed[col] = df_imputed[col].fillna(value)
            print(
                f"[Preprocessing] Đã điền giá trị {value} cho missing values của cột '{col}'")
    # -------------------------------------------------------------

    method = config.get('method', 'SimpleImputer')

    # Phân tách numeric và categorical columns còn lại
    numeric_cols = df_imputed.select_dtypes(
        include=[np.number]).columns.tolist()
    categorical_cols = df_imputed.select_dtypes(
        exclude=[np.number]).columns.tolist()

    imputers = {}

    # Chạy lại đoạn xử lý chung (SimpleImputer / KNNImputer) cho các cột bị thiếu còn lại (như 'country', 'children')
    if method == 'SimpleImputer':
        strategy = config.get('strategy', 'median')
        print(
            f"[Preprocessing] Áp dụng SimpleImputer với strategy='{strategy}' cho numeric features")

        if numeric_cols:
            num_imputer = SimpleImputer(strategy=strategy)
            df_imputed[numeric_cols] = num_imputer.fit_transform(
                df_imputed[numeric_cols])
            imputers['numeric'] = num_imputer

        if categorical_cols:
            cat_imputer = SimpleImputer(strategy='most_frequent')
            df_imputed[categorical_cols] = cat_imputer.fit_transform(
                df_imputed[categorical_cols])
            imputers['categorical'] = cat_imputer

    elif method == 'KNNImputer':
        n_neighbors = config.get('n_neighbors', 5)
        print(
            f"[Preprocessing] Áp dụng KNNImputer với n_neighbors={n_neighbors} cho numeric features")

        if numeric_cols:
            knn_imputer = KNNImputer(n_neighbors=n_neighbors)
            df_imputed[numeric_cols] = knn_imputer.fit_transform(
                df_imputed[numeric_cols])
            imputers['numeric'] = knn_imputer

        if categorical_cols:
            cat_imputer = SimpleImputer(strategy='most_frequent')
            df_imputed[categorical_cols] = cat_imputer.fit_transform(
                df_imputed[categorical_cols])
            imputers['categorical'] = cat_imputer

    else:
        raise ValueError(
            f"[Preprocessing] Method '{method}' chưa được hỗ trợ.")

    # Ghi nhận số lượng missing values sau khi xử lý
    missing_after = df_imputed.isnull().sum()
    missing_after = missing_after[missing_after > 0].to_dict()

    # Lưu lại metadata
    metadata = {
        'method': method,
        'config': config,
        'numeric_columns': numeric_cols,
        'categorical_columns': categorical_cols,
        'missing_before': missing_before,
        'missing_after': missing_after,
        'dropped_columns': config.get('drop_columns', []),
        'imputers': imputers
    }

    print(
        f"[Preprocessing] Đã xử lý xong. Số cột còn missing data: {len(missing_after)}")

    return df_imputed, metadata


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

    """
    # Phát hiện categorical columns (object hoặc category dtypes)
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    if not categorical_cols:
        print("[Preprocessing] Không có categorical columns để encode.")
        return df.copy(), {
            'method': config.get('method', 'OneHot'),
            'categorical_columns': [],
            'encoded_columns': [],
            'encoder': None
        }
    
    method = config.get('method', 'OneHot')
    df_encoded = df.copy()
    
    print(f"[Preprocessing] Áp dụng {method} encoding cho {len(categorical_cols)} categorical columns: {categorical_cols}")
    
    if method == 'OneHot':
        # Sử dụng OneHotEncoder
        drop_first = config.get('drop_first', False)
        drop_param = 'first' if drop_first else None
        
        encoder = OneHotEncoder(sparse_output=False, drop=drop_param, handle_unknown='ignore')
        
        # Fit và transform
        encoded_array = encoder.fit_transform(df_encoded[categorical_cols])
        
        # Tạo tên cột mới
        encoded_columns = []
        for i, col in enumerate(categorical_cols):
            categories = encoder.categories_[i]
            if drop_first and len(categories) > 1:
                categories = categories[1:]  # Bỏ category đầu nếu drop_first
            for cat in categories:
                encoded_columns.append(f"{col}_{cat}")
        
        # Tạo DataFrame với encoded features
        encoded_df = pd.DataFrame(encoded_array, columns=encoded_columns, index=df_encoded.index)
        
        # Xóa các cột categorical gốc và thêm encoded
        df_encoded = df_encoded.drop(columns=categorical_cols)
        df_encoded = pd.concat([df_encoded, encoded_df], axis=1)
        
        print(f"[Preprocessing] OneHot encoding hoàn thành. Số features: {len(df.columns)} → {len(df_encoded.columns)}")
        
        metadata = {
            'method': 'OneHot',
            'categorical_columns': categorical_cols,
            'encoded_columns': encoded_columns,
            'drop_first': drop_first,
            'encoder': encoder
        }
        
    elif method == 'Label':
        # Sử dụng LabelEncoder cho mỗi cột
        encoders = {}
        label_mappings = {}
        
        for col in categorical_cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            encoders[col] = le
            label_mappings[col] = dict(zip(le.classes_, le.transform(le.classes_)))
        
        print(f"[Preprocessing] Label encoding hoàn thành. Số features giữ nguyên: {len(df_encoded.columns)}")
        
        metadata = {
            'method': 'Label',
            'categorical_columns': categorical_cols,
            'encoded_columns': categorical_cols,  # Giữ nguyên tên cột
            'encoders': encoders,
            'label_mappings': label_mappings
        }
    else:
        raise ValueError(f"[Preprocessing] Method '{method}' không được hỗ trợ. Chọn 'OneHot' hoặc 'Label'.")
    
    return df_encoded, metadata

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
    """
    df_scaled = df.copy()
    method = config.get('method', 'StandardScaler')

    # Lọc chỉ các cột numeric để scale
    numeric_cols = df_scaled.select_dtypes(include=[np.number]).columns.tolist()
    non_numeric_cols = df_scaled.select_dtypes(exclude=[np.number]).columns.tolist()

    if non_numeric_cols:
        print(f"[Preprocessing] Cảnh báo: Tìm thấy {len(non_numeric_cols)} cột không phải numeric, sẽ bỏ qua: {non_numeric_cols}")

    if not numeric_cols:
        print("[Preprocessing] Không tìm thấy numeric columns để scaling.")
        metadata = {
            'method': method,
            'numeric_columns': [],
            'scaler': None,
        }
        return df_scaled, metadata

    print(f"[Preprocessing] Áp dụng {method} cho {len(numeric_cols)} numeric features")

    if method == 'StandardScaler':
        scaler = StandardScaler()
    elif method == 'MinMaxScaler':
        feature_range = tuple(config.get('feature_range', (0, 1)))
        scaler = MinMaxScaler(feature_range=feature_range)
        print(f"  - feature_range = {feature_range}")
    else:
        raise ValueError(f"[Preprocessing] Scaling method '{method}' chưa được hỗ trợ. Chọn 'StandardScaler' hoặc 'MinMaxScaler'.")

    df_scaled[numeric_cols] = scaler.fit_transform(df_scaled[numeric_cols])

    # Log thông tin về scaling parameters
    if method == 'StandardScaler':
        print(f"  - Mean range: [{scaler.mean_.min():.4f}, {scaler.mean_.max():.4f}]")
        print(f"  - Scale range: [{scaler.scale_.min():.4f}, {scaler.scale_.max():.4f}]")
    elif method == 'MinMaxScaler':
        print(f"  - Data min range: [{scaler.data_min_.min():.4f}, {scaler.data_min_.max():.4f}]")
        print(f"  - Data max range: [{scaler.data_max_.min():.4f}, {scaler.data_max_.max():.4f}]")

    print(f"[Preprocessing] Scaling hoàn tất cho {len(numeric_cols)} features")

    metadata = {
        'method': method,
        'config': config,
        'numeric_columns': numeric_cols,
        'scaler': scaler,
    }

    return df_scaled, metadata


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
    print("[Preprocessing] Bắt đầu chạy full preprocessing pipeline...")

    # 1. Tách features (X) và target (y)
    if target_column in df.columns:
        y = df[target_column].values
        X_df = df.drop(columns=[target_column])
    else:
        y = None
        X_df = df.copy()

    # 2. Áp dụng Imputation (Điền khuyết / Xóa cột)
    print("\n--- BƯỚC 1: XỬ LÝ MISSING DATA (IMPUTATION) ---")
    impute_config = config.get('imputation', {})
    X_df, impute_meta = apply_imputation(X_df, impute_config)

    # --- YÊU CẦU: Lưu dataset sau khi xử lý missing data ---
    # Gắn lại cột target để lưu thành file dataset hoàn chỉnh
    df_imputed_complete = X_df.copy()
    if y is not None:
        df_imputed_complete[target_column] = y

    # Tạo thư mục data/processed nếu chưa tồn tại
    output_dir = "data/processed"
    os.makedirs(output_dir, exist_ok=True)

    # Lưu file
    output_path = os.path.join(output_dir, "dataset_after_imputation.csv")
    df_imputed_complete.to_csv(output_path, index=False)
    print(
        f"[Preprocessing] Đã lưu dataset sau khi xử lý missing data tại: {output_path}\n")
    # -------------------------------------------------------

    # 3. Áp dụng Encoding (Xử lý Categorical - Hiện hàm này đang chờ implement)
    print("--- BƯỚC 2: ENCODING ---")
    encode_config = config.get('encoding', {})
    X_df, encode_meta = apply_encoding(X_df, encode_config)

    # 4. Áp dụng Scaling (Chuẩn hóa Numeric - Hiện hàm này đang chờ implement)
    print("\n--- BƯỚC 3: SCALING ---")
    scale_config = config.get('scaling', {})
    X_df, scale_meta = apply_scaling(X_df, scale_config)

    # 5. Chuyển sang numpy array để đưa vào Model
    X = X_df.values

    # 6. Tổng hợp metadata
    metadata = {
        'imputation': impute_meta,
        'encoding': encode_meta,
        'scaling': scale_meta
    }

    print("[Preprocessing] Hoàn tất full preprocessing pipeline!")
    return X, y, metadata


def preprocess_with_train_test_split(
    df: pd.DataFrame,
    target_column: str,
    config: Dict[str, Any],
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Pipeline preprocessing với train/test split để tránh data leakage.
    
    Quy trình:
    1. Tách features và target
    2. Split train/test (BEFORE preprocessing)
    3. Xóa cột + điền hằng số dựa trên config (áp dụng trên cả train/test để thống nhất)
    4. Fit tất cả transformers (imputer, encoder, scaler) trên TRAIN DATA ONLY
    5. Transform cả TRAIN và TEST data bằng fitted transformers
    6. Trả về X_train, X_test, y_train, y_test, metadata
    
    Args:
        df: DataFrame gốc
        target_column: Tên cột target để tách ra
        config: Dictionary cấu hình với keys 'imputation', 'encoding', 'scaling'
        test_size: Tỷ lệ test set (mặc định: 0.2)
        random_state: Seed cho reproducibility (mặc định: 42)
    
    Returns:
        Tuple chứa:
            - X_train: Training features đã được preprocess (numpy array)
            - X_test: Testing features đã được preprocess (numpy array)
            - y_train: Training target values (numpy array)
            - y_test: Testing target values (numpy array)
            - metadata: Dictionary chứa fitted transformers và preprocessing info
    
    ⚠️ IMPORTANT: Tránh data leakage bằng cách fit trên train data only!
    """
    print("[Preprocessing] Bắt đầu preprocessing với train/test split (tránh data leakage)...")
    
    # 1. Tách features và target
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' không tồn tại trong DataFrame")
    
    y = df[target_column].values
    X_df = df.drop(columns=[target_column])
    
    # 2. Split train/test TRƯỚC khi preprocessing
    print(f"[Preprocessing] Split data: {(1-test_size)*100:.0f}% train, {test_size*100:.0f}% test")
    X_train, X_test, y_train, y_test = train_test_split(
        X_df, y, test_size=test_size, random_state=random_state
    )
    print(f"  - Train shape: {X_train.shape}, Test shape: {X_test.shape}")
    
    # 3. Xử lý drop columns và constant fill (áp dụng trên cả train/test)
    print("\n--- BƯỚC 1: XỬ LÝ MISSING DATA - IMPUTATION ---")
    impute_config = config.get('imputation', {})
    
    # Drop columns
    drop_cols = impute_config.get('drop_columns', [])
    if drop_cols:
        cols_to_drop = [col for col in drop_cols if col in X_train.columns]
        X_train = X_train.drop(columns=cols_to_drop)
        X_test = X_test.drop(columns=cols_to_drop)
        print(f"[Preprocessing] Đã xoá các cột: {cols_to_drop}")
    
    # Constant fill
    constant_fill = impute_config.get('constant_fill', {})
    for col, value in constant_fill.items():
        if col in X_train.columns:
            X_train[col] = X_train[col].fillna(value)
            X_test[col] = X_test[col].fillna(value)
            print(f"[Preprocessing] Điền giá trị {value} cho cột '{col}'")
    
    # 4. Fit imputers trên TRAIN data only
    method = impute_config.get('method', 'SimpleImputer')
    numeric_cols_train = X_train.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols_train = X_train.select_dtypes(exclude=[np.number]).columns.tolist()
    
    imputers = {}
    
    if method == 'SimpleImputer':
        strategy = impute_config.get('strategy', 'median')
        print(f"[Preprocessing] Fitting SimpleImputer (strategy='{strategy}') trên train data...")
        
        if numeric_cols_train:
            num_imputer = SimpleImputer(strategy=strategy)
            X_train[numeric_cols_train] = num_imputer.fit_transform(X_train[numeric_cols_train])
            X_test[numeric_cols_train] = num_imputer.transform(X_test[numeric_cols_train])
            imputers['numeric'] = num_imputer
        
        if categorical_cols_train:
            cat_imputer = SimpleImputer(strategy='most_frequent')
            X_train[categorical_cols_train] = cat_imputer.fit_transform(X_train[categorical_cols_train])
            X_test[categorical_cols_train] = cat_imputer.transform(X_test[categorical_cols_train])
            imputers['categorical'] = cat_imputer
    
    elif method == 'KNNImputer':
        n_neighbors = impute_config.get('n_neighbors', 5)
        print(f"[Preprocessing] Fitting KNNImputer (n_neighbors={n_neighbors}) trên train data...")
        
        if numeric_cols_train:
            knn_imputer = KNNImputer(n_neighbors=n_neighbors)
            X_train[numeric_cols_train] = knn_imputer.fit_transform(X_train[numeric_cols_train])
            X_test[numeric_cols_train] = knn_imputer.transform(X_test[numeric_cols_train])
            imputers['numeric'] = knn_imputer
        
        if categorical_cols_train:
            cat_imputer = SimpleImputer(strategy='most_frequent')
            X_train[categorical_cols_train] = cat_imputer.fit_transform(X_train[categorical_cols_train])
            X_test[categorical_cols_train] = cat_imputer.transform(X_test[categorical_cols_train])
            imputers['categorical'] = cat_imputer
    
    else:
        raise ValueError(f"[Preprocessing] Method '{method}' chưa được hỗ trợ.")
    
    # 5. Fit encoding trên TRAIN data only
    print("\n--- BƯỚC 2: ENCODING ---")
    encode_config = config.get('encoding', {})
    categorical_cols = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
    
    encoder = None
    encoders_dict = {}
    
    if categorical_cols:
        enc_method = encode_config.get('method', 'OneHot')
        print(f"[Preprocessing] Fitting {enc_method} encoding trên train data...")
        
        if enc_method == 'OneHot':
            drop_first = encode_config.get('drop_first', False)
            drop_param = 'first' if drop_first else None
            
            encoder = OneHotEncoder(sparse_output=False, drop=drop_param, handle_unknown='ignore')
            encoder.fit(X_train[categorical_cols])
            
            # Transform train và test
            X_train_enc = encoder.transform(X_train[categorical_cols])
            X_test_enc = encoder.transform(X_test[categorical_cols])
            
            # Tạo tên cột và DataFrame
            encoded_columns = []
            for i, col in enumerate(categorical_cols):
                for cat in encoder.categories_[i]:
                    encoded_columns.append(f"{col}_{cat}")
            
            X_train_enc_df = pd.DataFrame(X_train_enc, columns=encoded_columns, index=X_train.index)
            X_test_enc_df = pd.DataFrame(X_test_enc, columns=encoded_columns, index=X_test.index)
            
            # Xóa categorical columns gốc và thêm encoded
            X_train = X_train.drop(columns=categorical_cols)
            X_test = X_test.drop(columns=categorical_cols)
            X_train = pd.concat([X_train, X_train_enc_df], axis=1)
            X_test = pd.concat([X_test, X_test_enc_df], axis=1)
            
            print(f"[Preprocessing] OneHot encoding xong. Features: {X_train.shape[1]}")
        
        elif enc_method == 'Label':
            print("[Preprocessing] Fitting Label encoding trên train data...")
            
            for col in categorical_cols:
                le = LabelEncoder()
                X_train[col] = le.fit_transform(X_train[col].astype(str))
                X_test[col] = le.transform(X_test[col].astype(str))
                encoders_dict[col] = le
            
            encoder = encoders_dict
            print(f"[Preprocessing] Label encoding xong. {len(categorical_cols)} cột encode")
    
    # 6. Fit scaling trên TRAIN data only
    print("\n--- BƯỚC 3: SCALING ---")
    scale_config = config.get('scaling', {})
    numeric_cols = X_train.select_dtypes(include=[np.number]).columns.tolist()
    
    scaler = None
    if numeric_cols:
        scale_method = scale_config.get('method', 'StandardScaler')
        print(f"[Preprocessing] Fitting {scale_method} trên train data...")
        
        if scale_method == 'StandardScaler':
            scaler = StandardScaler()
        elif scale_method == 'MinMaxScaler':
            feature_range = tuple(scale_config.get('feature_range', (0, 1)))
            scaler = MinMaxScaler(feature_range=feature_range)
            print(f"  - feature_range = {feature_range}")
        else:
            raise ValueError(f"[Preprocessing] Scaling method '{scale_method}' chưa được hỗ trợ.")
        
        # Fit trên train, transform cả train và test
        scaler.fit(X_train[numeric_cols])
        X_train[numeric_cols] = scaler.transform(X_train[numeric_cols])
        X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])
        
        print(f"[Preprocessing] Scaling xong cho {len(numeric_cols)} features")
    
    # 7. Chuyển sang numpy array
    X_train_array = X_train.values
    X_test_array = X_test.values
    
    # 8. Tổng hợp metadata
    metadata = {
        'imputation': {
            'method': method,
            'imputers': imputers,
            'numeric_columns': numeric_cols_train,
            'categorical_columns': categorical_cols_train
        },
        'encoding': {
            'method': encode_config.get('method', 'OneHot'),
            'encoder': encoder,
            'categorical_columns': categorical_cols
        },
        'scaling': {
            'method': scale_config.get('method', 'StandardScaler'),
            'scaler': scaler,
            'numeric_columns': numeric_cols
        },
        'split_info': {
            'test_size': test_size,
            'random_state': random_state,
            'train_shape': X_train_array.shape,
            'test_shape': X_test_array.shape
        }
    }
    
    print(f"\n[Preprocessing] Hoàn tất preprocessing! Train: {X_train_array.shape}, Test: {X_test_array.shape}")
    
    return X_train_array, X_test_array, y_train, y_test, metadata


# TODO: Thêm các hàm utility khác nếu cần
# - Hàm lưu và load fitted transformers (scalers, encoders)
# - Hàm xử lý outliers
