# TODO - Task Tracking

Checklist chi tiết cho implementation của Tabular ML Pipeline.

## 📋 Overview

**Project**: K22 HCMUT Group 6 - Tabular ML Pipeline  
**Team Size**: 4 members  
**Timeline**: [Start Date] - [End Date]  
**Status**: 🟡 In Progress

## 🎯 Implementation Phases

### ✅ Phase 0: Project Setup (COMPLETED)
- [x] Tạo directory structure
- [x] Setup Git repository
- [x] Create module template files
- [x] Write documentation (README, CONTRIBUTING, ARCHITECTURE)
- [x] Setup configuration file

---

### 🔵 Phase 1: Data Ingestion & EDA (Weeks 1-2)

#### Module: data_loader.py

**Assigned to**: [Member Name 1]  
**Status**: ⏳ Not Started

- [ ] **1.1 Implement `load_data_from_url()`**
  - [ ] Use `requests` library để download file
  - [ ] Handle network errors (timeout, connection errors)
  - [ ] Add progress bar cho large files (optional: `tqdm`)
  - [ ] Verify file downloaded successfully
  - [ ] Return file path
  
- [ ] **1.2 Implement `create_dataframe()`**
  - [ ] Support CSV format (`.csv`)
  - [ ] Support Excel format (`.xlsx`, `.xls`)
  - [ ] Support JSON format (`.json`)
  - [ ] Auto-detect file format từ extension
  - [ ] Generate metadata dict (shape, dtypes, missing values)
  - [ ] Return DataFrame + metadata
  
- [ ] **1.3 Implement `load_data_pipeline()`**
  - [ ] Combine load_data_from_url() + create_dataframe()
  - [ ] Check if file already exists locally (avoid re-download)
  - [ ] Add logging messages
  - [ ] Return DataFrame + metadata

- [ ] **1.4 Testing**
  - [ ] Test với Titanic dataset
  - [ ] Test với Adult Income dataset
  - [ ] Test error handling (invalid URL, corrupted file)

#### Module: eda.py

**Assigned to**: [Member Name 2]  
**Status**: ⏳ Not Started

- [ ] **1.5 Implement `generate_eda_report()`**
  - [ ] Calculate basic statistics (mean, median, std, min, max)
  - [ ] Count missing values per column
  - [ ] List data types
  - [ ] Detect outliers (IQR method)
  - [ ] Save report to text file
  - [ ] Return report dict

- [ ] **1.6 Implement `plot_correlation_heatmap()`**
  - [ ] Calculate correlation matrix
  - [ ] Use seaborn heatmap
  - [ ] Add annotations với correlation values
  - [ ] Save plot to PNG file
  - [ ] Return file path

- [ ] **1.7 Implement `plot_missing_values()`**
  - [ ] Calculate % missing per column
  - [ ] Create bar chart
  - [ ] Highlight columns với >20% missing
  - [ ] Save plot to PNG file
  - [ ] Return file path

- [ ] **1.8 Implement `plot_class_distribution()`**
  - [ ] Count samples per class
  - [ ] Create bar chart or pie chart
  - [ ] Add percentage labels
  - [ ] Check for class imbalance
  - [ ] Save plot to PNG file
  - [ ] Return file path

- [ ] **1.9 Implement `run_full_eda()`**
  - [ ] Call all EDA functions
  - [ ] Collect results in dict
  - [ ] Return results dict

- [ ] **1.10 Testing**
  - [ ] Test với sample DataFrame
  - [ ] Verify plots are generated correctly
  - [ ] Check report contains correct statistics

**Phase 1 Deliverables**:
- Raw data downloaded and loaded into DataFrame
- EDA report generated with statistics and visualizations
- Data quality issues identified

---

### 🟢 Phase 2: Preprocessing & Feature Engineering (Weeks 3-4)

#### Module: preprocessing.py

**Assigned to**: [Member Name 3]  
**Status**: ⏳ Not Started

- [ ] **2.1 Implement `apply_imputation()`**
  - [ ] SimpleImputer cho numeric features (mean/median/most_frequent)
  - [ ] SimpleImputer cho categorical features (most_frequent)
  - [ ] KNNImputer (optional advanced method)
  - [ ] Handle case where all values are NaN
  - [ ] Return imputed DataFrame + metadata

