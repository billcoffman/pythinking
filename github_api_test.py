import unittest
from unittest.mock import patch
from github_connector import GitHubConnector

class TestGitHubConnector(unittest.TestCase):
    
    def setUp(self):
        self.connector = GitHubConnector(ip='example.com', owner='test_owner', token='test_token')
    
    def test_load_unassigned_all_assigned(self):
        self.assertIsNone(self.connector.load_unassigned())
        self.assertEqual(self.connector.ipaddr, 'example.com')
        self.assertEqual(self.connector.owner, 'test_owner')
        self.assertEqual(self.connector.token, 'test_token')
        self.assertIsNone(self.connector.api_url)
    
    @patch('os.environ', {'GITHUB_IP': 'example.com', 'GITHUB_OWNER': 'test_owner', 'GITHUB_TOKEN': 'test_token'})
    def test_load_unassigned_env_vars(self):
        self.assertIsNone(self.connector.load_unassigned())
        self.assertEqual(self.connector.ipaddr, 'example.com')
        self.assertEqual(self.connector.owner, 'test_owner')
        self.assertEqual(self.connector.token, 'test_token')
        self.assertIsNone(self.connector.api_url)
    
    @patch('builtins.open', create=True)
    def test_load_unassigned_json_file(self, mock_open):
        mock_file = mock_open(read_data='{"ip": "example.com", "owner": "test_owner", "token": "test_token"}')
        with patch('os.path.isfile', return_value=True):
            self.assertIsNone(self.connector.load_unassigned('/path/to/config.json'))
            mock_open.assert_called_once_with('/path/to/config.json')
            self.assertEqual(self.connector.ipaddr, 'example.com')
            self.assertEqual(self.connector.owner, 'test_owner')
            self.assertEqual(self.connector.token, 'test_token')
            self.assertIsNone(self.connector.api_url)
    
    @patch('builtins.open', create=True)
    def test_load_unassigned_json_file_missing_value(self, mock_open):
        mock_file = mock_open(read_data='{"ip": "example.com", "owner": "test_owner"}')
        with patch('os.path.isfile', return_value=True):
            with self.assertRaises(ValueError):
                self.connector.load_unassigned('/path/to/config.json')
    
    def test_repo_url(self):
        self.assertEqual(self.connector.repo_url('test_repo'), 'https://example.com/test_owner/test_repo')
