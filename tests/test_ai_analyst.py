import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai_analyst import AIAnalyst

class TestAIAnalyst(unittest.TestCase):

    @patch('src.ai_analyst.requests.post')
    def test_identify_viral_moments_success(self, mock_post):
        # Mocking Gemini Response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [
                {
                    'content': {
                        'parts': [{'text': '[{"start": 10, "end": 20, "reason": "Test viral"}]'}]
                    }
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        analyst = AIAnalyst(api_key="test_key")
        moments = analyst.identify_viral_moments([{"start": 0, "end": 60, "text": "test"}])

        self.assertEqual(len(moments), 1)
        self.assertEqual(moments[0]['start'], 10)
        self.assertEqual(moments[0]['reason'], "Test viral")

if __name__ == "__main__":
    unittest.main()
