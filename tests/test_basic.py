"""Basic test cases for QuantumScope."""
import unittest
from unittest.mock import patch, MagicMock
from QuantumScope import __version__

class TestQuantumScope(unittest.TestCase):
    """Test cases for QuantumScope package."""

    def test_version(self):
        """Test that version is set correctly."""
        self.assertIsNotNone(__version__)
        self.assertIsInstance(__version__, str)
        # Version should be in format X.Y.Z
        self.assertRegex(__version__, r'^\d+\.\d+\.\d+$')

    @patch('QuantumScope.main.QuantumScopeEngine')
    def test_main_import(self, mock_engine):
        """Test that main can be imported and called."""
        # This is a basic test to ensure the main module can be imported
        from QuantumScope.main import main
        self.assertTrue(callable(main))
