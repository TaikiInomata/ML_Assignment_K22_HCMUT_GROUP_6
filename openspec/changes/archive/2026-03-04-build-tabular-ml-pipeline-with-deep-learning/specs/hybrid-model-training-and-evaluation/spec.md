## ADDED Requirements

### Requirement: Dictionary-Driven Model Configuration
The training module SHALL accept model hyperparameters through dictionary inputs for all supported models to enable reproducible comparisons.

#### Scenario: Train Logistic Regression with dictionary parameters
- **WHEN** user passes a parameter dictionary for Logistic Regression in config
- **THEN** the system initializes and trains the model using only values from that dictionary

### Requirement: Traditional Model Support
The modeling module SHALL support Logistic Regression, SVM, and Random Forest as baseline traditional classifiers over tabular features.

#### Scenario: Train and evaluate Random Forest baseline
- **WHEN** config selects Random Forest with valid training data
- **THEN** the system trains Random Forest and returns predictions for the evaluation stage

### Requirement: MLP Bonus Pipeline Support
The modeling module SHALL provide a simple TensorFlow/Keras MLP pipeline for tabular classification as bonus deep learning functionality.

#### Scenario: Train MLP with configured architecture
- **WHEN** config enables deep learning mode and provides MLP parameters
- **THEN** the system builds and trains an MLP model and outputs prediction scores compatible with evaluation functions

### Requirement: Standard Evaluation Metrics and Visual Diagnostics
The evaluation module SHALL compute Accuracy, Precision, Recall, and F1-score, and MUST generate Confusion Matrix and ROC-AUC visual outputs for classification results.

#### Scenario: Compute required metric set
- **WHEN** true labels and predicted labels are provided to evaluation
- **THEN** the system returns Accuracy, Precision, Recall, and F1-score in a structured summary

#### Scenario: Create confusion matrix and ROC-AUC artifacts
- **WHEN** prediction labels and prediction scores are available
- **THEN** the system generates confusion matrix and ROC-AUC plots suitable for inclusion in `reports/`