- [ ] **2.2 Implement `apply_encoding()`**
  - [ ] OneHotEncoder cho categorical features
  - [ ] LabelEncoder (alternative)
  - [ ] Handle unknown categories (for test data)
  - [ ] Drop first category option (để avoid multicollinearity)
  - [ ] Return encoded DataFrame + metadata

- [ ] **2.3 Implement `apply_scaling()`**
  - [ ] StandardScaler (mean=0, std=1)
  - [ ] MinMaxScaler (range [0, 1])
  - [ ] Apply only to numeric features (not categorical)
  - [ ] Fit on train data, transform both train and test
  - [ ] Return scaled DataFrame + scaler object

- [ ] **2.4 Implement `preprocess_pipeline()`**
  - [ ] Separate features (X) và target (y)
  - [ ] Call apply_imputation() → apply_encoding() → apply_scaling()
  - [ ] Convert DataFrame to numpy arrays
  - [ ] Return X, y, metadata

- [ ] **2.5 Testing**
  - [ ] Test với data có missing values
  - [ ] Test với data có categorical features
  - [ ] Verify shapes are correct
  - [ ] Check no NaN values remain

#### Module: features.py

**Assigned to**: [Member Name 4]  
**Status**: ⏳ Not Started

- [ ] **2.6 Implement `apply_pca()`**
  - [ ] Fit PCA trên training data
  - [ ] Choose n_components để retain variance_threshold (e.g., 0.95)
  - [ ] Transform data
  - [ ] Calculate explained variance ratio
  - [ ] Return transformed data + PCA info dict

- [ ] **2.7 Implement `save_features()`**
  - [ ] Support NumPy format (.npy)
  - [ ] Support HDF5 format (.h5)
  - [ ] Save X và y separately
  - [ ] Add metadata (shape, dtype)
  - [ ] Return saved file path

- [ ] **2.8 Implement `load_features()`**
  - [ ] Load từ .npy file
  - [ ] Load từ .h5 file
  - [ ] Verify shapes match expectations
  - [ ] Return X, y

- [ ] **2.9 Implement `engineer_features()`**
  - [ ] Call apply_pca()
  - [ ] Call save_features()
  - [ ] Return engineered features

- [ ] **2.10 Testing**
  - [ ] Test PCA reduces dimensions correctly
  - [ ] Test save/load roundtrip
  - [ ] Verify loaded data == saved data

**Phase 2 Deliverables**:
- Clean dataset with no missing values
- Categorical features encoded to numeric
- Features scaled to appropriate range
- Dimensionality reduced with PCA
- Processed features saved to disk

---

### 🟠 Phase 3: Model Training (Weeks 5-6)

#### Module: models.py

**Assigned to**: [Member Name 1, Member Name 2]  
**Status**: ⏳ Not Started

- [ ] **3.1 Implement `train_logistic_regression()`**
  - [ ] Import LogisticRegression từ sklearn
  - [ ] Apply hyperparameters từ config
  - [ ] Fit model trên training data
  - [ ] Predict trên test data
  - [ ] Return trained model + predictions

- [ ] **3.2 Implement `train_svm()`**
  - [ ] Import SVC từ sklearn
  - [ ] Apply hyperparameters từ config (kernel, C, gamma)
  - [ ] Fit model trên training data
  - [ ] Predict trên test data
  - [ ] Return trained model + predictions

- [ ] **3.3 Implement `train_random_forest()`**
  - [ ] Import RandomForestClassifier từ sklearn
  - [ ] Apply hyperparameters từ config (n_estimators, max_depth)
  - [ ] Fit model trên training data
  - [ ] Predict trên test data
  - [ ] Return trained model + predictions

