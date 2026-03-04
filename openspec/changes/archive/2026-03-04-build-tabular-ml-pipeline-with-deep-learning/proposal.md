## Why

Nhóm cần một kiến trúc pipeline học máy dạng module cho dữ liệu bảng vừa đáp ứng yêu cầu bắt buộc của bài tập (imputation, encoding, đánh giá mô hình truyền thống), vừa mở rộng thêm pipeline học sâu để lấy điểm thưởng. Việc chuẩn hóa ngay từ đầu giúp giảm rủi ro code rời rạc trong notebook, dễ phân công cho 4 thành viên, và đảm bảo đầu ra có thể chấm điểm được.

## What Changes

- Xây dựng cấu trúc dự án chuẩn gồm `notebooks/`, `modules/`, `features/`, `reports/` cho workflow huấn luyện và báo cáo.
- Thiết kế capability tải dữ liệu trực tiếp từ URL công khai (không mount Google Drive), đọc vào DataFrame và hỗ trợ dữ liệu thiếu/dữ liệu phân loại.
- Thiết kế capability EDA + tiền xử lý có thể cấu hình (imputation, encoding, scaling), kèm logging tiến trình.
- Thiết kế capability trích xuất đặc trưng (PCA) và lưu artifact ra `.npy` hoặc `.h5`.
- Thiết kế capability huấn luyện/đánh giá mô hình truyền thống (Logistic Regression, SVM, Random Forest) và mô hình MLP (TensorFlow/Keras).
- Chuẩn hóa các hàm module theo PEP8 + Google-style docstring để sẵn sàng triển khai thực tế.

## Capabilities

### New Capabilities
- `tabular-data-ingestion-and-eda`: Tải dữ liệu từ URL công khai, phân tích mô tả và trực quan hóa cho dữ liệu bảng có missing/categorical.
- `configurable-tabular-preprocessing-and-features`: Tiền xử lý có thể cấu hình (imputation, encoding, scaling), giảm chiều PCA và xuất đặc trưng `.npy`/`.h5`.
- `hybrid-model-training-and-evaluation`: Huấn luyện mô hình truyền thống + MLP, đánh giá bằng metric chuẩn và biểu đồ (confusion matrix, ROC-AUC).

### Modified Capabilities
- None.

## Impact

- Affected code: Toàn bộ module mới trong `modules/` (`data_loader.py`, `eda.py`, `preprocessing.py`, `features.py`, `models.py`, `evaluation.py`) và notebook điều phối trong `notebooks/`.
- Dependencies: Sử dụng các thư viện đã có sẵn (pandas, numpy, scikit-learn, tensorflow, matplotlib/seaborn).
- Data/Artifacts: Phát sinh file đặc trưng trong `features/` (`.npy` hoặc `.h5`) và tài liệu báo cáo/ảnh trong `reports/`.
- Team workflow: Tạo ranh giới chức năng rõ ràng để phân công theo module, giảm xung đột khi làm việc nhóm.
