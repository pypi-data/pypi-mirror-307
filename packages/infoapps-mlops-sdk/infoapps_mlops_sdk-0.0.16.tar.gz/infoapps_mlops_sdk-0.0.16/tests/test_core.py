import os
import unittest

from turihub import User

from ..src.infoapps_mlops_sdk.integrations.keras_callback import MLOpsKerasCallback
from ..src.infoapps_mlops_sdk.core import PlatformType, init_experiment, HubPlatform


class TestHubPlatformReal(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load the API token from an environment variable
        cls.api_token = os.getenv("MLOPS_BIGSUR_TURI_API_KEY")
        cls.project_name = "infoapps_mlops_devel"  # Use a dedicated test project

        # Ensure that the token is available
        if cls.api_token is None:
            raise ValueError("Please set the MLOPS_BIGSUR_TURI_API_KEY environment variable")

        # Initialize the HubPlatform with a real token
        cls.platform = HubPlatform(api_token=cls.api_token)

    def test_project_initialization(self):
        # Test the project method with a real API call
        project = self.platform.getHubInstance().project(self.project_name)
        self.assertIsNotNone(project)
        self.assertEqual(project.id, self.project_name)

    @unittest.skip("Skipping test_experiments_through_delegation.")
    def test_experiments_through_delegation(self):
        # Accessing Hub methods directly through delegation
        project = self.platform.project(self.project_name)  # Forwarded to Hub instance
        experiments = project.experiments.experiments()
        self.assertIsNotNone(experiments)
        self.assertGreaterEqual(len(experiments), 0)

    @unittest.skip("Skipping test_user.")
    def test_user(self):
        # Accessing Hub methods directly through delegation
        user = self.platform.user()
        self.assertIsNotNone(user)
        assert isinstance(user, User)

    @unittest.skip("Skipping test_models.")
    def test_models(self):
        # Accessing Hub methods directly through delegation
        project = self.platform.project(self.project_name)
        modelapi = project.models
        # models = modelapi.registered_models()
        self.assertIsNotNone(modelapi)

    @unittest.skip("Skipping test_namespaces.")
    def test_namespaces(self):
        # Accessing Hub methods directly through delegation
        namespaces = self.platform.namespaces()
        self.assertIsNotNone(namespaces)

    @unittest.skip("Skipping test_get_list_experiments.")
    def test_get_list_experiments(self):
        # Test the project method with a real API call
        experiments = self.platform.list_experiments(self.project_name)
        self.assertIsNotNone(experiments)
        self.assertGreaterEqual(len(experiments), 0)

    # def test_tensorboad_callback(self):
    #     from sklearn.model_selection import train_test_split
    #     from sklearn.datasets import load_wine
    #     from tensorflow.keras.models import Sequential
    #     from tensorflow.keras.layers import Dense
    #     from tensorflow.keras.utils import to_categorical
    #     from infoapps_mlops_sdk.core import PlatformType, initialize
    #
    #     # Create an experiment object
    #     experiment = initialize(platform_type=PlatformType.KERAS)
    #
    #     # Load and prepare the dataset
    #     data = load_wine()
    #     X_train, X_test, y_train, y_test = train_test_split(data.data, to_categorical(data.target), test_size=0.2,
    #                                                         random_state=42)
    #
    #     # Define a simple Keras model
    #     model = Sequential([
    #         Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    #         Dense(32, activation='relu'),
    #         Dense(y_train.shape[1], activation='softmax')
    #     ])
    #
    #     model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    #
    #     # Create an instance of MLOpsCallback with the experiment object
    #     mlops_callback = MLOpsTensorflowCallback(experiment)
    #
    #     # Train the model and log metrics with MLOpsCallback
    #     model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, callbacks=[mlops_callback])
    #
    #     # Test the project method with a real API call
    #     # project = self.platform.project(self.project_name)
    #     # callback = project.keras_callback()
    #     self.assertIsNotNone(mlops_callback)

    def test_keras_callback(self):
        from sklearn.model_selection import train_test_split
        from sklearn.datasets import load_wine
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense
        from tensorflow.keras.utils import to_categorical
        from tensorflow.keras.metrics import AUC
        from tensorflow.keras.metrics import TopKCategoricalAccuracy

        # Create an experiment object
        experiment = init_experiment(experiment_name="my_experiment2", platform_type=PlatformType.KERAS, owner_email="renaldo_williams@apple.com")
        # experiment.setOwnerEmail("renaldo_williams@apple.com")

        # Load and prepare the dataset
        data = load_wine()
        X_train, X_test, y_train, y_test = train_test_split(data.data, to_categorical(data.target), test_size=0.2,
                                                            random_state=42)

        # Define a simple Keras model
        model = Sequential([
            Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
            Dense(32, activation='relu'),
            Dense(y_train.shape[1], activation='softmax')
        ])

        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=[
            'accuracy',  # Standard accuracy
            'precision',  # Precision
            'recall',  # Recall
            AUC(),  # AUC
            TopKCategoricalAccuracy(k=3)  # Top-3 accuracy
        ])

        # Create an instance of MLOpsCallback with the experiment object
        mlops_callback = MLOpsKerasCallback(experiment, epochs=10)

        # Train the model and log metrics with MLOpsCallback
        model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, callbacks=[mlops_callback])

        experiment.done()
        # Test the project method with a real API call
        # project = self.platform.project(self.project_name)
        # callback = project.keras_callback()
        self.assertIsNotNone(mlops_callback)
