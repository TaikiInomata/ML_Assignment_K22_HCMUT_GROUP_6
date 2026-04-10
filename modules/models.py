"""
Module: Model Training

Module này cung cấp các hàm để huấn luyện mô hình:
- Traditional ML models: Logistic Regression, SVM, Random Forest
- Deep Learning: MLP với TensorFlow/Keras
- Tất cả models nhận parameters từ dictionary
"""

import numpy as np
from typing import Dict, Any, Tuple, List
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold
# TODO: Import TensorFlow/Keras khi implement MLP
# import tensorflow as tf
# from tensorflow import keras


def train_logistic_regression(X_train: np.ndarray, y_train: np.ndarray, 
                              X_test: np.ndarray, params: Dict[str, Any]) -> Tuple[Any, np.ndarray]:
    """
    Huấn luyện Logistic Regression model.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test features
        params: Dictionary parameters cho LogisticRegression
    
    Returns:
        Tuple chứa:
            - model: Trained model
            - predictions: Predictions trên test set
    
    TODO: Implement Logistic Regression training
    - Khởi tạo model với params
    - Fit trên training data
    - Predict trên test data
    - Log training progress
    - Trả về model và predictions
    """
    model = LogisticRegression(**params)
    print(f"[Models] Huấn luyện Logistic Regression với params={params}")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return model, predictions


def train_svm(X_train: np.ndarray, y_train: np.ndarray, 
              X_test: np.ndarray, params: Dict[str, Any]) -> Tuple[Any, np.ndarray]:
    """
    Huấn luyện SVM model.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test features
        params: Dictionary parameters cho SVC
    
    Returns:
        Tuple chứa:
            - model: Trained model
            - predictions: Predictions trên test set
    
    TODO: Implement SVM training
    - Khởi tạo SVC với params
    - Fit trên training data
    - Predict trên test data
    - Log training progress
    - Trả về model và predictions
    """
    final_params = dict(params)
    final_params.setdefault('probability', True)

    model = SVC(**final_params)
    print(f"[Models] Huấn luyện SVM với params={final_params}")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return model, predictions