- [x] **3.4 Implement `train_mlp()` (BONUS)**
  - [ ] Build MLP model với Keras/TensorFlow
  - [ ] Define architecture: Input → Hidden Layers → Output
  - [ ] Add dropout layers để prevent overfitting
  - [ ] Compile model (optimizer, loss, metrics)
  - [ ] Add EarlyStopping callback
  - [ ] Fit model với validation split
  - [ ] Predict trên test data
  - [ ] Return trained model + predictions
  - [x] Bonus deep learning pipeline is implemented in `modules/models.py`

- [ ] **3.5 Implement `train_models_pipeline()`**
  - [ ] Split data: train_test_split()
  - [ ] Train all enabled models
  - [ ] Collect trained models in dict
  - [ ] Collect predictions in dict
  - [ ] Return models dict + predictions dict

- [ ] **3.6 Testing**
  - [ ] Test với small dataset
  - [ ] Verify predictions shape matches test data
  - [ ] Check all models train without errors

**Phase 3 Deliverables**:
- 3 traditional ML models trained (Logistic, SVM, Random Forest)
- 1 deep learning model trained (MLP - bonus)
- Predictions generated for all models

---

### 🟣 Phase 4: Evaluation & Comparison (Week 7)

#### Module: evaluation.py

**Assigned to**: [Member Name 3, Member Name 4]  
**Status**: ⏳ Not Started

- [ ] **4.1 Implement `compute_metrics()`**
  - [ ] Calculate accuracy (sklearn.metrics.accuracy_score)
  - [ ] Calculate precision (sklearn.metrics.precision_score)
  - [ ] Calculate recall (sklearn.metrics.recall_score)
  - [ ] Calculate F1-score (sklearn.metrics.f1_score)
  - [ ] Handle multi-class case (average='weighted')
  - [ ] Return metrics dict

- [ ] **4.2 Implement `plot_confusion_matrix()`**
  - [ ] Calculate confusion matrix
  - [ ] Use seaborn heatmap để visualize
  - [ ] Add labels (True Positive, False Positive, etc.)
  - [ ] Add percentage annotations
  - [ ] Save plot to PNG
  - [ ] Return file path

- [ ] **4.3 Implement `plot_roc_auc()`**
  - [ ] Get prediction probabilities (predict_proba)
  - [ ] Calculate ROC curve (fpr, tpr, thresholds)
  - [ ] Calculate AUC score
  - [ ] Plot ROC curve với AUC in legend
  - [ ] Add diagonal reference line (random classifier)
  - [ ] Save plot to PNG
  - [ ] Return file path

- [ ] **4.4 Implement `evaluate_model()`**
  - [ ] Call compute_metrics()
  - [ ] Call plot_confusion_matrix()
  - [ ] Call plot_roc_auc()
  - [ ] Collect results in dict
  - [ ] Return evaluation results

- [ ] **4.5 Implement `compare_models()`**
  - [ ] Create comparison DataFrame (rows=models, cols=metrics)
  - [ ] Create bar chart comparing all metrics
  - [ ] Highlight best model for each metric
  - [ ] Save comparison plot to PNG
  - [ ] Return file path

- [ ] **4.6 Testing**
  - [ ] Test với sample predictions
  - [ ] Verify metrics are in correct range [0, 1]
  - [ ] Check plots are generated correctly

**Phase 4 Deliverables**:
- Performance metrics for all models
- Confusion matrices generated
- ROC-AUC curves plotted
- Model comparison chart created

---

### 🔴 Phase 5: Integration & Documentation (Week 8)

**Assigned to**: All Members  
**Status**: ⏳ Not Started

- [ ] **5.1 Integration Testing**
  - [ ] Test full pipeline trong `main_pipeline.ipynb`
  - [ ] Verify all steps execute without errors
  - [ ] Check all outputs are generated
  - [ ] Test with different datasets

- [ ] **5.2 Documentation Updates**
  - [ ] Update README.md với final results
  - [ ] Add example outputs (screenshots, metrics)
  - [ ] Document known issues và limitations
  - [ ] Add setup instructions

- [ ] **5.3 Code Cleanup**
  - [ ] Remove TODO comments (replaced với implementation)
  - [ ] Remove debug print statements
  - [ ] Format code với Black
  - [ ] Check PEP8 compliance với flake8

