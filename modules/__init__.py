"""
Package: Tabular ML Pipeline Modules

Package này chứa các module cho pipeline học máy dữ liệu bảng:
- data_loader: Tải dữ liệu từ URL công khai
- eda: Phân tích dữ liệu khám phá (EDA) và trực quan hóa
- preprocessing: Tiền xử lý dữ liệu (imputation, encoding, scaling)
- features: Kỹ thuật đặc trưng và PCA
- models: Huấn luyện mô hình (ML truyền thống + MLP)
- evaluation: Đánh giá mô hình và tính toán metrics

Author: Team ML
Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "Team ML"

from .data_loader import (
	load_data_from_url,
	create_dataframe,
	load_data_pipeline,
	load_data_from_config,
	load_data_from_source,
	load_hotel_bookings_dataset,
)
from .eda import (
	generate_eda_report,
	plot_correlation_heatmap,
	plot_missing_values,
	plot_class_distribution,
	run_full_eda,
	analyze_categorical_features_distribution,
	analyze_categorical_target_relationship,
	plot_categorical_distribution,
	plot_categorical_with_target,
	plot_categorical_association_heatmap,
	run_categorical_eda,
)
from .preprocessing import (
	apply_imputation,
	apply_encoding,
	apply_scaling,
	preprocess_pipeline,
	preprocess_with_train_test_split,
)
from .features import apply_pca, save_features, load_features, engineer_features
from .models import (
	train_logistic_regression,
	train_svm,
	train_random_forest,
	train_mlp,
	train_models_pipeline,
)
from .evaluation import (
	compute_metrics,
	plot_confusion_matrix,
	plot_roc_auc,
	evaluate_model,
	compare_models,
)
