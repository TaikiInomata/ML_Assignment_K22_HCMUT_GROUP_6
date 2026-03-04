"""
Module: Model Evaluation

Module này cung cấp các hàm để đánh giá mô hình:
- Tính toán metrics: Accuracy, Precision, Recall, F1-score
- Tạo visualizations: Confusion Matrix, ROC-AUC curves
- Lưu kết quả vào reports/
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List, Optional
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc, roc_auc_score
)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, 
                   metrics: List[str] = ['accuracy', 'precision', 'recall', 'f1']) -> Dict[str, float]:
    """
    Tính toán các metrics đánh giá model.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        metrics: List các metrics cần tính (mặc định: tất cả)
    
    Returns:
        Dictionary chứa giá trị các metrics
    
    TODO: Implement metrics calculation
    - Tính accuracy nếu trong metrics list
    - Tính precision nếu trong metrics list
    - Tính recall nếu trong metrics list
    - Tính f1-score nếu trong metrics list
    - Xử lý multi-class vs binary classification
    - Trả về dictionary với tên và giá trị metrics
    """
    # TODO: Implement metrics calculation
    print("[Evaluation] TODO: Tính toán metrics")
    pass


def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray,
                         output_path: str, figsize: tuple = (8, 6)) -> str:
    """
    Vẽ và lưu Confusion Matrix.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        output_path: Đường dẫn lưu hình ảnh
        figsize: Kích thước figure
    
    Returns:
        Đường dẫn đến file hình ảnh đã lưu
    
    TODO: Implement confusion matrix visualization
    - Tính confusion matrix
    - Vẽ heatmap với seaborn
    - Thêm labels và annotations
    - Lưu hình ảnh với DPI cao
    - Trả về đường dẫn
    """
    # TODO: Implement confusion matrix plot
    print(f"[Evaluation] TODO: Vẽ Confusion Matrix và lưu vào {output_path}")
    pass


def plot_roc_auc(y_true: np.ndarray, y_proba: np.ndarray,
                output_path: str, figsize: tuple = (8, 6)) -> str:
    """
    Vẽ và lưu ROC-AUC curve.
    
    Args:
        y_true: True labels
        y_proba: Predicted probabilities (cho positive class)
        output_path: Đường dẫn lưu hình ảnh
        figsize: Kích thước figure
    
    Returns:
        Đường dẫn đến file hình ảnh đã lưu
    
    TODO: Implement ROC-AUC visualization
    - Tính false positive rate và true positive rate
    - Tính AUC score
    - Vẽ ROC curve
    - Thêm diagonal reference line
    - Hiển thị AUC score trên plot
    - Lưu hình ảnh
    - Trả về đường dẫn
    """
    # TODO: Implement ROC-AUC plot
    print(f"[Evaluation] TODO: Vẽ ROC-AUC curve và lưu vào {output_path}")
    pass


def evaluate_model(y_true: np.ndarray, y_pred: np.ndarray, 
                  y_proba: Optional[np.ndarray],
                  model_name: str, output_dir: str,
                  config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Đánh giá toàn diện một model.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        y_proba: Predicted probabilities (optional, cho ROC-AUC)
        model_name: Tên model để đặt tên files
        output_dir: Thư mục lưu outputs
        config: Cấu hình evaluation
    
    Returns:
        Dictionary chứa metrics và đường dẫn plots
    
    TODO: Implement full model evaluation
    - Tính toán metrics
    - Vẽ confusion matrix nếu enabled trong config
    - Vẽ ROC-AUC nếu enabled và có y_proba
    - Lưu tất cả outputs vào output_dir
    - Tổng hợp kết quả vào dictionary
    - Trả về results
    """
    # TODO: Implement full evaluation pipeline
    print(f"[Evaluation] TODO: Đánh giá model {model_name}")
    pass


def compare_models(results: Dict[str, Dict[str, Any]], 
                  output_path: str) -> str:
    """
    So sánh performance của nhiều models.
    
    Args:
        results: Dictionary chứa kết quả của tất cả models
        output_path: Đường dẫn lưu comparison chart
    
    Returns:
        Đường dẫn đến comparison chart
    
    TODO: Implement model comparison
    - Extract metrics từ tất cả models
    - Tạo comparison bar chart
    - Highlight model tốt nhất cho mỗi metric
    - Lưu chart
    - Trả về đường dẫn
    """
    # TODO: Implement model comparison visualization
    print(f"[Evaluation] TODO: So sánh các models và lưu vào {output_path}")
    pass


# TODO: Thêm các hàm evaluation khác nếu cần
# - Classification report chi tiết
# - Precision-Recall curve
# - Learning curves
# - Feature importance visualization (cho tree-based models)
