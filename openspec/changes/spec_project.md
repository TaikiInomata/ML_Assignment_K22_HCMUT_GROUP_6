### 1\. Chủ đề bài tập lớn (Topic)

Chủ đề: Xây dựng Pipeline Học máy Dự báo Khả năng Hủy đặt phòng dựa trên hướng tiếp cận Truyền thống và Học sâu
---------------------------------------------------------------------------------------------------------------

### 1\. Bối cảnh và Tầm quan trọng

Trong ngành dịch vụ lưu trú, việc khách hàng hủy đặt phòng (cancellation) gây ra tổn thất doanh thu đáng kể và gây khó khăn trong việc tối ưu hóa vận hành. Việc dự báo chính xác khả năng một đơn đặt phòng bị hủy giúp khách sạn chủ động trong việc quản lý doanh thu (revenue management) và đưa ra các chính sách khuyến mãi hoặc bù đắp phù hợp.

### 2\. Mục tiêu dự án

-   Xây dựng Pipeline truyền thống: Thiết kế quy trình xử lý dữ liệu từ thô đến mô hình hoàn chỉnh, đảm bảo tính cấu hình linh hoạt (configurable) theo yêu cầu của đề bài.

-   Xử lý dữ liệu thực tế: Thực hành các kỹ thuật xử lý dữ liệu lỗi thời, dữ liệu thiếu và mã hóa biến định danh trên tập dữ liệu có độ phức tạp cao.

-   So sánh và Đánh giá: Phân tích sự hiệu quả giữa các thuật toán học máy cổ điển và mạng nơ-ron học sâu (MLP) để tìm ra giải pháp tối ưu nhất.

* * * * *

### 3\. Phân tích đặc trưng dữ liệu (Data Features)

Tập dữ liệu này gồm 32 đặc trưng (features) mô tả chi tiết hành vi đặt phòng, đáp ứng hoàn hảo các ràng buộc của giảng viên:

-   Dữ liệu thiếu (Missing Values) : * company: Chiếm tỉ lệ thiếu rất cao (~94%), đòi hỏi nhóm phải quyết định loại bỏ hay dùng kỹ thuật gán nhãn đặc biệt.

-   agent, children, country: Yêu cầu các kỹ thuật Imputation như Mean, Median hoặc KNN.

-   Dữ liệu phân loại (Categorical Values): * Các cột như hotel, arrival_date_month, meal, market_segment, distribution_channel, deposit_type.

-   Nhóm sẽ thực hành One-hot Encoding và Label Encoding trên các trường dữ liệu này.

-   Biến mục tiêu (Target Variable): * is_canceled: Giá trị nhị phân ($0$: không hủy, $1$: có hủy).

* * * * *

### 4\. Kiến trúc Pipeline đề xuất

Hệ thống sẽ được xây dựng theo mô hình Modular, cho phép thay đổi cấu hình mà không cần viết lại mã nguồn:

1.  Exploratory Data Analysis (EDA): Thống kê mô tả, trực quan hóa xu hướng phân phối và phát hiện giá trị ngoại lai (outliers).

2.  Preprocessing Module: * Imputation: Điền giá trị thiếu.

-   Scaling: Lựa chọn linh hoạt giữa $MinMaxScaler$ và $StandardScaler$.

-   Encoding: Mã hóa các biến định danh.

4.  Feature Engineering: Áp dụng PCA để giảm số chiều, thử nghiệm với các ngưỡng phương sai giữ lại như $90\%$ hoặc $95\%$.

5.  Modeling (Traditional): Triển khai và so sánh ít nhất 3 mô hình: Logistic Regression, SVM, và Random Forest.

6.  Deep Learning (Bonus): Xây dựng mạng nơ-ron đa tầng (MLP) để so sánh đối chứng.

* * * * *

### 5\. Chỉ số đánh giá (Metrics)

Để đánh giá tính hiệu quả của hệ thống, nhóm sẽ sử dụng các chỉ số đo lường chuẩn trong phân loại nhị phân:

-   Accuracy (Độ chính xác tổng quát).

-   Precision (Độ chính xác trên các mẫu dự báo tích cực).

-   Recall (Khả năng bắt trọn các mẫu thực sự tích cực).

-   $F_1$-score (Chỉ số cân bằng giữa Precision và Recall).

### 2\. Kế hoạch chi tiết và Phân công (Mô hình làm việc song song)

### 🚀 Giai đoạn 1: Khởi động & EDA (03/03 - 08/03)

Mục tiêu: Hoàn thành Progress Report 1.

-   Thành viên 1:

-   Khởi tạo GitHub Repository với đầy đủ cấu trúc thư mục: notebooks/, modules/, reports/, features/.

