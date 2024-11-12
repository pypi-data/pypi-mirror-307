# tests/run_all_tests.py

from capibara_model.core.config import CapibaraConfig
from capibara_model.data import MultilingualDataset, CapibaraDataLoader
import unittest
import jax  # type: ignore
import jax.numpy as jnp  # type: ignore
from jax import random  # type: ignore
import os
import sys

# Add the project root directory to the path to be able to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def generate_mock_data(key, num_samples, sequence_length, vocab_size):
    """
    Generate simulated data for tests.

    Args:
        key (jax.random.PRNGKey): A JAX random key used for generating random data.
        num_samples (int): The number of mock data samples to generate.
        sequence_length (int): The length of each mock data sequence.
        vocab_size (int): The size of the vocabulary for generating random text.

    Returns:
        list: A list of dictionaries containing 'text' data for testing.
    """
    keys = random.split(key, num_samples)
    return [{'text': ' '.join([str(random.randint(subkey, (), 0, vocab_size).item()) for _ in range(sequence_length)])}
            for subkey in keys]


def create_test_config():
    """
    Create a test configuration.

    Returns:
        CapibaraConfig: A test configuration object with predefined values.
    """
    return CapibaraConfig(
        d_model=512,
        d_state=256,
        d_conv=128,
        expand=2,
        base_model_name='gpt2',
        translation_model='facebook/m2m100_418M',
        get_active_layers=lambda: ['platonic', 'game_theory', 'ethics'],
        get_layer_config=lambda layer_name: {},
        personality={},
        context_window_size=10,
        max_length=50,
        vocab_size=1000,
        batch_size=32
    )


def load_tests(loader, standard_tests, pattern):
    """
    Load all tests from files in the tests folder.

    Args:
        loader (unittest.TestLoader): The test loader object.
        standard_tests (unittest.TestSuite): The standard test suite.
        pattern (str): The pattern for matching test files.

    Returns:
        unittest.TestSuite: The updated test suite with loaded tests.
    """
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern="test_*.py")
    standard_tests.addTests(package_tests)
    return standard_tests


class JAXTestRunner:
    """
    A test runner class for running JAX-based tests.
    """

    @staticmethod
    def run():
        """
        Run all tests using the JAX test runner.

        This method sets up the test environment, creates mock data, a test dataset, and a dataloader,
        loads all test files, and runs the tests using the unittest test runner.
        """
        # Set up the test environment
        key = random.PRNGKey(42)
        config = create_test_config()
        mock_data = generate_mock_data(
            key, num_samples=100, sequence_length=50, vocab_size=config.vocab_size)

        # Create a test dataset and dataloader
        dataset = CapibaraDataset(mock_data, config)
        dataloader = CapibaraDataLoader(dataset, config)

        # Run the tests
        test_loader = unittest.TestLoader()
        all_tests = load_tests(test_loader, unittest.TestSuite(), "test_*.py")

        for test in all_tests:
            if hasattr(test, 'config'):
                test.config = config
            if hasattr(test, 'mock_data'):
                test.mock_data = mock_data
            if hasattr(test, 'dataloader'):
                test.dataloader = dataloader

        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(all_tests)


if __name__ == "__main__":
    # Configure JAX to use CPU, GPU, or TPU as needed
    # jax.config.update('jax_platform_name', 'cpu')  # Use this for CPU
    # jax.config.update('jax_platform_name', 'gpu')  # Use this for GPU
    # jax.config.update('jax_platform_name', 'tpu')  # Use this for TPU

    JAXTestRunner.run()
