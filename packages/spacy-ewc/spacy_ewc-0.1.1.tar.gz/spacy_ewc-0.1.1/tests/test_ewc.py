import unittest
import spacy
from spacy.training import Example
import logging
import numpy as np
from spacy_ewc.ewc import EWC, VectorDict
from data_examples.original_spacy_labels import original_spacy_labels
from data_examples.training_data import training_data


# Define a logger that matches the module where EWC is used
# Adjust to match the EWC module path
logger = logging.getLogger("spacy_ewc.ewc")


class TestEWC(unittest.TestCase):

    def setUp(self):
        # Initialize the nlp pipeline
        self.nlp = spacy.load("en_core_web_sm")
        # Mock training data for the initial task
        self.train_data = [
            Example.from_dict(self.nlp.make_doc(text), annotations)
            for text, annotations in original_spacy_labels
        ]

        # Train the model
        self.nlp.update(self.train_data)
        # Create an instance of the EWC class
        self.ewc = EWC(self.nlp, self.train_data, lambda_=500)

    def test_initial_fisher_matrix_not_none(self):
        # Ensure that the Fisher matrix is computed after training on initial
        # task
        self.assertIsNotNone(
            self.ewc.fisher_matrix,
            "Fisher matrix should not be None after initialization.",
        )

    def test_theta_star_initialization(self):
        # Verify theta_star is initialized correctly after initial training
        self.assertIsInstance(
            self.ewc.theta_star, dict, "theta_star should be a dictionary."
        )
        self.assertGreater(
            len(self.ewc.theta_star),
            0,
            "theta_star should contain parameters.",
        )

    def test_capture_current_params(self):
        # Test if get_current_params method correctly captures model parameters
        current_params = self.ewc._capture_current_parameters()
        self.assertIsInstance(
            current_params,
            dict,
            "get_current_params should return a dictionary.",
        )
        self.assertGreater(
            len(current_params),
            0,
            "Captured current_params should contain parameters.",
        )

    def test_fisher_matrix_computation(self):
        # Test if the Fisher matrix is correctly computed
        fisher_matrix = self.ewc._compute_fisher_matrix(self.train_data)
        self.assertIsInstance(
            fisher_matrix, dict, "Fisher matrix should be a dictionary."
        )
        self.assertGreater(
            len(fisher_matrix),
            0,
            "Fisher matrix should contain computed values.",
        )

    def test_loss_penalty_calculation(self):
        # Test the loss penalty calculation function
        penalty = self.ewc.compute_ewc_penalty()
        self.assertIsInstance(penalty, float, "loss_penalty should return a float.")
        self.assertGreaterEqual(penalty, 0.0, "loss_penalty should be non-negative.")

    def test_ewc_loss_calculation(self):
        # Test the EWC loss function
        mock_task_loss = 0.5
        ewc_loss = self.ewc.ewc_loss(mock_task_loss)
        self.assertIsInstance(ewc_loss, float, "ewc_loss should return a float.")
        self.assertGreaterEqual(
            ewc_loss,
            mock_task_loss,
            "EWC loss should be at least as large as task loss.",
        )

    def test_gradient_penalty_calculation(self):
        # Test the gradient_penalty method
        ewc_penalty_gradients = self.ewc.compute_gradient_penalty()

        # Ensure it returns a dictionary
        self.assertIsInstance(
            ewc_penalty_gradients,
            dict,
            "gradient_penalty should return a dictionary.",
        )

        # Check if the dictionary has the same keys as theta_star
        self.assertEqual(
            set(ewc_penalty_gradients.keys()),
            set(self.ewc.theta_star.keys()),
            "gradient_penalty should contain the same keys as theta_star.",
        )

        # Verify each gradient is non-negative
        for key, penalty in ewc_penalty_gradients.items():
            self.assertTrue(
                (penalty >= 0).all(),
                "Each penalty gradient should be non-negative.",
            )

    def test_get_current_params_copy_behavior(self):
        # Test with copy=True
        copied_params = self.ewc._capture_current_parameters(copy=True)
        self.assertIsInstance(
            copied_params,
            dict,
            "get_current_params should return a dictionary.",
        )

        # Ensure parameters are copied (i.e., not the same object reference)
        for key, param in copied_params.items():
            self.assertNotEqual(
                id(param),
                id(self.ewc._capture_current_parameters(copy=False)[key]),
                f"Parameter '{key}' should be a different object when copy=True.",
            )

        # Test with copy=False
        referenced_params = self.ewc._capture_current_parameters(copy=False)
        self.assertIsInstance(
            referenced_params,
            dict,
            "get_current_params should return a dictionary.",
        )

        # Ensure parameters are references (i.e., the same object reference)
        for key, param in referenced_params.items():
            self.assertEqual(
                id(param),
                id(self.ewc._capture_current_parameters(copy=False)[key]),
                f"Parameter '{key}' should be the same object when copy=False.",
            )

    def test_apply_ewc_penalty_to_gradients_missing_keys(self):
        # Temporarily remove a key from theta_star to test missing key handling
        missing_key = list(self.ewc.theta_star.keys())[0]
        del self.ewc.theta_star[missing_key]

        with self.assertRaises(ValueError) as context:
            self.ewc.apply_ewc_penalty_to_gradients()

        self.assertIn(
            missing_key,
            str(context.exception),
            "apply_ewc_penalty_to_gradients should raise an error when a required key is missing.",
        )

    def test_apply_ewc_penalty_to_gradients_incompatible_shapes(self):
        # Modify theta_star to have an incompatible shape for testing
        key = list(self.ewc.theta_star.keys())[0]
        original_shape = self.ewc.theta_star[key].shape
        # Change shape to be incompatible
        self.ewc.theta_star[key] = self.ewc.theta_star[key].ravel()

        # Run apply_ewc_penalty_to_gradients and ensure it skips incompatible
        # shapes without error
        with self.assertRaises(Exception) as e:
            self.ewc.apply_ewc_penalty_to_gradients()
            self.assertAlmostEqual(
                e,
                "apply_ewc_penalty_to_gradients raised an exception for incompatible shapes",
            )

        # Restore original shape
        self.ewc.theta_star[key] = self.ewc.theta_star[key].reshape(original_shape)

    def test_apply_ewc_penalty_to_gradients_incompatible_types(self):
        # Change the dtype of a parameter to test incompatible types handling
        key = list(self.ewc.theta_star.keys())[0]
        self.ewc.theta_star[key] = self.ewc.theta_star[key].astype(
            "float32"
        )  # Change dtype

        # Run apply_ewc_penalty_to_gradients and ensure it skips incompatible
        # types without error
        try:
            self.ewc.apply_ewc_penalty_to_gradients()
        except Exception as e:
            self.fail(
                f"apply_ewc_penalty_to_gradients raised an exception for incompatible types: {e}"
            )

    def test_apply_ewc_penalty_to_gradients_valid_parameters(self):
        # Ensure gradients are modified when all parameters are compatible
        initial_gradients = {}
        for layer in self.nlp.get_pipe("ner").model.walk():
            for (_, name), (_, grad) in layer.get_gradients().items():
                key = f"{layer.name}_{name}"
                initial_gradients[key] = grad.copy()

        # Apply EWC gradient calculation
        self.ewc.apply_ewc_penalty_to_gradients()

        gradients_comparisons = []

        # Check that the gradients have been modified
        for layer in self.nlp.get_pipe("ner").model.walk():
            for (_, name), (_, grad) in layer.get_gradients().items():
                key = f"{layer.name}_{name}"
                if (
                    key in initial_gradients
                    and initial_gradients[key].shape == grad.shape
                ):
                    gradients_comparisons.append((initial_gradients[key] == grad).all())

        # Ensure that not all gradients are identical (i.e., at least one was
        # modified)
        self.assertFalse(
            all(gradients_comparisons),
            "At least one gradient should be modified by apply_ewc_penalty_to_gradients.",
        )

    def test_validate_initialization(self):
        # Test _validate_initialization by manually setting fisher_matrix and
        # theta_star to None
        self.ewc.fisher_matrix = None
        self.ewc.theta_star = None

        with self.assertRaises(ValueError) as context:
            self.ewc._validate_initialization()

        # Check if both error messages are present for fisher_matrix and
        # theta_star
        self.assertIn(
            "Fisher Information Matrix has not been computed",
            str(context.exception),
        )
        self.ewc.fisher_matrix = {"layer_name": [0]}

        with self.assertRaises(ValueError) as context:
            self.ewc._validate_initialization()

        self.assertIn("Initial model parameters are not set", str(context.exception))

    def test_fisher_matrix_no_batches_yielded_positive_loss(self):
        # Test that _compute_fisher_matrix raises an error if no batches yield positive loss
        # Using an empty data set to simulate no batches yielding loss
        empty_data = []

        with self.assertRaises(ValueError) as context:
            EWC(self.nlp, empty_data)

        self.assertIn(
            "No batches yielded positive loss; Fisher Information Matrix not computed.",
            str(context.exception),
        )

    def test_apply_ewc_penalty_to_gradients_missing_key_message(self):
        # Temporarily remove a key from fisher_matrix to test missing key
        # handling
        missing_key = list(self.ewc.fisher_matrix.keys())[0]
        del self.ewc.fisher_matrix[missing_key]

        with self.assertRaises(ValueError) as context:
            self.ewc.apply_ewc_penalty_to_gradients()

        self.assertIn(
            f"Invalid key_name found '{missing_key}'",
            str(context.exception),
        )

    def test_apply_ewc_penalty_to_gradients_incompatible_shapes_logging(self):
        # Modify fisher_matrix to have an incompatible shape for testing
        key = list(self.ewc.fisher_matrix.keys())[0]
        original_shape = self.ewc.fisher_matrix[key].shape
        self.ewc.fisher_matrix[key] = self.ewc.fisher_matrix[key].ravel()

        with self.assertLogs(logger, level="INFO") as log:
            self.ewc.apply_ewc_penalty_to_gradients()

        # Check that the log captured the warning about incompatible shapes
        self.assertTrue(any("Shape mismatch" in message for message in log.output))

        # Restore original shape for cleanup
        self.ewc.fisher_matrix[key] = self.ewc.fisher_matrix[key].reshape(
            original_shape
        )

    def test_apply_ewc_penalty_to_gradients_incompatible_dtypes(self):
        # Change the dtype of a parameter to test incompatible dtypes handling
        key = list(self.ewc.fisher_matrix.keys())[-1]
        self.ewc.fisher_matrix[key] = self.ewc.fisher_matrix[key].astype(
            "float32"
        )  # Change dtype

        try:
            self.ewc.apply_ewc_penalty_to_gradients()
        except Exception as e:
            self.fail(
                f"apply_ewc_penalty_to_gradients raised an exception for incompatible dtypes: {e}"
            )

    def test_apply_ewc_penalty_to_gradients_modified_gradients(self):
        # Ensure that gradients are modified correctly in
        # apply_ewc_penalty_to_gradients
        initial_gradients = {}
        for layer in self.nlp.get_pipe("ner").model.walk():
            for (_, name), (_, grad) in layer.get_gradients().items():
                key = f"{layer.name}_{name}"
                initial_gradients[key] = grad.copy()

        # Apply EWC gradient calculation
        self.ewc.apply_ewc_penalty_to_gradients()

        gradients_modified = False

        # Check that the gradients have been modified
        for layer in self.nlp.get_pipe("ner").model.walk():
            for (_, name), (_, grad) in layer.get_gradients().items():
                key = f"{layer.name}_{name}"
                if (
                    key in initial_gradients
                    and initial_gradients[key].shape == grad.shape
                ):
                    if not (initial_gradients[key] == grad).all():
                        gradients_modified = True
                        break

        self.assertTrue(
            gradients_modified,
            "Gradients should be modified by apply_ewc_penalty_to_gradients.",
        )

    def test_lambda_initialization(self):
        # Check if the lambda parameter was initialized correctly
        self.assertEqual(
            self.ewc.lambda_,
            500,
            "Lambda should be initialized to the specified value.",
        )

    def test_set_lambda_updates_lambda_value(self):
        # Test that set_lambda properly updates the lambda_ parameter
        self.ewc.set_lambda(2000)
        self.assertEqual(
            self.ewc.lambda_,
            2000,
            "Lambda should update to the new value provided.",
        )

    def test_apply_ewc_penalty_to_gradients_with_different_lambda_values(self):
        # Ensure that gradients are modified according to lambda_ value
        # Capture initial gradients
        initial_gradients = {}
        for layer in self.nlp.get_pipe("ner").model.walk():
            for (_, name), (_, grad) in layer.get_gradients().items():
                key = f"{layer.name}_{name}"
                initial_gradients[key] = grad.copy()

        # Apply EWC penalty with initial lambda
        self.ewc.apply_ewc_penalty_to_gradients()

        # Check that gradients were modified
        gradients_changed_with_initial_lambda = False
        for layer in self.nlp.get_pipe("ner").model.walk():
            for (_, name), (_, grad) in layer.get_gradients().items():
                key = f"{layer.name}_{name}"
                if key in initial_gradients:
                    if not np.array_equal(initial_gradients[key], grad):
                        gradients_changed_with_initial_lambda = True
                        break
        self.assertTrue(
            gradients_changed_with_initial_lambda,
            "Gradients should change when apply_ewc_penalty_to_gradients is applied.",
        )

        # Set a different lambda and reapply
        self.ewc.set_lambda(1000)
        self.ewc.apply_ewc_penalty_to_gradients()

        # Check that gradients have been modified according to the new lambda
        # value
        gradients_changed_with_new_lambda = False
        for layer in self.nlp.get_pipe("ner").model.walk():
            for (_, name), (_, grad) in layer.get_gradients().items():
                key = f"{layer.name}_{name}"
                if key in initial_gradients:
                    if not np.array_equal(initial_gradients[key], grad):
                        gradients_changed_with_new_lambda = True
                        break
        self.assertTrue(
            gradients_changed_with_new_lambda,
            "Gradients should change according to the new lambda value in apply_ewc_penalty_to_gradients.",
        )

    def test_ewc_loss_calculation_with_different_lambda_values(self):
        # Test EWC loss with different lambda values
        mock_task_loss = 0.5

        # Mock training data for the initial task
        self.train_data = [
            Example.from_dict(self.nlp.make_doc(text), annotations)
            for text, annotations in training_data
        ]

        # Train the model
        self.nlp.update(self.train_data)

        # Calculate EWC loss with initial lambda
        initial_ewc_loss = self.ewc.ewc_loss(mock_task_loss)

        # Set a new lambda and calculate EWC loss again
        self.ewc.set_lambda(2000)
        new_ewc_loss = self.ewc.ewc_loss(mock_task_loss)

        self.assertNotEqual(
            initial_ewc_loss,
            new_ewc_loss,
            "EWC loss should differ when lambda is changed.",
        )

    def test_set_lambda_logs_correctly(self):
        # Check logging output when setting lambda
        with self.assertLogs(logger, level="INFO") as log:
            self.ewc.set_lambda(1500)

        self.assertIn(
            "Updating lambda_",
            log.output[0],
            "The log should contain the lambda update message.",
        )

    def tearDown(self):
        del self.ewc
        del self.nlp


class TestVectorDict(unittest.TestCase):

    def setUp(self):
        """Set up a sample VectorDict instance for testing."""
        self.vector_dict = VectorDict()
        # Populate with example key-value pairs
        self.vector_dict["key1"] = np.array([1.0, 2.0, 3.0])
        self.vector_dict["key2"] = np.array([4.0, 5.0, 6.0])

    def test_str(self):
        self.assertEqual(
            str(self.vector_dict),
            "key1: [1.0, 2.0, 3.0]...\nkey2: [4.0, 5.0, 6.0]...",
        )

        self.assertEqual(str(VectorDict()), "{}")

    def test_repr(self):
        """Test the __repr__ method for correct string representation."""
        # Expected format for the __repr__ output (based on the VectorDict
        # formatting)
        expected_repr = (
            "VectorDict({ key1: [1.0, 2.0, 3.0]..., key2: [4.0, 5.0, 6.0]... })"
        )

        # Call the __repr__ method
        actual_repr = repr(self.vector_dict)

        # Check if the actual repr output matches the expected format
        self.assertEqual(actual_repr, expected_repr)


if __name__ == "__main__":
    unittest.main()
