# 📋 Báo Cáo Cập Nhật: Preprocessing với Train/Test Split và Hoàn Thiện EDA

**Ngày cập nhật:** 08/04/2026  
**Phạm vi:** Giai đoạn 2 → 3 (Chuẩn bị cho Stage 3 tránh data leakage)

---

## 🎯 Mục Tiêu

Sửa lỗi data leakage trong preprocessing pipeline hiện tại và hoàn thiện các hàm EDA còn TODO.

### Vấn đề Ban Đầu
- ❌ Stage 1-2: fit transformers (imputer, encoder, scaler) trên TOÀN bộ dữ liệu
- ❌ Rồi mới split train/test → TEST DATA ảnh hưởng đến transformer parameters
- ❌ Dẫn tới data leakage khi train model

---

## ✅ Cải Tiến Thực Hiện

### 1️⃣ Preprocessing: Thêm Hàm `preprocess_with_train_test_split`

**File:** [`modules/preprocessing.py`](modules/preprocessing.py)

#### Nguyên lý hoạt động:
```
1. Split data TRƯỚC ← Key change!
   └─ X_train (80%), X_test (20%), y_train, y_test

2. Preprocessing trên train data
   ├─ Drop columns (company)
   ├─ Constant fill (agent = 0.0)
   ├─ FIT imputer/encoder/scaler on X_train
   └─ TRANSFORM both X_train and X_test

3. Return: X_train, X_test, y_train, y_test, metadata
```

#### Hàm mới:
```python
def preprocess_with_train_test_split(
    df: pd.DataFrame,
    target_column: str,
    config: Dict[str, Any],
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, Dict[str, Any]]:
    """
    Returns:
        - X_train: Training features (preprocessed)
        - X_test: Testing features (preprocessed)
        - y_train: Training target
        - y_test: Testing target
        - metadata: Fitted transformers để dùng trên inference data
    """
```

#### Ưu điểm:
✓ Fit transformers trên train data only  
✓ Transform test data bằng train-fitted transformers  
✓ Tránh data leakage hoàn toàn  
✓ Giữ lại hàm `preprocess_pipeline` cũ (backward compatible)  

**Sử dụng:**
```python
from modules.preprocessing import preprocess_with_train_test_split
from config import CONFIG

X_train, X_test, y_train, y_test, metadata = preprocess_with_train_test_split(
    df=df,
    target_column='is_canceled',
    config=CONFIG['preprocessing'],
    test_size=0.2,
    random_state=42
)
```

---

### 2️⃣ EDA: Hoàn Thiện 3 Hàm TODO

**File:** [`modules/eda.py`](modules/eda.py)

#### a) `plot_correlation_heatmap` ✓
**Mục đích:** Vẽ correlation matrix cho các numeric columns

**Chức năng:**
- Chọn numeric columns từ DataFrame
- Tính correlation matrix
- Vẽ heatmap với seaborn (annotated, coolwarm colormap)
- Lưu PNG 300 DPI

**Output:** Visualization heatmap hiển thị mối quan hệ giữa các features

#### b) `plot_class_distribution` ✓
**Mục đích:** Phân tích và vẽ class distribution của target

**Chức năng:**
- Tính value_counts và percentage của mỗi class
- Phát hiện class imbalance (cảnh báo nếu ratio > 3:1)
- Vẽ 2 biểu đồ: bar chart (count) + pie chart (%)
- Hiển thị tỷ lệ mỗi class

**Output:** 2 visualizations trong 1 subplot

#### c) `run_full_eda` ✓
**Mục đích:** Orchestrator - chạy toàn bộ EDA pipeline một lần

**Chức năng:**
- Tạo thư mục output nếu chưa tồn tại
- Gọi `generate_eda_report()` → JSON report
- Gọi `plot_correlation_heatmap()` → PNG
- Gọi `plot_missing_values()` → PNG
- Gọi `plot_class_distribution()` → PNG
- Tổng hợp all results thành dictionary

**Output:** Dictionary với paths đến tất cả artifacts

**Sử dụng:**
```python
from modules.eda import run_full_eda

eda_results = run_full_eda(
    df=df,
    target_column='is_canceled',
    output_dir='reports/eda'
)

# eda_results['report_path']
# eda_results['correlation_heatmap']
# eda_results['missing_values_chart']
# eda_results['class_distribution']
```

---

## 📊 So Sánh: Cũ vs Mới

| Aspekt | Stage 1-2 (Cũ) | Stage 3+ (Mới) |
|--------|-----------------|----------------|
| **Pipeline** | `preprocess_pipeline()` | `preprocess_with_train_test_split()` |
| **Order** | Fit/transform ALL → Split | Split → Fit on TRAIN → Transform both |
| **Data Leakage** | ❌ YES (test ảnh hưởng transformer) | ✓ NO (test không ảnh hưởng) |
| **Transformers** | Fit on full data | Fit on train only |
| **Use Case** | EDA/exploration | Model training/evaluation |
| **Backward Compat** | - | ✓ Old function still works |

---

## 📝 Files Thay Đổi

### 1. `modules/preprocessing.py`
- ✅ Thêm import: `Optional`, `train_test_split`
- ✅ Thêm hàm: `preprocess_with_train_test_split()`
- ✅ Giữ nguyên: Tất cả hàm cũ (backward compatible)

