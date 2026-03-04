# Architecture Documentation

Tài liệu kiến trúc cho Tabular ML Pipeline Project.

## 🏗️ Tổng Quan Kiến Trúc

Dự án được thiết kế theo **modular architecture** với sự phân tách rõ ràng giữa các thành phần.

### Nguyên Tắc Thiết Kế

1. **Separation of Concerns**: Mỗi module có trách nhiệm riêng biệt
2. **Reusability**: Functions có thể tái sử dụng cho different datasets
3. **Configurability**: Tất cả parameters trong centralized config
4. **Extensibility**: Dễ dàng thêm models/features mới
5. **Testability**: Mỗi module có thể test độc lập

## 📊 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                              │
│                                                                       │
│  ┌──────────────────────┐         ┌──────────────────────┐          │
│  │ main_pipeline.ipynb  │         │ example_usage.ipynb  │          │
│  │ (Main orchestration) │         │ (Usage examples)      │          │
│  └──────────┬───────────┘         └──────────────────────┘          │
└─────────────┼─────────────────────────────────────────────────────┬─┘
              │                                                       │
              │ Import modules                                       │
              ▼                                                       │
┌─────────────────────────────────────────────────────────────────┐  │
│                       CONFIGURATION LAYER                        │  │
│                                                                   │  │
│  ┌──────────────────────────────────────────────────────────┐   │  │
│  │                      config.py                            │   │  │
│  │  • Data config  • EDA config                             │   │  │
│  │  • Preprocessing config  • Features config               │   │  │
│  │  • Models config  • Evaluation config                    │   │  │
│  └──────────────────────────────────────────────────────────┘   │  │
└───────────────────────────────┬─────────────────────────────────┘  │
                                │ Used by all modules                │
                                ▼                                    │
