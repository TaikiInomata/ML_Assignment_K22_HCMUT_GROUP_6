"""
Configuration File

Centralized configuration cho toàn bộ ML pipeline.
Sử dụng file này thay vì hard-code values trong notebook.

Usage:
    from config import CONFIG
    url = CONFIG['data']['url']
"""

# ============ Cấu hình Dữ liệu ============
DATA_CONFIG = {
    'url': 'https://example.com/dataset.csv',  # TODO: Thay bằng URL dataset thực tế
    'file_path': 'data/raw_data.csv',
    'target_column': 'target'  # TODO: Thay bằng tên cột target thực tế
}

# ============ Cấu hình EDA ============
EDA_CONFIG = {
    'enabled': True,
    'output_dir': 'reports/eda/',
    'generate_correlation_heatmap': True,
    'generate_missing_value_chart': True,
    'generate_class_distribution': True,
    'figsize': {
        'heatmap': (12, 10),
        'missing_values': (12, 8),
        'class_distribution': (10, 6)
    }
}

# ============ Cấu hình Preprocessing ============
PREPROCESSING_CONFIG = {
    # Imputation - Xử lý missing values
    'imputation': {
        'method': 'SimpleImputer',  # Options: 'SimpleImputer', 'KNNImputer'
        'strategy': 'mean',  # Cho SimpleImputer: 'mean', 'median', 'most_frequent'
        'n_neighbors': 5  # Cho KNNImputer
    },
    
    # Encoding - Xử lý categorical features
    'encoding': {
        'method': 'OneHot',  # Options: 'OneHot', 'Label'
        'drop_first': False  # Cho OneHot encoding: drop first category để tránh multicollinearity
    },
    
    # Scaling - Chuẩn hóa numeric features
    'scaling': {
        'method': 'StandardScaler',  # Options: 'StandardScaler', 'MinMaxScaler'
        'feature_range': (0, 1)  # Cho MinMaxScaler: (min, max)
    }
}

# ============ Cấu hình Feature Engineering ============
FEATURES_CONFIG = {
    'pca': {
        'enabled': True,  # Bật/tắt PCA
        'variance_threshold': 0.95  # Giữ 95% explained variance; thử 0.90, 0.95, 0.99
    },
    'output': {
        'format': 'npy',  # Options: 'npy', 'h5'
        'path': 'features/processed_features'  # Đường dẫn base (không có extension)
    }
}

# ============ Cấu hình Models ============
MODELS_CONFIG = {
    # Train/Test split
    'train_test_split': {
        'test_size': 0.2,  # 20% cho test set
        'random_state': 42  # Seed cho reproducibility
    },
    
    # Logistic Regression
    'logistic_regression': {
        'enabled': True,
        'params': {
            'max_iter': 1000,
            'random_state': 42,
            'solver': 'lbfgs'
        }
    },
    
    # Support Vector Machine
    'svm': {
        'enabled': True,
        'params': {
            'kernel': 'rbf',  # Options: 'linear', 'poly', 'rbf', 'sigmoid'
            'C': 1.0,  # Regularization parameter
            'gamma': 'scale',  # Kernel coefficient
            'random_state': 42
        }
    },
    
    # Random Forest
    'random_forest': {
        'enabled': True,
        'params': {
            'n_estimators': 100,  # Số lượng trees
            'max_depth': None,  # Độ sâu tối đa của tree (None = không giới hạn)
            'min_samples_split': 2,
            'min_samples_leaf': 1,
            'random_state': 42
        }
    },
    
    # Multi-Layer Perceptron (Deep Learning - Bonus)
    'mlp': {
        'enabled': True,
        'params': {
            'hidden_layers': [128, 64, 32],  # Số neurons mỗi hidden layer
            'activation': 'relu',  # Activation function: 'relu', 'tanh', 'sigmoid'
            'dropout_rate': 0.3,  # Dropout để prevent overfitting
            'learning_rate': 0.001,
            'epochs': 50,  # Số epochs training
            'batch_size': 32,
            'validation_split': 0.2,  # 20% training data cho validation
            'early_stopping': {
                'enabled': True,
                'patience': 5  # Dừng nếu val_loss không cải thiện sau 5 epochs
            }
        }
    }
}

# ============ Cấu hình Evaluation ============
EVALUATION_CONFIG = {
    'metrics': ['accuracy', 'precision', 'recall', 'f1'],  # Metrics cần tính
    'generate_confusion_matrix': True,
    'generate_roc_auc': True,
    'output_dir': 'reports/evaluation/',
    'figsize': {
        'confusion_matrix': (8, 6),
        'roc_auc': (8, 6),
        'comparison': (12, 6)
    },
    'save_dpi': 300  # DPI cho saved images
}

# ============ Master Configuration Dictionary ============
CONFIG = {
    'data': DATA_CONFIG,
    'eda': EDA_CONFIG,
    'preprocessing': PREPROCESSING_CONFIG,
    'features': FEATURES_CONFIG,
    'models': MODELS_CONFIG,
    'evaluation': EVALUATION_CONFIG
}

# ============ Helper Functions ============
def get_config():
    """
    Get toàn bộ configuration.
    
    Returns:
        Dictionary chứa tất cả configurations
    """
    return CONFIG


def get_data_config():
    """Get data configuration only."""
    return DATA_CONFIG


def get_preprocessing_config():
    """Get preprocessing configuration only."""
    return PREPROCESSING_CONFIG


def get_models_config():
    """Get models configuration only."""
    return MODELS_CONFIG


def print_config():
    """Print configuration để review."""
    import json
    print("=" * 60)
    print("CONFIGURATION SUMMARY")
    print("=" * 60)
    print(json.dumps(CONFIG, indent=2, default=str))
    print("=" * 60)


if __name__ == "__main__":
    # Print configuration khi chạy file này
    print_config()
