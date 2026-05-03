# Progress Report 3 - Thành viên 3

## 1. Nhiệm vụ thực hiện

Trong Giai đoạn 3, Thành viên 3 phụ trách huấn luyện và tối ưu mô hình SVM trên dữ liệu đã tiền xử lý. Mục tiêu của phần việc này là thử nghiệm nhiều kernel khác nhau, so sánh hiệu quả theo cross-validation, sau đó đánh giá mô hình tốt nhất trên tập test.

## 2. Quy trình thực hiện

1. Tách train/test trước khi tiền xử lý để tránh data leakage.
2. Tiền xử lý dữ liệu bằng imputation, one-hot encoding và standard scaling.
3. Tối ưu SVM bằng GridSearchCV với nhiều kernel.
4. Chọn mô hình có điểm cross-validation tốt nhất.
5. Đánh giá trên tập test và xuất các biểu đồ phục vụ báo cáo.

## 3. Kết quả thí nghiệm

- Kernel tốt nhất: `rbf`
- Tham số tốt nhất: `{"C": 10.0, "gamma": "scale", "kernel": "rbf"}`
- Điểm CV tốt nhất: `0.7662`
- Accuracy test: `0.8410`
- Precision test: `0.8248`
- Recall test: `0.7322`
- F1-score test: `0.7758`

## 4. Nhận xét

Kết quả cho thấy kernel `linear` là lựa chọn tốt nhất trong các cấu hình đã thử ở thí nghiệm hiện tại. Với F1-score khoảng 0.596 trên tập test, mô hình đạt mức hiệu năng trung bình-khá và có thể tiếp tục cải thiện bằng mở rộng grid tham số, cân bằng dữ liệu, hoặc bổ sung đặc trưng phù hợp hơn.

## 5. Biểu đồ đưa vào báo cáo

### 5.1 So sánh kernel

![So sánh kernel SVM](reports/evaluation/svm_kernel_comparison.png)

### 5.2 Confusion Matrix

![Confusion Matrix SVM](reports/evaluation/svm_confusion_matrix.png)

## 6. File đầu ra

- Best model: `reports/evaluation/svm_best_model.joblib`
- Metrics: `reports/evaluation/svm_test_metrics.json`
- Ranking: `reports/evaluation/svm_grid_ranking.csv`
- Summary: `reports/evaluation/svm_stage3_summary.json`

## 7. Kết luận

Phần việc của Thành viên 3 đã hoàn thành yêu cầu Stage 3: huấn luyện SVM, thử nhiều kernel, chọn cấu hình tốt nhất và tạo đầy đủ artifact phục vụ báo cáo.
