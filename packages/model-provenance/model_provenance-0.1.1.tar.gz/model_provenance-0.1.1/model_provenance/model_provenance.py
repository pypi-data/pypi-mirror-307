import joblib
import json
import time
import numpy as np
import pandas as pd
import scipy.sparse as sp
from typing import Any, Dict, Optional
import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
def normalize_for_json(data):
    """
    Recursively convert non-serializable types (like np.int64) into JSON-compatible formats.
    """
    if isinstance(data, dict):
        return {key: normalize_for_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [normalize_for_json(element) for element in data]
    elif isinstance(data, np.integer):
        return int(data)
    elif isinstance(data, np.floating):
        return float(data)
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, pd.Series) or isinstance(data, pd.DataFrame):
        return data.to_dict(orient='list')
    else:
        return data

class ModelProvenance:
    def __init__(self, model: Any, version: str = "1.0.0", seed: Optional[int] = None, custom_metadata: Dict[str, Any] = None):
        self.model = model
        self.metadata = {
            'version': version,
            'created_at': time.strftime("%Y-%m-%d %H:%M:%S"),
            'seed': seed,
            'training_params': None,
            'example_data_path': None,
            'dataset_info': None,
            'model_info': self._extract_model_info(model),
            'dependencies': self._get_dependencies(),
            'custom_metadata': custom_metadata or {}
        }

    def _extract_model_info(self, model: Any) -> Dict[str, Any]:
        model_info = {
            'type': type(model).__name__,
            'package_version': self._get_package_version(model)
        }
        logger.info("Model info extracted: %s", model_info)
        return model_info

    def _get_package_version(self, model: Any) -> str:
        if hasattr(model, '__module__'):
            module_name = model.__module__.split('.')[0]
            try:
                module = __import__(module_name)
                return getattr(module, '__version__', 'unknown')
            except ImportError:
                return 'unknown'
        return 'unknown'

    def _prepare_data_info(self, X: Any, y: Any = None) -> Dict[str, Any]:
        data_info = {'X_type': type(X).__name__}
        
        if isinstance(X, np.ndarray):
            data_info.update({'X_shape': X.shape, 'X_samples': X[:5].tolist()})
        elif isinstance(X, pd.DataFrame):
            data_info.update({'X_shape': X.shape, 'X_columns': X.columns.tolist(), 'X_samples': X.head().to_dict(orient='list')})
        elif isinstance(X, sp.spmatrix):
            data_info.update({'X_shape': X.shape, 'X_type': 'scipy.sparse matrix', 'X_samples': X[:5].toarray().tolist()})
        elif isinstance(X, list):
            data_info.update({'X_length': len(X), 'X_samples': X[:5] if len(X) >= 5 else X})
        else:
            logger.warning("Unsupported data type for X: %s", type(X))
            data_info['X_samples'] = 'Unknown'

        if y is not None:
            if isinstance(y, np.ndarray):
                data_info['y_shape'] = y.shape
                data_info['y_samples'] = y[:5].tolist()
            elif isinstance(y, pd.Series):
                data_info['y_shape'] = y.shape
                data_info['y_samples'] = y.head().tolist()
            elif isinstance(y, list):
                data_info['y_length'] = len(y)
                data_info['y_samples'] = y[:5]
            else:
                logger.warning("Unsupported data type for y: %s", type(y))
                data_info['y_samples'] = 'Unknown'

        return data_info

    def _get_dependencies(self) -> Dict[str, str]:
        dependencies = {}
        for module_name in ['numpy', 'pandas', 'scipy', 'sklearn', 'xgboost']:
            try:
                module = __import__(module_name)
                dependencies[module_name] = getattr(module, '__version__', 'unknown')
            except ImportError:
                dependencies[module_name] = 'not installed'
        logger.info("Dependencies captured: %s", dependencies)
        return dependencies

    def fit(self, X, y, *args, **kwargs):
        self.metadata['dataset_info'] = self._prepare_data_info(X, y)
        self.metadata['training_params'] = kwargs

        try:
            self.model.fit(X, y, *args, **kwargs)
            logger.info("Model training completed.")
        except Exception as e:
            logger.error("Model training failed: %s", e)
            raise e

        return self

    def predict(self, X, *args, **kwargs):
        try:
            return self.model.predict(X, *args, **kwargs)
        except Exception as e:
            logger.error("Prediction failed: %s", e)
            raise e

    def save(self, model_path: str, metadata_path: str = None, example_data_path: str = None):
        joblib.dump(self.model, model_path)
    
        if example_data_path:
            self._save_example_data(self.metadata['dataset_info']['X_samples'], example_data_path)
            self.metadata['example_data_path'] = example_data_path

        if metadata_path is None:
            metadata_path = model_path.replace('.joblib', '_metadata.json')
    
        # Normalize metadata before saving as JSON
        normalized_metadata = normalize_for_json(self.metadata)
        with open(metadata_path, 'w') as f:
            json.dump(normalized_metadata, f, indent=4)
    
        logger.info("Model saved to %s, metadata saved to %s, example data saved to %s", model_path, metadata_path, example_data_path or 'N/A')

    def _save_example_data(self, example_data: Any, example_data_path: str):
        joblib.dump(example_data, example_data_path)
        logger.info("Example data saved to %s", example_data_path)

    def save_dataset(self, X, y, dataset_path: str):
        if isinstance(X, pd.DataFrame):
            X.to_csv(f"{dataset_path}_X.csv", index=False)
        elif isinstance(X, np.ndarray):
            np.savetxt(f"{dataset_path}_X.csv", X, delimiter=",")
        elif sp.issparse(X):
            sp.save_npz(f"{dataset_path}_X.npz", X)
        else:
            raise ValueError("Unsupported format for X dataset")

        if y is not None:
            if isinstance(y, pd.Series):
                y.to_csv(f"{dataset_path}_y.csv", index=False)
            elif isinstance(y, np.ndarray):
                np.savetxt(f"{dataset_path}_y.csv", y, delimiter=",")
            else:
                raise ValueError("Unsupported format for y dataset")
        
        logger.info("Dataset saved at %s_X.csv and %s_y.csv", dataset_path, dataset_path)

    @staticmethod
    def load(model_path: str, metadata_path: str = None, example_data_path: str = None):
        model = joblib.load(model_path)
        
        if metadata_path is None:
            metadata_path = model_path.replace('.joblib', '_metadata.json')
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        meta_model = ModelProvenance(model)
        meta_model.metadata = metadata
        
        if example_data_path:
            meta_model.metadata['example_data'] = joblib.load(example_data_path)
        
        logger.info("Model and metadata loaded from %s and %s", model_path, metadata_path)
        return meta_model