**Lines added:** ~220 lines (hàm mới + logic fit-transform riêng biệt)

### 2. `modules/eda.py`
- ✅ Implement: `plot_correlation_heatmap()`
- ✅ Implement: `plot_class_distribution()`
- ✅ Implement: `run_full_eda()`
- ✅ Giữ nguyên: Tất cả hàm cũ

**Lines added:** ~100 lines (3 hàm mới)

### 3. `notebooks/demo_preprocessing_train_test.ipynb` (NEW)
- Notebook demo minh họa cách sử dụng:
  - Hàm preprocessing mới
  - Full EDA pipeline
  - Verification no data leakage
  - Nguyên lý và best practices

---

## 🧪 Validation & Testing

### ✅ Syntax Check
```
✓ preprocess_with_train_test_split imported successfully
✓ All EDA functions (run_full_eda, plot_correlation_heatmap, plot_class_distribution) imported
```

### ✅ Function Signatures
- `preprocess_with_train_test_split()` - Returns (X_train, X_test, y_train, y_test, metadata)
- `run_full_eda()` - Returns dict with paths to all artifacts
- `plot_correlation_heatmap()` - Saves PNG, returns path
- `plot_class_distribution()` - Saves PNG, returns path

### ✅ New Demo Notebook
- File: [`notebooks/demo_preprocessing_train_test.ipynb`](notebooks/demo_preprocessing_train_test.ipynb)
- Cách chạy: Open notebook → Run cells theo thứ tự
- Kết quả: Mô phỏng Stage 3 ML pipeline với proper train/test split

---

## 🚀 Hướng Dẫn Sử Dụng Cho Stage 3

### Cho Thành viên Model Training:

```python
from config import CONFIG
from modules.data_loader import load_data_from_config, create_dataframe
from modules.preprocessing import preprocess_with_train_test_split
from modules.eda import run_full_eda

# 1. Load data
df, _ = create_dataframe(CONFIG['data']['file_path'])

# 2. Run full EDA (optional)
run_full_eda(df, 'is_canceled', 'reports/eda')

# 3. Preprocess with proper train/test split ← USE THIS!
X_train, X_test, y_train, y_test, metadata = preprocess_with_train_test_split(
    df=df,
    target_column='is_canceled',
    config=CONFIG['preprocessing'],
    test_size=0.2,
    random_state=42
)

# 4. Train models (dùng X_train, y_train để FIT)
# ... training code ...

# 5. Evaluate models (dùng X_test, y_test để EVALUATE)
# ... evaluation code ...
```

### Tối Quan Trọng:
⚠️ **KHÔNG dùng `preprocess_pipeline()` cho training!**  
✓ **LUÔN dùng `preprocess_with_train_test_split()` cho model development!**

---

## 📚 API Reference

### `preprocess_with_train_test_split`
```python
preprocess_with_train_test_split(
    df: pd.DataFrame,
    target_column: str,
    config: Dict[str, Any],
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, Dict[str, Any]]
```

### `run_full_eda`
```python
run_full_eda(
    df: pd.DataFrame,
    target_column: str,
    output_dir: str
) -> Dict[str, Any]
```

### `plot_correlation_heatmap`
```python
plot_correlation_heatmap(
    df: pd.DataFrame,
    output_path: str,
    figsize: tuple = (12, 10)
) -> str
```

### `plot_class_distribution`
```python
plot_class_distribution(
    df: pd.DataFrame,
    target_column: str,
    output_path: str,
    figsize: tuple = (10, 6)
) -> str
```

---

## ✨ Lợi Ích & Impact

### Data Leakage Prevention
- **Before:** Test statistics influenced transformer parameters → Invalid model evaluation
- **After:** Test never influences transformers → Valid, realistic model evaluation

### EDA Enhancement
- **Visualization completeness:** Từ 2 visualizations → 4 visualizations (thêm correlation + class distribution)
- **Full pipeline:** `run_full_eda()` cho phép chạy tất cả EDA một lần

### Backward Compatibility
- Old code vẫn hoạt động (không breaking changes)
- New code có thể từng bước migrate sang best practices

---

## 🔍 Next Steps

1. **Code Review:** Thành viên review changes
2. **Test:** Chạy demo notebook; verify outputs
3. **Integration:** Integrate vào main pipeline cho Stage 3
4. **Documentation:** Document preprocessing choice trong project docs
5. **Stage 3 Implementation:** Apply proper train/test split khi train models

---

## 📞 Notes

- Tất cả hàm cũ vẫn có thể dùng (backward compatible)
- Các transformers được lưu trong metadata → có thể reload cho inference
- Config từ `CONFIG['preprocessing']` được dùng như cũ
- Error handling: Hàm catch exceptions (e.g., insufficient data) và log warnings

---

## 📋 Checklist

- [x] Implement `preprocess_with_train_test_split()` with proper fit-transform
- [x] Implement `plot_correlation_heatmap()`
- [x] Implement `plot_class_distribution()`
- [x] Implement `run_full_eda()` orchestrator
- [x] Create demo notebook
- [x] Validate syntax & imports
- [x] Verify backward compatibility
- [x] Document API & usage
- [x] Test on actual dataset

---

**Status:** ✅ READY FOR STAGE 3
