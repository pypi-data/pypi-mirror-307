import os
import joblib
import json
import numpy as np
import pandas as pd
import scipy.sparse as sp
import unittest
from model_provenance.model_provenance import ModelProvenance
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

class TestModelProvenance(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model = LogisticRegression()
        cls.version = "1.0.0"
        cls.seed = 42
        cls.custom_metadata = {"experiment": "test"}

    def setUp(self):
        self.model_provenance = ModelProvenance(
            model=self.model,
            version=self.version,
            seed=self.seed,
            custom_metadata=self.custom_metadata
        )

        self.cleanup_files = []

    def tearDown(self):
        for filepath in self.cleanup_files:
            if os.path.exists(filepath):
                os.remove(filepath)

    def test_numpy_array_data(self):
        X = np.random.rand(100, 10)
        y = np.random.randint(2, size=100)

        # Fit and save model with numpy data
        self.model_provenance.fit(X, y)
        self.assertIsNotNone(self.model_provenance.metadata['dataset_info'])

        # Test saving model and metadata
        model_path = 'test_model.joblib'
        metadata_path = 'test_model_metadata.json'
        example_data_path = 'test_example_data.joblib'
        self.model_provenance.save(model_path, metadata_path, example_data_path)

        # Check files were created
        self.cleanup_files.extend([model_path, metadata_path, example_data_path])
        self.assertTrue(os.path.exists(model_path))
        self.assertTrue(os.path.exists(metadata_path))
        self.assertTrue(os.path.exists(example_data_path))

    def test_pandas_dataframe_data(self):
        X = pd.DataFrame(np.random.rand(100, 10), columns=[f"feature_{i}" for i in range(10)])
        y = pd.Series(np.random.randint(2, size=100))

        # Fit and save model with pandas DataFrame
        self.model_provenance.fit(X, y)
        self.assertIsNotNone(self.model_provenance.metadata['dataset_info'])

        model_path = 'test_model_df.joblib'
        metadata_path = 'test_model_df_metadata.json'
        example_data_path = 'test_example_data_df.joblib'
        self.model_provenance.save(model_path, metadata_path, example_data_path)

        self.cleanup_files.extend([model_path, metadata_path, example_data_path])
        self.assertTrue(os.path.exists(model_path))
        self.assertTrue(os.path.exists(metadata_path))
        self.assertTrue(os.path.exists(example_data_path))

    def test_sparse_matrix_data(self):
        X = sp.csr_matrix(np.random.rand(100, 10))
        y = np.random.randint(2, size=100)

        # Fit and save model with sparse matrix
        self.model_provenance.fit(X, y)
        self.assertIsNotNone(self.model_provenance.metadata['dataset_info'])

        model_path = 'test_model_sparse.joblib'
        metadata_path = 'test_model_sparse_metadata.json'
        example_data_path = 'test_example_data_sparse.joblib'
        self.model_provenance.save(model_path, metadata_path, example_data_path)

        self.cleanup_files.extend([model_path, metadata_path, example_data_path])
        self.assertTrue(os.path.exists(model_path))
        self.assertTrue(os.path.exists(metadata_path))
        self.assertTrue(os.path.exists(example_data_path))

    def test_list_data(self):
        X = [[i] * 10 for i in range(100)]
        y = [0 if i < 50 else 1 for i in range(100)]

        # Fit and save model with list data
        self.model_provenance.fit(X, y)
        self.assertIsNotNone(self.model_provenance.metadata['dataset_info'])

        model_path = 'test_model_list.joblib'
        metadata_path = 'test_model_list_metadata.json'
        example_data_path = 'test_example_data_list.joblib'
        self.model_provenance.save(model_path, metadata_path, example_data_path)

        self.cleanup_files.extend([model_path, metadata_path, example_data_path])
        self.assertTrue(os.path.exists(model_path))
        self.assertTrue(os.path.exists(metadata_path))
        self.assertTrue(os.path.exists(example_data_path))

    def test_pipeline(self):
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('classifier', LogisticRegression())
        ])
        model_provenance_pipeline = ModelProvenance(
            model=pipeline,
            version=self.version,
            seed=self.seed,
            custom_metadata=self.custom_metadata
        )

        X = np.random.rand(100, 10)
        y = np.random.randint(2, size=100)

        # Fit and save model with pipeline
        model_provenance_pipeline.fit(X, y)
        self.assertIsNotNone(model_provenance_pipeline.metadata['dataset_info'])

        model_path = 'test_model_pipeline.joblib'
        metadata_path = 'test_model_pipeline_metadata.json'
        example_data_path = 'test_example_data_pipeline.joblib'
        model_provenance_pipeline.save(model_path, metadata_path, example_data_path)

        self.cleanup_files.extend([model_path, metadata_path, example_data_path])
        self.assertTrue(os.path.exists(model_path))
        self.assertTrue(os.path.exists(metadata_path))
        self.assertTrue(os.path.exists(example_data_path))

    def test_metadata_integrity(self):
        X = np.random.rand(100, 10)
        y = np.random.randint(2, size=100)

        model_path = 'test_model_metadata.joblib'
        metadata_path = 'test_model_metadata.json'
        example_data_path = 'test_example_data_metadata.joblib'
        self.cleanup_files.extend([model_path, metadata_path, example_data_path])

        self.model_provenance.fit(X, y)
        self.model_provenance.save(model_path, metadata_path, example_data_path)

        # Reload model and metadata
        loaded_model_provenance = ModelProvenance.load(model_path, metadata_path, example_data_path)
        
        # Check integrity of metadata
        self.assertEqual(loaded_model_provenance.metadata['version'], self.version)
        self.assertEqual(loaded_model_provenance.metadata['seed'], self.seed)
        self.assertEqual(loaded_model_provenance.metadata['custom_metadata'], self.custom_metadata)
        
        # Check metadata content
        with open(metadata_path, 'r') as f:
            metadata_content = json.load(f)
        self.assertEqual(metadata_content['version'], self.version)
        self.assertEqual(metadata_content['seed'], self.seed)
        self.assertEqual(metadata_content['custom_metadata'], self.custom_metadata)

if __name__ == '__main__':
    unittest.main()
