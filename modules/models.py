"""
Module: Model Training

Module này cung cấp các hàm để huấn luyện mô hình:
- Traditional ML models: Logistic Regression, SVM, Random Forest
- Deep Learning: MLP với TensorFlow/Keras
- Tất cả models nhận parameters từ dictionary
"""

import numpy as np
from typing import Dict, Any, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
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
    # TODO: Implement Logistic Regression
    print("[Models] TODO: Huấn luyện Logistic Regression")
    pass


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
    # TODO: Implement SVM
    print("[Models] TODO: Huấn luyện SVM")
    pass


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
    # TODO: Implement Random Forest
    print("[Models] TODO: Huấn luyện Random Forest")
    pass


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
    # TODO: Implement MLP with TensorFlow/Keras
    print("[Models] TODO: Huấn luyện MLP (Deep Learning)")
    pass


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
    # TODO: Implement training pipeline
    print("[Models] TODO: Chạy pipeline huấn luyện tất cả models")
    pass


# TODO: Thêm các hàm utility khác nếu cần
# - Hàm lưu và load trained models
# - Hàm grid search cho hyperparameter tuning
# - Hàm cross-validation
