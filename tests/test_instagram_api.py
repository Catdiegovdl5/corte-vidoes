import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.instagram_uploader import InstagramUploader

class TestInstagramUploader(unittest.TestCase):

    def setUp(self):
        self.uploader = InstagramUploader(access_token="fake_token", ig_user_id="fake_user_id")

    @patch('src.instagram_uploader.requests.post')
    @patch('src.instagram_uploader.requests.get')
    def test_upload_reels_success(self, mock_get, mock_post):
        # Mocking Fase 1: Container Creation
        mock_response_post1 = MagicMock()
        mock_response_post1.json.return_value = {'id': 'container_123'}

        mock_response_post2 = MagicMock()
        mock_response_post2.json.return_value = {'id': 'media_123'}

        mock_post.side_effect = [mock_response_post1, mock_response_post2]

        # Mocking Fase 2: Status Check
        mock_response_get = MagicMock()
        mock_response_get.json.return_value = {'status_code': 'FINISHED'}
        mock_get.return_value = mock_response_get

        result = self.uploader.upload_reels("http://video.mp4", "Legenda de Teste")

        self.assertEqual(result, 'media_123')
        self.assertEqual(mock_post.call_count, 2)
        mock_get.assert_called()

    @patch('src.instagram_uploader.requests.post')
    def test_create_container_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'error': 'Some Error'}
        mock_post.return_value = mock_response

        container_id = self.uploader._create_container("http://video.mp4", "Caption")

        self.assertIsNone(container_id)

    @patch('src.instagram_uploader.requests.get')
    def test_wait_for_processing_retry(self, mock_get):
        # Simula 2 tentativas processando e 1 finalizada
        res1 = MagicMock()
        res1.json.return_value = {'status_code': 'IN_PROGRESS'}
        res2 = MagicMock()
        res2.json.return_value = {'status_code': 'IN_PROGRESS'}
        res3 = MagicMock()
        res3.json.return_value = {'status_code': 'FINISHED'}

        mock_get.side_effect = [res1, res2, res3]

        with patch('time.sleep', return_value=None):
            result = self.uploader._wait_for_processing("container_123")

        self.assertTrue(result)
        self.assertEqual(mock_get.call_count, 3)

if __name__ == "__main__":
    unittest.main()