┌─────────────────────────────────────────────────────────────────┐  │
│                       PROCESSING MODULES                         │  │
│                                                                   │  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐│  │
│  │    data_   │  │            │  │   pre-     │  │            ││  │
│  │   loader   │─▶│    eda     │─▶│ processing │─▶│  features  ││  │
│  │            │  │            │  │            │  │            ││  │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘│  │
│         │                │                │              │       │  │
│         ▼                ▼                ▼              ▼       │  │
│  ┌─────────────────────────────────────────────────────────┐   │  │
│  │                    Data Storage                          │   │  │
│  │  data/*.csv    reports/eda/*.png    features/*.npy      │   │  │
│  └─────────────────────────────────────────────────────────┘   │  │
│                                                                   │  │
│  ┌────────────┐────────────────────────────┐                    │  │
│  │            │                             │                    │  │
│  │   models   │──▶  evaluation  ──▶ reports/evaluation/*.png   │  │
│  │            │                             │                    │  │
│  └────────────┘────────────────────────────┘                    │  │
└─────────────────────────────────────────────────────────────────┘  │
                                                                      │
                                    Uses configuration ──────────────┘
```

## 🔄 Data Flow Pipeline

### End-to-End Data Flow

```
┌──────────────┐
│  Raw Data    │ (URL or local file)
│  (Dataset)   │
└──────┬───────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  STEP 1: Data Ingestion                  │
│  Module: data_loader                      │
│                                           │
│  • load_data_from_url()                  │
│  • create_dataframe()                    │
│                                           │
│  Output: Raw DataFrame                    │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│  STEP 2: Exploratory Data Analysis       │
│  Module: eda                              │
│                                           │
│  • generate_eda_report()                 │
│  • plot_correlation_heatmap()            │
│  • plot_missing_values()                 │
│  • plot_class_distribution()             │
│                                           │
│  Output: EDA reports + visualizations     │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│  STEP 3: Preprocessing                   │
│  Module: preprocessing                    │
│                                           │
│  Step 3.1: Imputation                    │
│    • Handle missing values                │
│    • SimpleImputer / KNNImputer          │
│                                           │
│  Step 3.2: Encoding                      │
│    • Convert categorical → numeric        │
│    • OneHotEncoder / LabelEncoder        │
│                                           │
│  Step 3.3: Scaling                       │
│    • Normalize numeric features           │
│    • StandardScaler / MinMaxScaler       │
│                                           │
│  Output: Clean X, y arrays                │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│  STEP 4: Feature Engineering             │
│  Module: features                         │
│                                           │
│  • apply_pca() - Dimensionality reduction│
│  • save_features() - Persist to disk     │
│                                           │
│  Output: Engineered features (X_pca, y)  │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│  STEP 5: Model Training                  │
│  Module: models                           │
│                                           │
│  Train multiple models:                   │
│  • Logistic Regression (baseline)        │
│  • SVM (Support Vector Machine)          │
│  • Random Forest (ensemble)              │
│  • MLP (Deep Learning - bonus)           │
│                                           │
│  Output: Trained models + predictions     │
└─────────────────┬─────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────┐
│  STEP 6: Evaluation & Comparison         │
│  Module: evaluation                       │
│                                           │
│  • compute_metrics() - Accuracy, F1, etc │
│  • plot_confusion_matrix()               │
│  • plot_roc_auc()                        │
│  • compare_models()                      │
│                                           │
│  Output: Evaluation reports & plots       │
└──────────────────────────────────────────┘
```

## 🧩 Module Details

### 1. data_loader Module

**Purpose**: Load và prepare raw data  
**Inputs**: URL hoặc file path  
**Outputs**: pandas DataFrame + metadata

```python
# Key functions
load_data_from_url(url, output_path)
  ↓
create_dataframe(file_path)
  ↓
DataFrame + metadata dict
```

**Data Flow**:
```
URL → Download → Disk → Parse → DataFrame
```

### 2. eda Module

**Purpose**: Analyze và visualize data patterns  
**Inputs**: Raw DataFrame  
**Outputs**: Statistical reports + plots

```python
# Key functions
run_full_eda(df, target_column, output_dir)
  ├─ generate_eda_report()
  ├─ plot_correlation_heatmap()
  ├─ plot_missing_values()
  └─ plot_class_distribution()
```

**Artifacts Generated**:
- `reports/eda/eda_report.txt` - Statistical summary
- `reports/eda/correlation_heatmap.png` - Feature correlations
- `reports/eda/missing_values.png` - Missing data visualization
- `reports/eda/class_distribution.png` - Target distribution

### 3. preprocessing Module

**Purpose**: Clean và transform data  
**Inputs**: Raw DataFrame  
**Outputs**: Cleaned X, y arrays

```python
# Pipeline
preprocess_pipeline(df, target_column, config)
  ├─ apply_imputation(df, config)       # Handle NaN
  ├─ apply_encoding(df, config)         # Categorical → numeric
  └─ apply_scaling(df, config)          # Normalize values
     ↓
  X (features), y (target), metadata
```

**Transformations**:
1. **Imputation**: `NaN → mean/median/mode`
2. **Encoding**: `categorical strings → numeric codes`
3. **Scaling**: `arbitrary ranges → [0, 1] or standardized`

### 4. features Module

**Purpose**: Engineer và persist features  
**Inputs**: Preprocessed X, y  
**Outputs**: Engineered features (saved to disk)

```python
# Pipeline
engineer_features(X, y, config)
  ├─ apply_pca(X, config)               # Reduce dimensions
  └─ save_features(X_pca, y, config)    # Persist to .npy/.h5
     ↓
  X_pca (reduced features), y
```

**Storage Formats**:
- `.npy`: NumPy binary format (fast, simple)
- `.h5`: HDF5 format (compressed, large data)

### 5. models Module

**Purpose**: Train classification models  
**Inputs**: X_train, y_train, X_test  
**Outputs**: Trained models + predictions

```python
# Train each model
train_models_pipeline(X_train, y_train, X_test, y_test, config)
  ├─ train_logistic_regression()
  ├─ train_svm()
  ├─ train_random_forest()
  └─ train_mlp()                        # Deep learning (bonus)
     ↓
  models dict + predictions dict
```

**Models Architecture**:

```
Traditional ML Models:
┌────────────────────┐
│ Logistic Regression│  Linear decision boundary
│ (sklearn)          │  Fast, interpretable
└────────────────────┘

┌────────────────────┐
│ SVM (RBF kernel)   │  Non-linear decision boundary
│ (sklearn)          │  Good for medium data
└────────────────────┘

┌────────────────────┐
│ Random Forest      │  Ensemble of decision trees
│ (sklearn)          │  Robust, handles overfitting
└────────────────────┘

Deep Learning Model:
┌────────────────────────────────────┐
│ Multi-Layer Perceptron (MLP)       │
│                                     │
│  Input Layer → Hidden Layers → Output
│  (n_features)   [128, 64, 32]   (n_classes)
│                   ↓                 │
│                 ReLU + Dropout      │
│                                     │
│  Framework: TensorFlow/Keras       │
└────────────────────────────────────┘
```

### 6. evaluation Module

**Purpose**: Measure và compare model performance  
**Inputs**: y_test, predictions, trained models  
**Outputs**: Metrics + visualization plots

```python
# Evaluation pipeline
compare_models(results, output_path)
  ├─ compute_metrics()                  # Accuracy, Precision, Recall, F1
  ├─ plot_confusion_matrix()            # True/False Positives/Negatives
  └─ plot_roc_auc()                     # ROC curve + AUC score
     ↓
  Comparison plots + metrics dict
```

**Metrics Computed**:
- **Accuracy**: % correct predictions
- **Precision**: % of positive predictions that are correct
- **Recall**: % of actual positives found
- **F1-Score**: Harmonic mean of precision & recall
- **ROC-AUC**: Area under ROC curve (classification quality)

## 📁 File System Organization

```
project_folder/
├── config.py                    # Centralized configuration
├── requirements.txt             # Dependencies
├── README.md                    # Project overview
├── CONTRIBUTING.md              # Development guidelines
├── .gitignore                   # Git ignore rules
│
├── notebooks/                   # Jupyter notebooks
│   ├── main_pipeline.ipynb      # Main workflow orchestration
│   └── example_usage.ipynb      # Module usage examples
│
├── modules/                     # Python modules (core logic)
│   ├── __init__.py
│   ├── data_loader.py           # Data ingestion
│   ├── eda.py                   # Exploratory analysis
│   ├── preprocessing.py         # Data cleaning
│   ├── features.py              # Feature engineering
│   ├── models.py                # Model training
│   └── evaluation.py            # Model evaluation
│
├── data/                        # Raw datasets (gitignored)
│   ├── .gitkeep
│   ├── README.md                # Dataset documentation
│   └── *.csv                    # Downloaded datasets
│
├── features/                    # Engineered features (gitignored)
│   ├── .gitkeep
│   └── *.npy / *.h5            # Saved feature arrays
│
├── reports/                     # Analysis outputs (gitignored)
│   ├── eda/                     # EDA visualizations
│   │   ├── .gitkeep
│   │   └── *.png
│   └── evaluation/              # Model evaluation plots
│       ├── .gitkeep
│       └── *.png
│
└── docs/                        # Documentation
    ├── ARCHITECTURE.md          # This file
    └── TODO.md                  # Task tracking
```

## 🔌 Integration Points

### Notebook ↔ Modules

```python
# In main_pipeline.ipynb

# Import modules
from modules.data_loader import load_data_pipeline
from modules.preprocessing import preprocess_pipeline
from modules.models import train_models_pipeline

# Use config
from config import CONFIG

# Execute pipeline
df, _ = load_data_pipeline(
    CONFIG['data']['url'],
    CONFIG['data']['file_path']
)
```

### Module ↔ Config

```python
# In modules/models.py

from config import CONFIG

def train_models_pipeline(X_train, y_train, X_test, y_test, config=None):
    # Use config parameter or fall back to global CONFIG
    if config is None:
        config = CONFIG['models']
    
    # Access parameters
    test_size = config['train_test_split']['test_size']
    lr_params = config['logistic_regression']['params']
```

### Module ↔ Storage

```python
# Save features to disk
from modules.features import save_features

save_config = {
    'format': 'npy',
    'path': 'features/processed_features'
}
save_features(X_pca, y, save_config)

# Later: Load features from disk
from modules.features import load_features

X_loaded, y_loaded = load_features(
    'features/processed_features',
    'npy'
)
```

## 🔄 State Management

### Checkpointing Strategy

```python
# After each major step, save intermediate results

# After data loading
df.to_csv('data/checkpoint_raw.csv', index=False)

# After preprocessing
np.save('features/checkpoint_preprocessed_X.npy', X)
np.save('features/checkpoint_preprocessed_y.npy', y)

# After feature engineering
np.save('features/checkpoint_features_X.npy', X_pca)
np.save('features/checkpoint_features_y.npy', y)
```

**Benefits**:
- Resume pipeline từ bất kỳ điểm nào
- Debug individual steps mà không rerun toàn bộ
- Fast iteration during development

## 🚀 Execution Flow

### Sequential Execution (Main Pipeline)

```
Start
  ↓
Load Config
  ↓
Step 1: Load Data → DataFrame df
  ↓
Step 2: EDA → Reports & Plots
  ↓
Step 3: Preprocess → X, y
  ↓
Step 4: Engineer Features → X_pca, y
  ↓
Step 5: Train Models → models dict, predictions dict
  ↓
Step 6: Evaluate → metrics, comparison plots
  ↓
End
```

### Parallel Execution (Model Training)

```
Split data: X_train, X_test, y_train, y_test
  ↓
┌───────────────┬───────────────┬───────────────┬───────────────┐
│ Train Model 1 │ Train Model 2 │ Train Model 3 │ Train Model 4 │
│ (Logistic)    │ (SVM)         │ (RandomForest)│ (MLP)         │
└───────┬───────┴───────┬───────┴───────┬───────┴───────┬───────┘
        │               │               │               │
        └───────────────┴───────────────┴───────────────┘
                              ↓
                      Collect results
                              ↓
                      Compare & Evaluate
```

## ⚙️ Configuration Management

### Hierarchical Config Structure

```
CONFIG
├── data
│   ├── url
│   ├── file_path
│   └── target_column
├── eda
│   ├── enabled
│   ├── output_dir
│   └── figsize
├── preprocessing
│   ├── imputation (method, strategy)
│   ├── encoding (method, drop_first)
│   └── scaling (method, feature_range)
├── features
│   ├── pca (enabled, variance_threshold)
│   └── output (format, path)
├── models
│   ├── train_test_split (test_size, random_state)
│   ├── logistic_regression (enabled, params)
│   ├── svm (enabled, params)
│   ├── random_forest (enabled, params)
│   └── mlp (enabled, params)
└── evaluation
    ├── metrics
    ├── generate_confusion_matrix
    ├── generate_roc_auc
    └── output_dir
```

## 🧪 Testing Strategy

### Unit Testing (Future Improvement)

```python
# Test individual functions
def test_load_data_from_url():
    url = "https://example.com/data.csv"
    result = load_data_from_url(url, "test.csv")
    assert Path(result).exists()

def test_apply_pca():
    X = np.random.rand(100, 20)
    config = {'variance_threshold': 0.95}
    X_pca, info = apply_pca(X, config)
    assert X_pca.shape[1] < X.shape[1]
```

### Integration Testing

```python
# Test full pipeline
def test_full_pipeline():
    # Load config
    config = get_config()
    
    # Run pipeline
    results = run_full_pipeline(config)
    
    # Verify outputs
    assert 'models' in results
    assert 'metrics' in results
    assert len(results['metrics']) == 4  # 4 models
```

## 🔒 Error Handling

### Error Propagation

```
Module Level Errors
  ↓
Try-Except blocks trong functions
  ↓
Log error với descriptive message
  ↓
Raise exception or return error status
  ↓
Notebook Level
  ↓
Display error to user
  ↓
Stop execution or skip step
```

## 📈 Scalability Considerations

### Current Limitations
- **Memory**: All data loaded into RAM (pandas DataFrame)
- **Single Machine**: No distributed computing
- **Sequential**: Most steps run sequentially

### Future Improvements
- **Chunked Processing**: Process large files in chunks
- **Dask/Modin**: Parallel DataFrame operations
- **Model Parallelism**: Train models in parallel (multiprocessing)
- **Pipeline Caching**: Cache intermediate results

## 🎯 Design Decisions

### Why Modular Architecture?
- **Team Collaboration**: 4 members can work on different modules simultaneously
- **Testing**: Each module can be tested independently
- **Maintenance**: Easy to update one module without affecting others

### Why Config File?
- **Experimentation**: Change hyperparameters without modifying code
- **Reproducibility**: Same config = same results
- **Version Control**: Track parameter changes over time

### Why Jupyter Notebooks for Orchestration?
- **Visualization**: Perfect for displaying plots và results
- **Iteration**: Easy to rerun specific cells during development
- **Documentation**: Markdown cells explain workflow
- **Google Colab Compatible**: Can run trong cloud environment

---

**Document Version**: 1.0  
**Last Updated**: [Date]  
**Maintained By**: K22 HCMUT Group 6
