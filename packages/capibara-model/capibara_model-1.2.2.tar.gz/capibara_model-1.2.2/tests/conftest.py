# tests/conftest.py

import pytest  # type: ignore
import jax  # type: ignore
import jax.numpy as jnp  # type: ignore
from jax import random
import os
import logging
from typing import Dict, Any, Optional
from pathlib import Path

from capibara_model.core.config import CapibaraConfig  # type: ignore
from capibara_model.model import CapibaraTextGenerator  # type: ignore
from capibara_model.utils.logging import setup_logger  # type: ignore

# Configurar el logger para las pruebas
logger = setup_logger(__name__)


def initialize_tests() -> None:
    """
    Initialize the necessary configuration for running all tests.

    This function sets up:
    - Random seeds for reproducibility
    - Environment variables
    - JAX platform configuration
    - Logging configuration
    - Test data directories

    Raises:
        RuntimeError: If critical initialization steps fail
    """
    try:
        # Set a fixed random seed for reproducibility in tests
        key = jax.random.PRNGKey(42)

        # Configure JAX backend
        if os.environ.get('JAX_PLATFORM_NAME'):
            jax.config.update('jax_platform_name',
                              os.environ['JAX_PLATFORM_NAME'])

        # Set up test environment variables
        os.environ['CAPIBARA_LOG_LEVEL'] = 'ERROR'
        os.environ['CAPIBARA_TEST_MODE'] = 'TRUE'

        # Create test data directory if it doesn't exist
        test_data_dir = Path(__file__).parent / 'test_data'
        test_data_dir.mkdir(exist_ok=True)

        logger.info("Test initialization completed successfully")

    except Exception as e:
        logger.error(f"Failed to initialize tests: {str(e)}")
        raise RuntimeError(f"Test initialization failed: {str(e)}")


@pytest.fixture(scope="session", autouse=True)
def setup_tests() -> None:
    """
    Session-wide test setup fixture.

    This fixture runs once at the beginning of the test session and performs cleanup after all tests.
    """
    initialize_tests()
    yield
    # Cleanup after all tests
    logger.info("Cleaning up after test session")
    # Add cleanup code here if needed


@pytest.fixture(scope="session")
def test_config() -> CapibaraConfig:
    """
    Provides a test configuration for the CapibaraModel model.

    Returns:
        CapibaraConfig: A configuration object with test settings
    """
    try:
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
            batch_size=32,
            learning_rate=0.001,
            dropout_rate=0.1
        )
    except Exception as e:
        logger.error(f"Failed to create test configuration: {str(e)}")
        raise


@pytest.fixture(scope="function")
def capibara_model(test_config: CapibaraConfig) -> CapibaraModel:
    """
    Provides a fresh instance of the CapibaraModel model for each test.

    Args:
        test_config: The test configuration fixture

    Returns:
        CapibaraModel: A new model instance
    """
    try:
        return CapibaraModel(test_config)
    except Exception as e:
        logger.error(f"Failed to create model instance: {str(e)}")
        raise


@pytest.fixture(scope="function")
def rng_key() -> jnp.ndarray:
    """
    Provides a fresh PRNG key for each test.

    Returns:
        jnp.ndarray: A JAX PRNG key
    """
    return jax.random.PRNGKey(0)


@pytest.fixture(scope="function")
def sample_input(rng_key: jnp.ndarray, test_config: CapibaraConfig) -> jnp.ndarray:
    """
    Provides a sample input tensor for testing.

    Args:
        rng_key: The random key fixture
        test_config: The test configuration fixture

    Returns:
        jnp.ndarray: A random input tensor
    """
    try:
        return jax.random.randint(
            rng_key,
            (1, test_config.max_length),
            0,
            test_config.vocab_size
        )
    except Exception as e:
        logger.error(f"Failed to generate sample input: {str(e)}")
        raise


@pytest.fixture(scope="function")
def model_params(
    capibara_model: CapibaraModel,
    sample_input: jnp.ndarray,
    rng_key: jnp.ndarray
) -> Dict[str, Any]:
    """
    Provides initialized model parameters.

    Args:
        capibara_model: The model fixture
        sample_input: The sample input fixture
        rng_key: The random key fixture

    Returns:
        Dict[str, Any]: The initialized model parameters
    """
    try:
        return capibara_model.init(rng_key, sample_input)['params']
    except Exception as e:
        logger.error(f"Failed to initialize model parameters: {str(e)}")
        raise


@pytest.fixture(scope="function")
def attention_mask(test_config: CapibaraConfig) -> jnp.ndarray:
    """
    Provides an attention mask for testing.

    Args:
        test_config: The test configuration fixture

    Returns:
        jnp.ndarray: An attention mask tensor
    """
    return jnp.ones((1, test_config.max_length))


@pytest.fixture(scope="session")
def test_data_dir() -> Path:
    """
    Provides the path to the test data directory.

    Returns:
        Path: Path to the test data directory
    """
    return Path(__file__).parent / 'test_data'


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.

    This hook is called for every plugin and initial conftest file after command line options have been parsed.
    """
    logger.info("Starting test session")


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before returning the exit status to the system.
    """
    logger.info(f"Test session finished with exit status: {exitstatus}")


def pytest_runtest_setup(item):
    """
    Called before running a test item.
    """
    logger.debug(f"Setting up test: {item.name}")


def pytest_runtest_teardown(item, nextitem):
    """
    Called after running a test item.
    """
    logger.debug(f"Tearing down test: {item.name}")
