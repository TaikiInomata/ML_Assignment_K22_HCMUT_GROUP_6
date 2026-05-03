# Hướng dẫn tự tay hiện thực A-Z mục 5 (Yêu cầu sản phẩm)

Tài liệu này hướng dẫn bạn tự làm đầy đủ phần "Yêu cầu sản phẩm" trong đề bài, tập trung vào:
- Colab notebook chạy `Runtime -> Run all` không lỗi.
- Không mount Google Drive/Dropbox.
- Dữ liệu được tải từ nguồn công khai, có link rõ ràng trong notebook.
- Có bước cài đặt thư viện và chuẩn bị dữ liệu tự động.
- Tạo đủ artifact cần nộp (`.npy`/`.h5`, báo cáo, cấu trúc thư mục).

## 1. Mục tiêu đầu ra cần đạt

Sau khi hoàn thành, bạn phải có:
1. 1 notebook Colab (frontend chính) chạy được toàn bộ.
2. Thư mục dự án rõ ràng: `notebooks/`, `modules/`, `reports/`, `features/`.
3. File đặc trưng đã lưu dạng `.npy` hoặc `.h5` trong `features/`.
4. Báo cáo PDF tổng hợp EDA + pipeline + thí nghiệm + so sánh kết quả.
5. README đầy đủ thông tin học phần, giảng viên, thành viên, hướng dẫn chạy, link báo cáo + Colab.

## 2. Kế hoạch thực hiện nhanh (khuyến nghị)

1. Tạo notebook nộp bài mới: `notebooks/final_submission_colab.ipynb`.
2. Chia notebook thành 8 section: Setup, Data Download, Data Check, EDA, Preprocessing, Feature Save, Modeling, Export Results.
3. Chạy thử local 1 lần (nếu có), sau đó chạy trên Colab và bấm `Run all`.
4. Chốt artifact vào `features/` và `reports/`.
5. Chốt README + PDF báo cáo.

## 3. Khung notebook Colab để nộp (mẫu dùng ngay)

Bạn tạo notebook với thứ tự cell như sau.

### Cell 1 - Clone repo và di chuyển vào thư mục dự án

```bash
!git clone <LINK_GITHUB_REPO_CUA_BAN>
%cd project_folder
```

Ghi chú:
- Không dùng `drive.mount(...)`.
- Toàn bộ thao tác trong storage tạm của Colab.

### Cell 2 - Cài đặt dependencies

```bash
!python -m pip install --upgrade pip
!pip install -r requirements.txt
```

### Cell 3 - Khai báo nguồn dữ liệu công khai

```python
# Bắt buộc: để link nguồn dữ liệu công khai rõ ràng ngay trong notebook.
PUBLIC_DATA_SOURCE = "https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand"
print("Public data source:", PUBLIC_DATA_SOURCE)
```

### Cell 4 - Download dữ liệu (không mount cloud cá nhân)

Lựa chọn A (khuyến nghị với dự án hiện tại): dùng Kaggle API.

```bash
# Nếu chưa có kaggle
!pip install -q kaggle
!mkdir -p ~/.kaggle

# Upload kaggle.json bằng Colab file upload (không phải Google Drive mount)
from google.colab import files
uploaded = files.upload()  # chọn kaggle.json

!mv kaggle.json ~/.kaggle/kaggle.json
!chmod 600 ~/.kaggle/kaggle.json

# Download và giải nén trực tiếp vào data/
!kaggle datasets download -d jessemostipak/hotel-booking-demand -p data --force
!python - << 'PY'
import zipfile, glob
zips = glob.glob('data/*.zip')
for z in zips:
    with zipfile.ZipFile(z, 'r') as f:
        f.extractall('data')
print('Done extract')
PY
!ls -la data
```

Lựa chọn B: nếu bạn có direct CSV URL công khai, dùng `wget/curl` tải trực tiếp.

```bash
# Ví dụ: thay URL bên dưới bằng direct CSV link thật
!wget -O data/hotel_bookings.csv "<DIRECT_PUBLIC_CSV_URL>"
```

### Cell 5 - Kiểm tra file đầu vào

```python
from pathlib import Path
p = Path("data/hotel_bookings.csv")
assert p.exists(), f"Không tìm thấy {p}"
print("OK:", p, "size=", p.stat().st_size)
```

### Cell 6 - Chạy pipeline mô hình (script sẵn có)

```bash
# Chạy nhanh để kiểm tra quy trình không lỗi
!python scripts/run_stage3_member3_svm.py --quick --cv 2 --max-iter 3000
```

Nếu cần kết quả kỹ hơn:

```bash
!python scripts/run_stage3_member3_svm.py --full --cv 5 --max-iter 5000
```

### Cell 7 - Tạo và lưu file đặc trưng (.npy hoặc .h5)