- [ ] **5.4 Finalization**
  - [ ] Create final project report
  - [ ] Prepare presentation slides
  - [ ] Record demo video (optional)
  - [ ] Submit project

**Phase 5 Deliverables**:
- Working end-to-end pipeline
- Complete documentation
- Final project report
- Presentation materials

---

## 🎯 Quick Task Assignment Template

Copy this section và customize for your team:

```
┌─────────────────────────────────────────────────────────┐
│                   TASK ASSIGNMENTS                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Member 1: [Name]                                        │
│  Role: Data Engineer                                     │
│  Modules: data_loader.py, models.py (Logistic+SVM)     │
│  Deadline: [Date]                                        │
│                                                          │
│  Member 2: [Name]                                        │
│  Role: Data Analyst                                      │
│  Modules: eda.py, models.py (RandomForest+MLP)         │
│  Deadline: [Date]                                        │
│                                                          │
│  Member 3: [Name]                                        │
│  Role: ML Engineer                                       │
│  Modules: preprocessing.py, evaluation.py               │
│  Deadline: [Date]                                        │
│                                                          │
│  Member 4: [Name]                                        │
│  Role: Feature Engineer                                  │
│  Modules: features.py, evaluation.py (comparison)       │
│  Deadline: [Date]                                        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 📊 Progress Tracking

Update this weekly:

```
Week 1: [x] Setup complete, [_] Data loading in progress
Week 2: [ ] EDA complete
Week 3: [ ] Preprocessing complete
Week 4: [ ] Feature engineering complete
Week 5: [ ] Basic models trained
Week 6: [ ] Deep learning model trained
Week 7: [ ] Evaluation complete
Week 8: [ ] Final integration and submission
```

## 🐛 Issues Tracker

Track blockers and issues here:

| Issue ID | Description | Assigned To | Status | Resolution |
|----------|-------------|-------------|--------|------------|
| #001 | Example issue: Dataset URL không accessible | Member 1 | 🔴 Open | Try alternative dataset |
| #002 |  |  |  |  |

## 📅 Meeting Notes

### Meeting 1: [Date]
- **Attendees**: [List]
- **Agenda**: Project kickoff
- **Decisions**: 
  - Chose Titanic dataset
  - Assigned initial tasks
- **Action Items**:
  - [ ] Member 1: Setup Git repo
  - [ ] All: Review documentation

### Meeting 2: [Date]
- **Attendees**: 
- **Agenda**: 
- **Decisions**: 
- **Action Items**:

## 💡 Tips for Success

1. **Start Early**: Mỗi phase cần ~1 week, don't wait until deadline
2. **Communicate**: Use group chat để ask questions và share progress
3. **Test Incrementally**: Test mỗi function ngay sau khi implement
4. **Use Git Branches**: Create feature branch cho mỗi module
5. **Review Each Other's Code**: At least 1 person review before merge
6. **Document As You Go**: Add docstrings và comments while coding
7. **Run Full Pipeline Often**: Test integration early để catch issues
8. **Backup Work**: Commit và push code regularly

## 🎓 Learning Resources

- **PEP 8 Style Guide**: https://pep8.org/
- **Scikit-learn Documentation**: https://scikit-learn.org/stable/
- **TensorFlow/Keras Tutorials**: https://www.tensorflow.org/tutorials
- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Seaborn Gallery**: https://seaborn.pydata.org/examples/index.html

## ✅ Definition of Done

A task is considered "done" when:

- [x] Code implemented và follows PEP 8
- [x] Docstrings added for all functions
- [x] Function tested manually và works correctly
- [x] Code committed và pushed to Git
- [x] PR created và reviewed by teammate
- [x] Merged into main/develop branch
- [x] Documentation updated if needed

---

**Document Last Updated**: [Date]  
**Next Review**: [Date]

---

## 📞 Contact Information

- **Team Lead**: [Name] - [Email/Phone]
- **Member 1**: [Name] - [Email/Phone]
- **Member 2**: [Name] - [Email/Phone]
- **Member 3**: [Name] - [Email/Phone]
- **Member 4**: [Name] - [Email/Phone]
- **Instructor**: [Name] - [Email]

---

Good luck with the project! 🚀
