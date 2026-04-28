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
import importlib


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
    print("[Models] Huấn luyện Logistic Regression")
    model = LogisticRegression(**params)
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
    print("[Models] Huấn luyện SVM")
    model = SVC(**params)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return model, predictions


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
    print("[Models] Huấn luyện Random Forest")
    model = RandomForestClassifier(**params)
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
    print("[Models] Huấn luyện MLP (TensorFlow/Keras)")

    try:
        tf = importlib.import_module('tensorflow')
    except ImportError as exc:
        raise ImportError(
            "[Models] TensorFlow chưa được cài đặt. Cài bằng 'pip install tensorflow'."
        ) from exc

    hidden_layers = params.get('hidden_layers', [128, 64, 32])
    activation = params.get('activation', 'relu')
    dropout_rate = params.get('dropout_rate', 0.3)
    learning_rate = params.get('learning_rate', 0.001)
    epochs = params.get('epochs', 50)
    batch_size = params.get('batch_size', 32)
    validation_split = params.get('validation_split', 0.2)
    early_stopping_cfg = params.get('early_stopping', {'enabled': True, 'patience': 5})

    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Input(shape=(X_train.shape[1],)))
    for units in hidden_layers:
        model.add(tf.keras.layers.Dense(units, activation=activation))
        if dropout_rate and dropout_rate > 0:
            model.add(tf.keras.layers.Dropout(dropout_rate))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    callbacks = []
    if early_stopping_cfg.get('enabled', True):
        callbacks.append(
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=early_stopping_cfg.get('patience', 5),
                restore_best_weights=True,
            )
        )

    model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        callbacks=callbacks,
        verbose=0,
    )

    y_proba = model.predict(X_test, verbose=0).flatten()
    predictions = (y_proba >= 0.5).astype(int)
    return model, predictions


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
    print("[Models] Bắt đầu pipeline huấn luyện models")

    results: Dict[str, Any] = {
        'models': {},
        'predictions': {},
        'y_test': y_test,
    }

    if models_config.get('logistic_regression', {}).get('enabled', False):
        cfg = models_config.get('logistic_regression', {})
        model, preds = train_logistic_regression(
            X_train,
            y_train,
            X_test,
            cfg.get('params', {}),
        )
        results['models']['logistic_regression'] = model
        results['predictions']['logistic_regression'] = preds

    if models_config.get('svm', {}).get('enabled', False):
        cfg = models_config.get('svm', {})
        model, preds = train_svm(
            X_train,
            y_train,
            X_test,
            cfg.get('params', {}),
        )
        results['models']['svm'] = model
        results['predictions']['svm'] = preds

    if models_config.get('random_forest', {}).get('enabled', False):
        cfg = models_config.get('random_forest', {})
        model, preds = train_random_forest(
            X_train,
            y_train,
            X_test,
            cfg.get('params', {}),
        )
        results['models']['random_forest'] = model
        results['predictions']['random_forest'] = preds

    if models_config.get('mlp', {}).get('enabled', False):
        cfg = models_config.get('mlp', {})
        model, preds = train_mlp(
            X_train,
            y_train,
            X_test,
            cfg.get('params', {}),
        )
        results['models']['mlp'] = model
        results['predictions']['mlp'] = preds

    print(f"[Models] Huấn luyện xong {len(results['models'])} model(s)")
    return results


# TODO: Thêm các hàm utility khác nếu cần
# - Hàm lưu và load trained models
# - Hàm grid search cho hyperparameter tuning
# - Hàm cross-validation
