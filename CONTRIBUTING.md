# Contributing Guide

Hướng dẫn đóng góp cho dự án Tabular ML Pipeline.

## 👥 Team Information

**Project**: K22 HCMUT Group 6 - Machine Learning Pipeline  
**Members**: 4 thành viên  
**Course**: Machine Learning - Semester 2, Year 4

## 📋 Table of Contents

1. [Coding Standards](#coding-standards)
2. [Git Workflow](#git-workflow)
3. [Development Process](#development-process)
4. [Code Review](#code-review)
5. [Testing](#testing)
6. [Documentation](#documentation)

## 🎨 Coding Standards

### Python Style Guide

Dự án tuân theo **PEP 8** - Python Enhancement Proposal 8:

#### Naming Conventions

```python
# Variables và functions: snake_case
user_name = "John"
def calculate_accuracy(y_true, y_pred):
    pass

# Classes: PascalCase
class DataLoader:
    pass

# Constants: UPPER_CASE
MAX_ITERATIONS = 1000
DEFAULT_RANDOM_STATE = 42

# Private methods/variables: _leading_underscore
def _internal_helper():
    pass
```

#### Indentation và Spacing

```python
# 4 spaces cho indentation (KHÔNG dùng tabs)
def my_function():
    if condition:
        do_something()
        
# 2 blank lines giữa functions
def function_one():
    pass


def function_two():
    pass

# 1 blank line giữa methods trong class
class MyClass:
    def method_one(self):
        pass
    
    def method_two(self):
        pass
```

#### Line Length

- Maximum 88 characters (theo Black formatter)
- Nếu dài hơn, break into multiple lines:

```python
# Good
result = some_function(
    long_argument_1,
    long_argument_2,
    long_argument_3
)

# Bad
result = some_function(long_argument_1, long_argument_2, long_argument_3, long_argument_4)
```

### Docstrings

Sử dụng **Google Style Docstrings**:

```python
def train_model(X_train, y_train, model_params):
    """
    Train machine learning model với specified parameters.
    
    Args:
        X_train (np.ndarray): Training features, shape (n_samples, n_features)
        y_train (np.ndarray): Training labels, shape (n_samples,)
        model_params (dict): Model hyperparameters
            - 'learning_rate': Learning rate (float)
            - 'n_estimators': Number of estimators (int)
    
    Returns:
        tuple: (trained_model, training_metrics)
            - trained_model (sklearn.BaseEstimator): Trained model object
            - training_metrics (dict): Training metrics
    
    Raises:
        ValueError: Nếu X_train và y_train có different number of samples
    
    Example:
        >>> params = {'learning_rate': 0.01, 'n_estimators': 100}
        >>> model, metrics = train_model(X_train, y_train, params)
        >>> print(metrics['accuracy'])
        0.95
    """
    pass
```

### Import Order

Sắp xếp imports theo thứ tự:

```python
# 1. Standard library imports
import os
import sys
from pathlib import Path

# 2. Third-party imports
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# 3. Local application imports
from modules.data_loader import load_data
from modules.preprocessing import preprocess_pipeline
```

### Comments

```python
# TODO: Implement feature engineering logic
# FIXME: Bug in scaling logic when all values are zero
# NOTE: This function assumes data is already cleaned
# HACK: Temporary workaround until scikit-learn issue is fixed
```

## 🔀 Git Workflow

### Branch Strategy

Sử dụng **Feature Branch Workflow**:

```
main
├── develop
│   ├── feature/data-loader
│   ├── feature/eda-module
│   ├── feature/preprocessing
│   ├── feature/models-training
│   └── bugfix/missing-value-handling
```

#### Branch Naming Convention

```bash
# Feature branches
feature/<tên-feature>
feature/data-loader
feature/mlp-model

# Bugfix branches
bugfix/<tên-bug>
bugfix/encoding-error
bugfix/missing-imports

# Hotfix branches (urgent fixes)
hotfix/<tên-fix>
hotfix/critical-crash

# Experiment branches
experiment/<tên-experiment>
experiment/pca-alternatives
```

### Git Commands Workflow

#### Bắt Đầu Feature Mới

```bash
# 1. Update local main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/data-loader

# 3. Make changes and commit
git add .
git commit -m "feat: implement data loading from URL"

# 4. Push to remote
git push origin feature/data-loader

# 5. Create Pull Request trên GitHub
```

#### Commit Message Convention

Sử dụng **Conventional Commits**:

```bash
# Format
<type>(<scope>): <subject>

# Types
feat:     New feature
fix:      Bug fix
docs:     Documentation changes
style:    Code style changes (formatting, missing semicolons, etc)
refactor: Code refactoring
test:     Adding tests
chore:    Maintenance tasks
```

**Examples**:

```bash
feat(data): add load_data_from_url function
fix(preprocessing): handle edge case when all values are NaN
docs(readme): update installation instructions
refactor(eda): optimize correlation heatmap generation
test(models): add unit tests for train_logistic_regression
chore(deps): update scikit-learn to 1.3.0
```

#### Pull Request (PR) Process

1. **Create PR**: Feature branch → develop (hoặc main)
2. **Fill PR Template**:
   ```markdown
   ## Description
   Implement data loading module với support cho CSV, Excel, JSON
   
   ## Changes
   - Add load_data_from_url() function
   - Add create_dataframe() function
   - Add error handling cho invalid URLs
   
   ## Testing
   - [x] Tested với Titanic dataset
   - [x] Tested với Adult Income dataset
   - [ ] TODO: Test với local files
   
   ## Screenshots (if applicable)
   [Add screenshots]
   
   ## Related Issues
   Closes #15
   ```
3. **Request Review**: Tag 1-2 team members
4. **Address Feedback**: Make changes nếu có comments
5. **Merge**: Sau khi approved, merge vào develop/main

### Merge Conflicts

```bash
# 1. Update feature branch with latest main
git checkout feature/your-feature
git fetch origin
git merge origin/main

# 2. Resolve conflicts manually
# Edit conflicted files, remove conflict markers

# 3. Add resolved files
git add .
git commit -m "merge: resolve conflicts with main"

# 4. Push
git push origin feature/your-feature
```

## 🛠️ Development Process

### 1. Setup Environment

```bash
# Clone repository
git clone <repo-url>
cd project_folder

# Create virtual environment
python -m venv venv

# Activate venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Làm Việc Trên Module

1. Pick task từ `docs/TODO.md` hoặc GitHub Issues
2. Create feature branch
3. Implement function theo template trong module file
4. Test function locally
5. Commit với descriptive message
6. Push và create PR

### 3. Integration Testing

```bash
# Test với main_pipeline.ipynb
jupyter notebook notebooks/main_pipeline.ipynb

# Hoặc test với example_usage.ipynb
jupyter notebook notebooks/example_usage.ipynb
```

## 👀 Code Review

### Reviewer Checklist

- [ ] Code tuân theo PEP 8 style guide
- [ ] Functions có docstrings đầy đủ
- [ ] Variable names có ý nghĩa rõ ràng
- [ ] Logic dễ hiểu, không overly complex
- [ ] No hardcoded values (use config.py)
- [ ] Error handling đầy đủ (try-except where needed)
- [ ] Code có comments ở chỗ phức tạp
- [ ] No commented-out code (xóa hoặc explain why)
- [ ] Imports organized correctly
- [ ] No print statements (use logging if needed)

### Comment Examples

```python
# ✅ Good comments
# Calculate explained variance ratio for PCA components
# This threshold ensures we retain 95% of information
variance_ratio = pca.explained_variance_ratio_.sum()

# ❌ Bad comments
# Loop through data
for i in range(len(data)):  # i is counter
    pass  # Do nothing
```

## 🧪 Testing

### Manual Testing

```python
# Test individual functions
from modules.data_loader import load_data_from_url

url = "https://example.com/data.csv"
result = load_data_from_url(url, "data/test.csv")
print(f"Success: {result}")
```

### Edge Cases to Test

- **Empty data**: What if dataframe is empty?
- **Missing values**: All NaN in a column?
- **Invalid inputs**: Negative values, wrong types?
- **Large data**: Does it scale?

## 📚 Documentation

### Update Documentation Khi

1. **Add new function**: Update module README với function description
2. **Change API**: Update example_usage.ipynb
3. **Add dependencies**: Update requirements.txt
4. **Change workflow**: Update ARCHITECTURE.md

### Documentation Files

- `README.md`: Project overview
- `modules/README.md`: Module details và work assignments
- `data/README.md`: Dataset information
- `docs/ARCHITECTURE.md`: System architecture
- `docs/TODO.md`: Task tracking

## ⚠️ Common Pitfalls

### 1. Hardcoded Paths

```python
# ❌ Bad
df = pd.read_csv("C:\\Users\\MyName\\Desktop\\data.csv")

# ✅ Good
from pathlib import Path
data_path = Path("data") / "dataset.csv"
df = pd.read_csv(data_path)
```

### 2. Not Using Config

```python
# ❌ Bad
test_size = 0.2
random_state = 42

# ✅ Good
from config import CONFIG
test_size = CONFIG['models']['train_test_split']['test_size']
random_state = CONFIG['models']['train_test_split']['random_state']
```

### 3. No Error Handling

```python
# ❌ Bad
def divide(a, b):
    return a / b

# ✅ Good
def divide(a, b):
    """
    Divide a by b với error handling.
    
    Args:
        a (float): Numerator
        b (float): Denominator
    
    Returns:
        float: Result of division
    
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## 🔧 Tools

### Recommended VS Code Extensions

- **Python**: Microsoft Python extension
- **Pylance**: Fast Python language server
- **Black Formatter**: Auto-format code
- **GitLens**: Enhanced Git integration
- **Jupyter**: Notebook support

### Useful Commands

```bash
# Format code với Black
black modules/*.py

# Check style với flake8
flake8 modules/*.py

# Sort imports
isort modules/*.py
```

## 📞 Getting Help

- **Stuck?** Ask team members qua group chat
- **Bug?** Create GitHub Issue với detailed description
- **Merge conflict?** Call team meeting để resolve together
- **Design decision?** Discuss trong team before implementing

## 📝 License

This project is for educational purposes (HCMUT Machine Learning Course).

---

**Happy Coding! 🚀**
