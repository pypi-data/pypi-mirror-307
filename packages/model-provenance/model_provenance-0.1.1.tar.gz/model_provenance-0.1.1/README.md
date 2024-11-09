# ML Provenance Wrapper
![CI](https://github.com/DGaffney/ml-provenance-wrapper/actions/workflows/ci.yml/badge.svg)
`ML Provenance Wrapper` is a Python package that helps track metadata and provenance information for machine learning models. Designed to integrate seamlessly with scikit-learn and other models with `fit`/`predict` methods, it provides a convenient way to store important metadata such as training parameters, dataset characteristics, dependencies, and example data. This makes your models reproducible and easier to manage across projects and versions.

## Features

- **Model Metadata**: Tracks version, training parameters, dependencies, and custom metadata.
- **Dataset Info**: Captures data types, shapes, and a few example rows.
- **Compatibility**: Works with scikit-learn models, pipelines, XGBoost, and more.
- **Flexible Data Handling**: Supports numpy arrays, pandas DataFrames, sparse matrices, and lists.
- **Separate Storage for Model and Metadata**: Saves model, metadata, and example data in organized files.
- **Easy Dataset Export**: Allows exporting the datasets used in training/testing for future reference.

## Installation

To install the package from source, clone the repository and install using `pip`:

```bash
git clone https://github.com/DGaffney/ml-provenance-wrapper.git
cd ml-provenance-wrapper
pip install -e .
```
## Usage

Here's how to use `ModelProvenance` to wrap and track metadata for a model.

### Example with a scikit-learn Model

```python
from model_provenance import ModelProvenance
from sklearn.linear_model import LogisticRegression
import numpy as np

# Sample data
X = np.random.rand(100, 10)
y = np.random.randint(2, size=100)

# Initialize and train the model with provenance tracking
model = LogisticRegression()
provenance_model = ModelProvenance(model, version="1.0.0", seed=42)
provenance_model.fit(X, y)

# Save the model, metadata, and example data
provenance_model.save('logistic_model.joblib', 'logistic_metadata.json', 'example_data.joblib')`
```

### Example with a scikit-learn Pipeline

```python
from model_provenance import ModelProvenance
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import numpy as np

# Sample data
X = np.random.rand(100, 10)
y = np.random.randint(2, size=100)

# Create a pipeline model
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', SVC(kernel='linear'))
])

# Initialize and train the pipeline with provenance tracking
provenance_pipeline = ModelProvenance(pipeline, version="1.0.1")
provenance_pipeline.fit(X, y)

# Save the model, metadata, and example data
provenance_pipeline.save('pipeline_model.joblib', 'pipeline_metadata.json', 'example_data_pipeline.joblib')`
```

### Loading a Model with Metadata

To reload a previously saved model along with its metadata:

```python
from model_provenance import ModelProvenance

# Load the model and its metadata
loaded_provenance_model = ModelProvenance.load('logistic_model.joblib', 'logistic_metadata.json', 'example_data.joblib')

# Access metadata
print("Model Version:", loaded_provenance_model.metadata['version'])
print("Training Parameters:", loaded_provenance_model.metadata['training_params'])
print("Dataset Info:", loaded_provenance_model.metadata['dataset_info'])`
```

### Exporting Datasets

To save the training dataset separately:

```python
# Save dataset used in training (X, y) as CSV
provenance_model.save_dataset(X, y, "training_data")`
```

### Running Tests

The package uses `unittest` for testing. To run the test suite, navigate to the root directory and run:

```bash
python -m unittest discover -s tests
```

The tests cover:

-   Different data types (numpy arrays, pandas DataFrames, sparse matrices, lists).
-   Metadata and dataset export functionality.
-   Pipeline compatibility.

### Contributing

Contributions are welcome! If you find a bug or want to add a new feature, please open an issue or submit a pull request.

### License

This project is licensed under the MIT License. See the LICENSE file for more details.