def optimize_svm_with_kernel_search(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Tối ưu SVM bằng GridSearchCV qua nhiều kernel.

    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test features
        y_test: Test labels
        params: Dictionary cấu hình. Các key hỗ trợ:
            - base_params: tham số mặc định của SVC
            - param_grid: lưới tham số cho GridSearchCV
            - scoring: metric tối ưu (mặc định: 'f1')
            - cv: số folds (mặc định: 5)
            - n_jobs: số luồng chạy song song (mặc định: -1)

    Returns:
        Dictionary chứa best_model, best_params, cv_best_score,
        test_metrics, predictions, probability, grid_results.
    """
    base_params = dict(params.get('base_params', {}))
    base_params.setdefault('probability', True)
    base_params.setdefault('random_state', 42)

    default_grid: Dict[str, List[Any]] = {
        'kernel': ['linear', 'rbf', 'poly', 'sigmoid'],
        'C': [0.1, 1.0, 10.0],
        'gamma': ['scale', 'auto']
    }
    param_grid = params.get('param_grid', default_grid)
    scoring = params.get('scoring', 'f1')
    cv_folds = int(params.get('cv', 5))
    n_jobs = int(params.get('n_jobs', -1))

    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    estimator = SVC(**base_params)

    print(
        "[Models] Bắt đầu GridSearchCV cho SVM "
        f"(scoring={scoring}, cv={cv_folds})"
    )
    grid = GridSearchCV(
        estimator=estimator,
        param_grid=param_grid,
        scoring=scoring,
        cv=cv,
        n_jobs=n_jobs,
        refit=True,
        verbose=0
    )
    grid.fit(X_train, y_train)

    best_model = grid.best_estimator_
    predictions = best_model.predict(X_test)
    probability = None
    if hasattr(best_model, 'predict_proba'):
        probability = best_model.predict_proba(X_test)[:, 1]

    metrics = {
        'accuracy': float(accuracy_score(y_test, predictions)),
        'precision': float(precision_score(y_test, predictions, zero_division=0)),
        'recall': float(recall_score(y_test, predictions, zero_division=0)),
        'f1': float(f1_score(y_test, predictions, zero_division=0))
    }

    results = {
        'best_model': best_model,
        'best_params': grid.best_params_,
        'cv_best_score': float(grid.best_score_),
        'test_metrics': metrics,
        'predictions': predictions,
        'probability': probability,
        'grid_results': {
            'params': grid.cv_results_['params'],
            'mean_test_score': grid.cv_results_['mean_test_score'].tolist(),
            'rank_test_score': grid.cv_results_['rank_test_score'].tolist()
        }
    }

    print(
        "[Models] GridSearchCV hoàn tất | "
        f"Best params={results['best_params']} | "
        f"CV best={results['cv_best_score']:.4f} | "
        f"Test F1={metrics['f1']:.4f}"
    )
    return results


def train_random_forest(X_train: np.ndarray, y_train: np.ndarray, 
                       X_test: np.ndarray, params: Dict[str, Any]) -> Tuple[Any, np.ndarray]:
    """
    Huấn luyện Random Forest model.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test features
        params: Dictionary parameters cho RandomForestClassifier
    
    Returns:
        Tuple chứa:
            - model: Trained model
            - predictions: Predictions trên test set
    
    TODO: Implement Random Forest training
    - Khởi tạo RandomForestClassifier với params
    - Fit trên training data
    - Predict trên test data
    - Log training progress và feature importances
    - Trả về model và predictions
    """
    model = RandomForestClassifier(**params)
    print(f"[Models] Huấn luyện Random Forest với params={params}")
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return model, predictions


def train_mlp(X_train: np.ndarray, y_train: np.ndarray, 
              X_test: np.ndarray, params: Dict[str, Any]) -> Tuple[Any, np.ndarray]:
    """
    Huấn luyện MLP (Multi-Layer Perceptron) với TensorFlow/Keras.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test features
        params: Dictionary parameters cho MLP với keys:
            - hidden_layers: List số neurons mỗi hidden layer
            - activation: Activation function
            - dropout_rate: Dropout rate
            - learning_rate: Learning rate
            - epochs: Số epochs
            - batch_size: Batch size
            - validation_split: Validation split ratio
    
    Returns:
        Tuple chứa:
            - model: Trained Keras model
            - predictions: Predictions trên test set
    
    TODO: Implement MLP training
    - Build Keras Sequential model theo architecture trong params
    - Compile model với optimizer và loss function
    - Fit với training data và validation split
    - Plot training history
    - Predict trên test data
    - Trả về model và predictions
    """
    raise NotImplementedError(
        "MLP chưa được implement trong module này. "
        "Dự kiến triển khai ở giai đoạn bonus/deep learning."
    )


def train_models_pipeline(X_train: np.ndarray, y_train: np.ndarray,
                         X_test: np.ndarray, y_test: np.ndarray,
                         models_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pipeline huấn luyện tất cả models theo config.
    
    Args:
        X_train: Training features
        y_train: Training labels
        X_test: Test features
        y_test: Test labels
        models_config: Dictionary cấu hình cho tất cả models
    
    Returns:
        Dictionary chứa trained models và predictions
    
    TODO: Implement models training pipeline
    - Parse models_config để xác định models nào enabled
    - Train từng model được enable
    - Lưu model và predictions vào results dict
    - Log tổng quan về training session
    - Trả về results dictionary
    """
    print("[Models] Bắt đầu train_models_pipeline...")
    results: Dict[str, Any] = {}

    logistic_cfg = models_config.get('logistic_regression', {})
    if logistic_cfg.get('enabled', False):
        model, pred = train_logistic_regression(
            X_train, y_train, X_test, logistic_cfg.get('params', {})
        )
        results['logistic_regression'] = {
            'model': model,
            'predictions': pred
        }

    svm_cfg = models_config.get('svm', {})
    if svm_cfg.get('enabled', False):
        if svm_cfg.get('tuning', {}).get('enabled', False):
            tune_result = optimize_svm_with_kernel_search(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                params=svm_cfg.get('tuning', {})
            )
            results['svm'] = tune_result
        else:
            model, pred = train_svm(
                X_train, y_train, X_test, svm_cfg.get('params', {})
            )
            results['svm'] = {
                'model': model,
                'predictions': pred
            }

    rf_cfg = models_config.get('random_forest', {})
    if rf_cfg.get('enabled', False):
        model, pred = train_random_forest(
            X_train, y_train, X_test, rf_cfg.get('params', {})
        )
        results['random_forest'] = {
            'model': model,
            'predictions': pred
        }

    mlp_cfg = models_config.get('mlp', {})
    if mlp_cfg.get('enabled', False):
        try:
            model, pred = train_mlp(
                X_train, y_train, X_test, mlp_cfg.get('params', {})
            )
            results['mlp'] = {
                'model': model,
                'predictions': pred
            }
        except NotImplementedError as exc:
            print(f"[Models] Bỏ qua MLP: {exc}")
            results['mlp'] = {
                'error': str(exc)
            }

    print(f"[Models] Hoàn tất training cho {len(results)} model mục tiêu")
    return results


# TODO: Thêm các hàm utility khác nếu cần
# - Hàm lưu và load trained models
# - Hàm grid search cho hyperparameter tuning
# - Hàm cross-validation
