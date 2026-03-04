# Modules Documentation

Tài liệu chi tiết về các modules trong pipeline.

## 📚 Tổng Quan Modules

Pipeline gồm 6 modules chính, mỗi module có trách nhiệm riêng:

1. **data_loader.py** - Data Ingestion
2. **eda.py** - Exploratory Data Analysis
3. **preprocessing.py** - Data Preprocessing
4. **features.py** - Feature Engineering
5. **models.py** - Model Training
6. **evaluation.py** - Model Evaluation

## 1. data_loader.py

### Mục đích
Tải dữ liệu từ URL công khai và đọc vào Pandas DataFrame.

### Functions chính
- `load_data_from_url(url, output_path)` - Download data từ URL
- `create_dataframe(file_path)` - Đọc file thành DataFrame
- `load_data_pipeline(url, output_path)` - Pipeline hoàn chỉnh

### TODO
- [ ] Implement download logic với retry mechanism
- [ ] Hỗ trợ nhiều file formats (CSV, Excel, JSON)
- [ ] Validate URL và handle errors
- [ ] Extract metadata (rows, columns, dtypes, missing values)
- [ ] Add progress tracking cho large files

### Phân công
**Thành viên phụ trách**: [Tên]

## 2. eda.py

### Mục đích
Phân tích mô tả và tạo visualizations cho dữ liệu.

### Functions chính
- `generate_eda_report(df)` - Tạo báo cáo thống kê
- `plot_correlation_heatmap(df, output_path)` - Vẽ correlation heatmap
- `plot_missing_values(df, output_path)` - Vẽ missing values chart
- `plot_class_distribution(df, target, output_path)` - Vẽ class distribution
- `run_full_eda(df, target, output_dir)` - Chạy toàn bộ EDA

### TODO
- [ ] Implement descriptive statistics
- [ ] Vẽ correlation heatmap với seaborn
- [ ] Vẽ missing values visualization
- [ ] Vẽ class distribution (bar + pie chart)
- [ ] Cảnh báo class imbalance
- [ ] Lưu báo cáo text và images

### Phân công
**Thành viên phụ trách**: [Tên]

## 3. preprocessing.py

### Mục đích
Tiền xử lý dữ liệu với các bước configurable.

### Functions chính
- `apply_imputation(df, config)` - Xử lý missing values
- `apply_encoding(df, config)` - Encode categorical features
- `apply_scaling(df, config)` - Scale numeric features
- `preprocess_pipeline(df, target, config)` - Pipeline hoàn chỉnh

### TODO
- [ ] Implement SimpleImputer (mean/median/most_frequent)
- [ ] Implement KNNImputer
- [ ] Implement OneHot Encoding
- [ ] Implement Label Encoding
- [ ] Implement StandardScaler
- [ ] Implement MinMaxScaler với configurable range
- [ ] Lưu fitted transformers để transform test data

### Phân công
**Thành viên phụ trách**: [Tên]

## 4. features.py

### Mục đích
Feature engineering và dimensionality reduction.

### Functions chính
- `apply_pca(X, config)` - Apply PCA với variance threshold
- `save_features(X, y, config)` - Lưu features (.npy/.h5)
- `load_features(file_path, format)` - Load features
- `engineer_features(X, config)` - Feature engineering pipeline

### TODO
- [ ] Implement PCA với configurable variance threshold
- [ ] Log số chiều trước và sau PCA
- [ ] Lưu features dạng .npy
- [ ] Lưu features dạng .h5 (HDF5)
- [ ] Load features từ saved files
- [ ] Validate sau khi load

### Phân công
**Thành viên phụ trách**: [Tên]

## 5. models.py

### Mục đích
Huấn luyện các models (traditional ML + deep learning).

### Functions chính
- `train_logistic_regression(X_train, y_train, X_test, params)` - Train Logistic Regression
- `train_svm(X_train, y_train, X_test, params)` - Train SVM
- `train_random_forest(X_train, y_train, X_test, params)` - Train Random Forest
- `train_mlp(X_train, y_train, X_test, params)` - Train MLP (Keras)
- `train_models_pipeline(X_train, y_train, X_test, y_test, config)` - Train tất cả models

### TODO
- [ ] Implement Logistic Regression với params từ dictionary
- [ ] Implement SVM với params từ dictionary
- [ ] Implement Random Forest với params từ dictionary
- [ ] Implement MLP với TensorFlow/Keras
  - [ ] Build architecture từ config
  - [ ] Compile và train
  - [ ] Plot training history
- [ ] Log training progress cho tất cả models
- [ ] Return predictions và probabilities

### Phân công
**Thành viên phụ trách**: [Tên]

## 6. evaluation.py

### Mục đích
Đánh giá models và tạo visualizations.

### Functions chính
- `compute_metrics(y_true, y_pred, metrics)` - Tính metrics
- `plot_confusion_matrix(y_true, y_pred, output_path)` - Vẽ confusion matrix
- `plot_roc_auc(y_true, y_proba, output_path)` - Vẽ ROC-AUC curve
- `evaluate_model(y_true, y_pred, y_proba, model_name, output_dir, config)` - Đánh giá đầy đủ
- `compare_models(results, output_path)` - So sánh models

### TODO
- [ ] Implement metrics: accuracy, precision, recall, f1
- [ ] Vẽ confusion matrix với seaborn
- [ ] Vẽ ROC-AUC curve
- [ ] Tạo comparison bar chart cho tất cả models
- [ ] Highlight model tốt nhất
- [ ] Lưu tất cả plots với DPI cao

### Phân công
**Thành viên phụ trách**: [Tên]

## 🔧 Guidelines cho Implementation

### Coding Style
- Tuân thủ PEP8
- Google-style docstrings
- Type hints cho function signatures
- Clear error messages

### Testing
- Test với sample data trước
- Validate inputs và outputs
- Handle edge cases
- Log tiến trình ở mỗi bước

### Integration
- Ensure modules work together
- Follow input/output contracts
- Use centralized config
- Return consistent data structures

## 📋 Implementation Checklist

### Phase 1: Core Functions (Tuần 1-2)
- [ ] data_loader.py functions
- [ ] eda.py basic functions
- [ ] preprocessing.py imputation và encoding

### Phase 2: Advanced Features (Tuần 3)
- [ ] preprocessing.py scaling
- [ ] features.py PCA và save/load
- [ ] models.py traditional ML

### Phase 3: Deep Learning và Evaluation (Tuần 4)
- [ ] models.py MLP implementation
- [ ] evaluation.py metrics và plots
- [ ] Integration testing

### Phase 4: Polish và Documentation (Tuần 5)
- [ ] Code review và refactoring
- [ ] Complete documentation
- [ ] End-to-end testing
- [ ] Prepare final report

## 🤝 Team Collaboration

### Git Workflow
1. Create feature branch cho module của bạn
2. Implement và test locally
3. Create pull request
4. Code review từ team members
5. Merge sau khi approved

### Communication
- Daily standups hoặc updates trong group chat
- Document blocking issues
- Share progress và challenges
- Help teammates khi needed

## 📞 Contact

Nếu có câu hỏi về bất kỳ module nào, liên hệ thành viên phụ trách hoặc post trong group chat.
