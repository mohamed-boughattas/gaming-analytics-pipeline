"""Test configuration and fixtures for gaming analytics pipeline."""

from _pytest.config import Config


def pytest_configure(config: Config) -> None:
    """Configure pytest."""
    config.addinivalue_line("markers", "integration: mark test as integration test")
