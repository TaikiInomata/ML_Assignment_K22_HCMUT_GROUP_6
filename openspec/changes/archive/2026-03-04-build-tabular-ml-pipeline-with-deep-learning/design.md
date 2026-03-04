## Context

Dự án là bài tập lớn môn Học máy cho nhóm 4 sinh viên, cần vừa đáp ứng yêu cầu pipeline học máy truyền thống trên dữ liệu bảng, vừa có phần học sâu mở rộng để lấy điểm thưởng. Hiện trạng mong muốn là một codebase có khả năng chạy trong Google Colab mà không phụ thuộc Google Drive mount, dữ liệu tải trực tiếp từ URL công khai.

Ràng buộc chính:
- Dữ liệu bắt buộc có missing values và categorical features để thể hiện bước imputation + encoding.
- Pipeline phải xuất đặc trưng sang `.npy` hoặc `.h5`.
- Logic xử lý cần tách module rõ ràng để phân công nhóm, notebook chỉ làm vai trò điều phối.
- Các bước phải có khả năng bật/tắt qua config tập trung trong notebook.

## Goals / Non-Goals

**Goals:**
- Xây dựng kiến trúc module rõ ràng cho toàn bộ vòng đời: ingestion → EDA → preprocessing → feature extraction → training → evaluation.
- Chuẩn hóa giao diện hàm theo PEP8 + Google docstring, đồng nhất logging tiến trình.
- Hỗ trợ song song mô hình truyền thống (Logistic Regression, SVM, Random Forest) và MLP (TensorFlow/Keras).
- Tạo artifact đầu ra (đặc trưng, báo cáo, hình ảnh) theo cấu trúc thư mục thống nhất.

**Non-Goals:**
- Không tối ưu siêu tham số nâng cao (AutoML, Bayesian optimization) trong change này.
- Không triển khai hệ thống serving/triển khai production (API, Docker, CI/CD).
- Không bao phủ NLP, ảnh, chuỗi thời gian; chỉ tập trung dữ liệu bảng.

## Decisions

1. **Tách pipeline thành 6 module chuyên biệt trong `modules/`**
   - Quyết định: dùng các file `data_loader.py`, `eda.py`, `preprocessing.py`, `features.py`, `models.py`, `evaluation.py`.
   - Lý do: giảm coupling, dễ chia việc theo thành viên, dễ test từng khối.
   - Alternative considered: gom toàn bộ vào một notebook lớn; bị loại vì khó bảo trì và khó tái sử dụng.

2. **Dùng config dictionary tập trung tại notebook điều phối**
   - Quyết định: mọi bước nhận config dạng dictionary (bao gồm bật/tắt bước, loại imputer/encoder/scaler, tham số mô hình).
   - Lý do: cho phép chạy nhiều cấu hình và so sánh công bằng.
   - Alternative considered: hard-code tham số trong từng hàm; bị loại vì khó tái lập thí nghiệm.

3. **Chuẩn hóa I/O dữ liệu và artifact theo contract rõ ràng**
   - Quyết định: `data_loader` trả về DataFrame; `preprocessing/features` trả ma trận đặc trưng và metadata; `features` lưu `.npy` hoặc `.h5`.
   - Lý do: đảm bảo tính tương thích giữa mô hình truyền thống và MLP.
   - Alternative considered: chỉ lưu object pickle; bị loại vì kém minh bạch và khó kiểm tra độc lập.

4. **Thống nhất bộ metric và hình ảnh đánh giá**
   - Quyết định: dùng Accuracy, Precision, Recall, F1-score; thêm Confusion Matrix và ROC-AUC.
   - Lý do: bao phủ cả quality tổng quát và hiệu năng phân lớp.
   - Alternative considered: chỉ dùng accuracy; bị loại do không phản ánh mất cân bằng lớp.

5. **Logging tiến trình bằng `print` có thông điệp rõ ngữ cảnh**
   - Quyết định: mỗi bước chính in trạng thái (ví dụ: "Đang thực hiện PCA với 95% phương sai...").
   - Lý do: phù hợp yêu cầu bài tập và dễ debug trong Colab.
   - Alternative considered: logging framework phức tạp; bị loại để giữ MVP đơn giản.

## Risks / Trade-offs

- **[Risk] URL dữ liệu công khai không ổn định hoặc chậm** → Mitigation: hỗ trợ tải bằng `requests`/`wget`, retry cơ bản, và cache tạm trong phiên chạy.
- **[Risk] One-Hot có thể làm tăng mạnh số chiều** → Mitigation: cho phép bật PCA với ngưỡng phương sai cấu hình ($90\%$, $95\%$).
- **[Risk] MLP khó hội tụ với dữ liệu nhỏ/không cân bằng** → Mitigation: thiết kế MLP đơn giản, cho phép điều chỉnh learning rate/epochs/batch size qua config.
- **[Trade-off] Giữ thiết kế module hóa làm tăng số file ban đầu** → Đổi lại khả năng phân công và bảo trì dài hạn tốt hơn.

## Migration Plan

1. Tạo khung thư mục chuẩn (`notebooks/`, `modules/`, `features/`, `reports/`).
2. Triển khai module theo thứ tự phụ thuộc: `data_loader` → `eda` → `preprocessing` → `features` → `models` → `evaluation`.
3. Tạo notebook điều phối với config tập trung và luồng chạy chuẩn.
4. Chạy thử end-to-end trên một dataset tabular có missing + categorical; xác nhận artifact `.npy` hoặc `.h5` được tạo.
5. Hoàn thiện báo cáo và hình ảnh trong `reports/`.

Rollback strategy:
- Nếu bước học sâu gây lỗi, vẫn giữ pipeline truyền thống hoạt động độc lập (feature artifact + model cổ điển).
- Nếu định dạng `.h5` phát sinh lỗi thư viện, fallback lưu `.npy` để đảm bảo yêu cầu đầu ra.

## Open Questions

- Dataset công khai cụ thể nào sẽ được nhóm chốt dùng cho báo cáo cuối cùng?
- Có yêu cầu bắt buộc chia train/validation/test theo tỷ lệ cố định nào từ giảng viên không?
- Mức độ chi tiết mong muốn của phần so sánh giữa mô hình truyền thống và MLP trong báo cáo là bao nhiêu?
