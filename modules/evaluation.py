"""
Module: Model Evaluation

Module này cung cấp các hàm để đánh giá mô hình:
- Tính toán metrics: Accuracy, Precision, Recall, F1-score
- Tạo visualizations: Confusion Matrix, ROC-AUC curves
- Lưu kết quả vào reports/
"""

from __future__ import annotations

import os
from typing import Dict, Any, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
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
    results: Dict[str, float] = {}
    average = 'binary' if len(np.unique(y_true)) <= 2 else 'weighted'

    if 'accuracy' in metrics:
        results['accuracy'] = float(accuracy_score(y_true, y_pred))
    if 'precision' in metrics:
        results['precision'] = float(precision_score(y_true, y_pred, average=average, zero_division=0))
    if 'recall' in metrics:
        results['recall'] = float(recall_score(y_true, y_pred, average=average, zero_division=0))
    if 'f1' in metrics:
        results['f1'] = float(f1_score(y_true, y_pred, average=average, zero_division=0))

    return results


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
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=figsize)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


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
    y_proba = np.asarray(y_proba).reshape(-1)
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc_value = auc(fpr, tpr)

    plt.figure(figsize=figsize)
    plt.plot(fpr, tpr, label=f'ROC curve (AUC = {roc_auc_value:.4f})', color='darkorange')
    plt.plot([0, 1], [0, 1], linestyle='--', color='navy')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC-AUC Curve')
    plt.legend(loc='lower right')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


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
    os.makedirs(output_dir, exist_ok=True)

    metrics = compute_metrics(y_true, y_pred, config.get('metrics', ['accuracy', 'precision', 'recall', 'f1']))
    results: Dict[str, Any] = {
        'model_name': model_name,
        'metrics': metrics,
        'confusion_matrix_path': None,
        'roc_auc_path': None,
    }

    if config.get('generate_confusion_matrix', True):
        cm_path = os.path.join(output_dir, f'{model_name}_confusion_matrix.png')
        results['confusion_matrix_path'] = plot_confusion_matrix(y_true, y_pred, cm_path, figsize=config.get('figsize', {}).get('confusion_matrix', (8, 6)))

    if config.get('generate_roc_auc', True) and y_proba is not None:
        roc_path = os.path.join(output_dir, f'{model_name}_roc_auc.png')
        results['roc_auc_path'] = plot_roc_auc(y_true, y_proba, roc_path, figsize=config.get('figsize', {}).get('roc_auc', (8, 6)))

    return results


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
    if not results:
        raise ValueError('[Evaluation] Không có kết quả model nào để so sánh.')

    metrics_order = ['accuracy', 'precision', 'recall', 'f1']
    model_names = list(results.keys())
    values_by_metric = {
        metric: [results[name]['metrics'].get(metric, np.nan) for name in model_names]
        for metric in metrics_order
    }

    x = np.arange(len(model_names))
    width = 0.2

    plt.figure(figsize=(12, 6))
    for idx, metric in enumerate(metrics_order):
        plt.bar(x + (idx - 1.5) * width, values_by_metric[metric], width=width, label=metric.title())

    plt.xticks(x, model_names, rotation=15)
    plt.ylabel('Score')
    plt.ylim(0, 1.05)
    plt.title('Model Comparison')
    plt.legend()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    return output_path


# TODO: Thêm các hàm evaluation khác nếu cần
# - Classification report chi tiết
# - Precision-Recall curve
# - Learning curves
# - Feature importance visualization (cho tree-based models)