-   Viết file modules/data_loader.py để tải dữ liệu tự động từ URL công khai (Kaggle/GitHub Raw), tuyệt đối không dùng Google Drive mount.

-   Thành viên 2:

-   Thực hiện EDA về dữ liệu thiếu (Missing values).

-   Thống kê số lượng giá trị trống ở các cột agent, company, children.

-   Thành viên 3:

-   Thực hiện EDA về dữ liệu phân loại (Categorical values).

-   Phân tích sự đa dạng và tương quan của các biến như hotel, meal, country với biến mục tiêu is_canceled.

-   Thành viên 4:

-   Thực hiện EDA về dữ liệu số (Numerical values).

-   Vẽ biểu đồ phân phối và phát hiện giá trị ngoại lai cho lead_time, adr.

* * * * *

### 🛠 Giai đoạn 2: Tiền xử lý dữ liệu (09/03 - 22/03)

Mục tiêu: Hoàn thành Progress Report 2 trước 12h trưa 22/03/2026 gửi về lantv@hcmut.edu.vn.

-   Thành viên 1 :

-   Thiết lập file config.py để quản lý các tham số pipeline.

-   Tích hợp các hàm từ thành viên khác vào file modules/preprocessing.py thành một pipeline thống nhất.

-   Thành viên 2:

-   Hiện thực hàm Imputation: Sử dụng các kỹ thuật như Mean, Median hoặc KNN để điền giá trị thiếu dựa trên phân tích ở GĐ 1.

-   Thành viên 3:

-   Hiện thực hàm Encoding: Triển khai One-hot encoding hoặc Label encoding cho các biến phân loại.

-   Thành viên 4:

-   Hiện thực hàm Scaling: Cài đặt linh hoạt giữa MinMaxScaler và StandardScaler kèm cấu hình feature_range.

* * * * *

### 📉 Giai đoạn 3: Trích xuất đặc trưng & Mô hình hóa (23/03 - 12/04)

Mục tiêu: Hoàn thành Progress Report 3 trước 12h trưa 12/04/2026 gửi về lantv@hcmut.edu.vn.

-   Thành viên 1 :

-   Hiện thực kỹ thuật giảm chiều dữ liệu PCA trong modules/features.py.

-   Cấu hình các mức giữ lại phương sai (90%, 95%) và xuất file đặc trưng ra định dạng .npy vào thư mục features/.

-   Thành viên 2:

-   Huấn luyện và tối ưu mô hình Logistic Regression trên tập dữ liệu đã xử lý.

-   Thành viên 3:

-   Huấn luyện và tối ưu mô hình SVM (thử nghiệm các loại kernel khác nhau).

-   Thành viên 4:

-   Huấn luyện và tối ưu mô hình Random Forest, so sánh kết quả với các mô hình trên.

* * * * *

### 🧠 Giai đoạn 4: Học sâu & So sánh tổng thể (13/04 - 26/04)

Mục tiêu: Hoàn thành Progress Report 4 trước 12h trưa 26/04/2026 gửi về lantv@hcmut.edu.vn.

-   Thành viên 1 :

-   Xây dựng bảng tổng hợp so sánh các chỉ số Accuracy, Precision, Recall, F1-score của tất cả mô hình.

-   Vẽ biểu đồ Confusion Matrix và ROC-AUC cho báo cáo.

-   Thành viên 2:

-   Soạn thảo nội dung Báo cáo PDF: Phần EDA và quy trình Tiền xử lý.

-   Thành viên 3:

-   Soạn thảo nội dung Báo cáo PDF: Phần Phân tích kết quả mô hình và so sánh thí nghiệm.

-   Thành viên 4:

-   Phần điểm thưởng: Xây dựng mạng nơ-ron MLP (Deep Learning) để so sánh với pipeline truyền thống.

* * * * *

### 📦 Giai đoạn 5: Kiểm tra & Nộp bài (27/04 - 10/05)

Mục tiêu: Nộp bài qua Google Form trước 12h trưa ngày 10/05/2026.

-   Thành viên 1 :

-   Kiểm tra tính hoàn chỉnh của file nộp (.zip): notebooks/, modules/, reports/, features/.

-   Đảm bảo Notebook chạy thành công với chức năng Run all mà không phát sinh lỗi.

-   Thành viên 2:

-   Tổng hợp các minh chứng làm việc nhóm (hình ảnh họp, biên bản thảo luận) vào báo cáo.

-   Thành viên 3:

-   Cập nhật đầy đủ thông tin vào file README trên GitHub (Tên môn, giảng viên, thành viên, hướng dẫn chạy) để lấy điểm thưởng.

-   Thành viên 4:

-   Rà soát lại tỷ lệ đóng góp của từng thành viên trong bảng phân công công việc cuối cùng.