```python
import numpy as np
import pandas as pd
from config import CONFIG
from modules.preprocessing import preprocess_with_train_test_split
from modules.features import engineer_features, save_features

# 1) Load data
_df = pd.read_csv(CONFIG['data']['file_path'])

# 2) Preprocess với split đúng chuẩn
X_train, X_test, y_train, y_test, _ = preprocess_with_train_test_split(
    df=_df,
    target_column=CONFIG['data']['target_column'],
    config=CONFIG['preprocessing'],
    test_size=CONFIG['models']['train_test_split']['test_size'],
    random_state=CONFIG['models']['train_test_split']['random_state'],
)

# 3) Feature engineering (PCA nếu bật trong config)
X_train_eng, feat_meta = engineer_features(X_train, CONFIG['features'])

# 4) Lưu feature theo yêu cầu nộp bài
out_cfg = dict(CONFIG['features']['output'])
out_cfg['format'] = 'npy'   # đổi thành 'h5' nếu bạn muốn nộp h5
out_cfg['path'] = 'features/final_submission_features'
save_path = save_features(X_train_eng, np.asarray(y_train), out_cfg)
print('Saved features at:', save_path)
print('Feature metadata keys:', feat_meta.keys())
```

### Cell 8 - Tổng hợp kết quả để đưa vào báo cáo

```bash
!ls -la reports/evaluation
!ls -la features
```

### Cell 9 - Tự kiểm tra trước khi nộp (quan trọng)

```python
from pathlib import Path

required_paths = [
    Path('notebooks'),
    Path('modules'),
    Path('reports'),
    Path('features'),
    Path('reports/evaluation/svm_test_metrics.json'),
]

missing = [str(x) for x in required_paths if not x.exists()]
if missing:
    raise FileNotFoundError('Thiếu các mục bắt buộc: ' + ', '.join(missing))

has_npy = any(Path('features').glob('*.npy'))
has_h5 = any(Path('features').glob('*.h5'))
assert (has_npy or has_h5), 'Cần có ít nhất 1 file .npy hoặc .h5 trong features/'

print('Checklist cơ bản: PASS')
```

## 4. Checklist đúng theo tiêu chí Mục 5

Đánh dấu từng mục trước khi nộp:

- [ ] Notebook là frontend chính trên Google Colab.
- [ ] Bấm `Runtime -> Run all` chạy xong không lỗi.
- [ ] Không có bất kỳ dòng lệnh mount Google Drive/Dropbox.
- [ ] Có để rõ link nguồn dữ liệu công khai trong notebook.
- [ ] Có bước cài thư viện và chuẩn bị dữ liệu tự động.
- [ ] Có file đặc trưng `.npy` hoặc `.h5` trong `features/`.
- [ ] Có kết quả đánh giá trong `reports/`.
- [ ] Có báo cáo PDF tổng hợp phân tích.
- [ ] README đầy đủ thông tin môn học, GVHD, thành viên, hướng dẫn chạy, cấu trúc, link báo cáo + Colab.

## 5. Mẫu mục lục README để đủ điểm

Bạn cần đảm bảo README có các mục:

1. Thông tin môn học (tên môn, mã môn, học kỳ, năm học).
2. Thông tin GVHD.
3. Danh sách thành viên (họ tên, MSSV, email).
4. Mục tiêu bài tập lớn.
5. Hướng dẫn chạy notebook trên Colab (dependencies, tải dữ liệu).
6. Cấu trúc thư mục dự án.
7. Link báo cáo PDF và link Colab notebook.

## 6. Lỗi thường gặp và cách xử lý

1. Lỗi `kaggle: command not found`.
- Cách sửa: chạy lại `pip install kaggle`, khởi động lại runtime nếu cần.

2. Lỗi `403` khi download Kaggle.
- Cách sửa: kiểm tra `kaggle.json`, đặt đúng `~/.kaggle/kaggle.json`, `chmod 600`.

3. Notebook fail khi `Run all` do thứ tự cell.
- Cách sửa: reset runtime, chạy lại từ đầu, đảm bảo cell setup nằm trên cùng.

4. Thiếu file `.npy`/`.h5`.
- Cách sửa: chạy lại cell Feature Save, kiểm tra thư mục `features/`.

## 7. Cách nộp để an toàn

1. Export notebook đã chạy xong (có output) và kiểm tra lần cuối bằng `Run all`.
2. Đóng gói đúng cấu trúc thư mục: `notebooks/`, `modules/`, `reports/`, `features/`.
3. Kèm PDF report.
4. Nếu nộp thêm GitHub, đảm bảo README đầy đủ và link hợp lệ.

---

Nếu bạn muốn, bước tiếp theo là tạo thêm 1 notebook mẫu hoàn chỉnh theo đúng khung trên (có sẵn tiêu đề markdown + cell code) để bạn copy chạy ngay.
