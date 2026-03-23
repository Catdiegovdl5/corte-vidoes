import unittest
from unittest.mock import patch, MagicMock
import os
import json
import sys

# Ensure root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentinel import gerar_proposta_groq, fetch_leads

class TestSentinel(unittest.TestCase):

    @patch('sentinel.requests.post')
    def test_gerar_proposta_groq_success(self, mock_post):
        # Mocking the Gemini API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [
                {
                    'content': {
                        'parts': [{'text': 'Generated Proposal'}]
                    }
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        with patch('sentinel.GEMINI_API_KEY', 'test_key'):
            result = gerar_proposta_groq("Need video", "freelancer")
        self.assertEqual(result, "Generated Proposal")

    @patch('sentinel.gerar_proposta_groq')
    def test_fetch_leads(self, mock_gen):
        mock_gen.return_value = "Mocked Proposal"

        # Ensure the file doesn't exist before test
        if os.path.exists("leads_ready.json"):
            os.remove("leads_ready.json")

        fetch_leads()

        self.assertTrue(os.path.exists("leads_ready.json"))
        with open("leads_ready.json", "r") as f:
            data = json.load(f)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['proposal'], "Mocked Proposal")

        # Cleanup
        os.remove("leads_ready.json")

if __name__ == "__main__":
    unittest.main()
