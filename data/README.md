# Data Directory

Thư mục này chứa datasets cho dự án.

## 📁 Cấu Trúc

```
data/
├── .gitkeep           # Giữ thư mục trong Git
├── README.md          # File này
└── (raw data files)   # Data files sẽ được download vào đây
```

## 🔗 Dataset Sources

### Dataset Được Đề Xuất

Dưới đây là một số dataset công khai phù hợp với yêu cầu bài tập (có missing values và categorical features):

#### 1. **Titanic Dataset**
- **URL**: https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
- **Description**: Dữ liệu hành khách tàu Titanic
- **Features**: 12 features (numeric + categorical)
- **Target**: Survived (0/1)
- **Missing Values**: ✓ Có (Age, Cabin, Embarked)
- **Categorical Features**: ✓ Có (Sex, Embarked, Pclass)
- **Size**: ~60KB, 891 rows

#### 2. **Adult Income Dataset**
- **URL**: https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
- **Description**: Dự đoán thu nhập >50K hay <=50K
- **Features**: 14 features (numeric + categorical)
- **Target**: Income (>50K, <=50K)
- **Missing Values**: ✓ Có (workclass, occupation, native-country)
- **Categorical Features**: ✓ Có (workclass, education, marital-status, occupation, etc.)
- **Size**: ~3.8MB, 32,561 rows

#### 3. **Heart Disease Dataset**
- **URL**: https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data
- **Description**: Chẩn đoán bệnh tim
- **Features**: 13 features (numeric + categorical)
- **Target**: Presence of heart disease (0-4)
- **Missing Values**: ✓ Có
- **Categorical Features**: ✓ Có
- **Size**: ~10KB, 303 rows

#### 4. **Credit Approval Dataset**
- **URL**: https://archive.ics.uci.edu/ml/machine-learning-databases/credit-screening/crx.data
- **Description**: Phê duyệt thẻ tín dụng
- **Features**: 15 features (numeric + categorical)
- **Target**: Approved (+/-) 
- **Missing Values**: ✓ Có
- **Categorical Features**: ✓ Có
- **Size**: ~30KB, 690 rows

## 📥 Cách Tải Dataset

### Option 1: Sử dụng Pipeline (Recommended)

```python
from modules.data_loader import load_data_pipeline

# Tải và load vào DataFrame
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df, metadata = load_data_pipeline(url, "data/titanic.csv")
```

### Option 2: Manual Download

```bash
# Sử dụng wget (Linux/Mac)
wget -O data/titanic.csv https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv

# Hoặc sử dụng curl
curl -o data/titanic.csv https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv
```

### Option 3: Python requests

```python
import requests

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
response = requests.get(url)

with open("data/titanic.csv", "wb") as f:
    f.write(response.content)
```

## 📋 Yêu Cầu Dataset

Dataset cần thỏa mãn:
- ✅ **Missing Values**: Phải có missing values để demo imputation
- ✅ **Categorical Features**: Phải có features phân loại để demo encoding
- ✅ **Numeric Features**: Cần cho scaling và PCA
- ✅ **Classification Target**: Cho bài toán classification
- ✅ **Public URL**: Không cần authentication để tải

## 🔍 Khám Phá Dataset

Sau khi tải dataset, khám phá nó bằng:

```python
import pandas as pd

# Load dataset
df = pd.read_csv("data/your_dataset.csv")

# Basic info
print(f"Shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")
print(f"\nData types:\n{df.dtypes}")
print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nFirst few rows:\n{df.head()}")
```

## 📝 Dataset Checklist

Trước khi sử dụng dataset, kiểm tra:

- [ ] Dataset có thể tải từ URL công khai
- [ ] Dataset có missing values
- [ ] Dataset có categorical features
- [ ] Dataset có numeric features
- [ ] Target column rõ ràng
- [ ] Dataset size hợp lý (không quá lớn)
- [ ] Format file được hỗ trợ (CSV, Excel, etc.)

## 🚫 .gitignore

Data files thường không nên commit vào Git (vì dung lượng lớn). File `.gitignore` trong project đã exclude:

```
data/*.csv
data/*.xlsx
data/*.json
data/*.h5
data/*.npy
```

Chỉ `.gitkeep` và `README.md` được track.

## 💡 Tips

1. **Cache Dataset**: Sau khi download lần đầu, dataset sẽ được cache locally. Pipeline sẽ kiểm tra file tồn tại trước khi download lại.

2. **Multiple Datasets**: Bạn có thể download nhiều datasets để experiment:
   ```
   data/
   ├── titanic.csv
   ├── adult_income.csv
   └── heart_disease.csv
   ```

3. **Custom Dataset**: Nếu dùng dataset riêng, đảm bảo nó có URL công khai hoặc copy thủ công vào thư mục `data/`.

4. **Large Files**: Nếu dataset quá lớn (>100MB), consider using:
   - Google Drive links (với download script)
   - Kaggle API
   - Cloud storage (S3, Azure Blob, etc.)

## 📞 Support

Nếu gặp vấn đề với dataset:
1. Kiểm tra URL có accessible không
2. Kiểm tra format file có được hỗ trợ không
3. Xem error messages trong data_loader module
4. Liên hệ team members

## 📚 References

- [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)
- [Kaggle Datasets](https://www.kaggle.com/datasets)
- [Data Science Dojo Datasets](https://github.com/datasciencedojo/datasets)
- [Awesome Public Datasets](https://github.com/awesomedata/awesome-public-datasets)
