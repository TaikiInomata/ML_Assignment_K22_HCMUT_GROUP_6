# Báo Cáo Tiến Độ Giai Đoạn 3 - Thành viên 3

## 1. Nhiệm vụ được phân công

Trong Giai đoạn 3, Thành viên 3 phụ trách xây dựng, huấn luyện và tối ưu mô hình Support Vector Machine (SVM) trên tập dữ liệu đã được tiền xử lý. Nội dung công việc tập trung vào việc khảo sát nhiều kernel khác nhau, so sánh hiệu năng thông qua cross-validation, và đánh giá mô hình tối ưu trên tập kiểm tra nhằm phục vụ báo cáo tiến độ của nhóm.

## 2. Quy trình thực hiện

1. Thực hiện chia train/test trước bước tiền xử lý để bảo đảm không xảy ra hiện tượng data leakage.
2. Tiền xử lý dữ liệu bằng các bước imputation, one-hot encoding và standard scaling theo cấu hình của dự án.
3. Tối ưu mô hình SVM bằng GridSearchCV với nhiều lựa chọn kernel.
4. Lựa chọn mô hình có kết quả cross-validation tốt nhất làm mô hình đại diện.
5. Đánh giá mô hình trên tập test và xuất các biểu đồ minh họa phục vụ trình bày trong báo cáo.

## 3. Kết quả thí nghiệm

- Kernel tối ưu: `linear`
- Bộ tham số tối ưu: `{"C": 1.0, "gamma": "scale", "kernel": "linear"}`
- Điểm cross-validation tốt nhất: `1.0000`
- Accuracy trên tập test: `1.0000`
- Precision trên tập test: `1.0000`
- Recall trên tập test: `1.0000`
- F1-score trên tập test: `1.0000`

## 4. Nhận xét

Kết quả thực nghiệm cho thấy kernel `linear` là lựa chọn phù hợp nhất đối với dữ liệu sau tiền xử lý trong cấu hình thử nghiệm hiện tại. Mô hình đạt hiệu quả rất cao trên tập kiểm tra, qua đó cho thấy chuỗi tiền xử lý dữ liệu và quá trình lựa chọn tham số đã tạo ra biểu diễn đặc trưng phù hợp cho bài toán phân loại.

## 5. Hình minh họa sử dụng trong báo cáo

### 5.1 Biểu đồ so sánh các kernel của SVM

![Biểu đồ so sánh kernel SVM](reports/evaluation/svm_kernel_comparison.png)

### 5.2 Ma trận nhầm lẫn của mô hình SVM tốt nhất

![Ma trận nhầm lẫn SVM](reports/evaluation/svm_confusion_matrix.png)

## 6. Các tệp kết quả đầu ra

- Mô hình tốt nhất: `reports/evaluation/svm_best_model.joblib`
- Chỉ số đánh giá: `reports/evaluation/svm_test_metrics.json`
- Bảng xếp hạng các cấu hình thử nghiệm: `reports/evaluation/svm_grid_ranking.csv`
- File tổng hợp kết quả: `reports/evaluation/svm_stage3_summary.json`

## 7. Kết luận

Phần việc của Thành viên 3 trong Giai đoạn 3 đã hoàn thành đầy đủ yêu cầu đề ra, bao gồm huấn luyện mô hình SVM, thử nghiệm nhiều kernel, xác định cấu hình tối ưu và tạo đầy đủ các artifact phục vụ trình bày trong báo cáo PDF.
