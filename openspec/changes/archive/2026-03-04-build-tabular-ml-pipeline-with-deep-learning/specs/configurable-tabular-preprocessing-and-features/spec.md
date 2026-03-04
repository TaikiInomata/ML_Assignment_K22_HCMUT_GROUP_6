## ADDED Requirements

### Requirement: Configurable Missing Value Imputation
The preprocessing module SHALL support missing value handling via `SimpleImputer` (mean or median) and `KNNImputer`, selected through centralized notebook config.

#### Scenario: Apply mean SimpleImputer from config
- **WHEN** config selects `SimpleImputer` with strategy `mean`
- **THEN** the system imputes missing numeric values with feature means and logs the applied strategy

#### Scenario: Apply KNN imputation from config
- **WHEN** config selects `KNNImputer`
- **THEN** the system imputes missing values using nearest-neighbor logic and returns transformed feature matrix

### Requirement: Configurable Categorical Encoding and Scaling
The preprocessing module SHALL support One-Hot Encoding and Label Encoding for categorical variables, and MUST support `MinMaxScaler` (with configurable `feature_range`) and `StandardScaler`.

#### Scenario: One-Hot and MinMax preprocessing path
- **WHEN** config selects One-Hot Encoding and `MinMaxScaler` with a specified range
- **THEN** the system encodes categorical columns and scales numeric features according to the configured range

#### Scenario: Label and Standard scaling path
- **WHEN** config selects Label Encoding and `StandardScaler`
- **THEN** the system encodes categorical columns with label mapping and standardizes numeric features

### Requirement: PCA and Feature Artifact Export
The feature module SHALL support PCA dimensionality reduction using configurable explained variance thresholds (including $90\%$ and $95\%$) and MUST export processed features to `.npy` or `.h5`.

#### Scenario: Run PCA at 95 percent explained variance
- **WHEN** config enables PCA with threshold `0.95`
- **THEN** the system reduces feature dimensions to meet or exceed 95 percent explained variance and logs resulting component count

#### Scenario: Persist features to `.npy` artifact
- **WHEN** config selects output format `.npy`
- **THEN** the system saves transformed features under the `features/` directory as a valid `.npy` file

#### Scenario: Persist features to `.h5` artifact
- **WHEN** config selects output format `.h5`
- **THEN** the system saves transformed features under the `features/` directory as a valid `.h5` file
