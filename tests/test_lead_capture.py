import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sentinel

class TestLeadCapture(unittest.TestCase):

    @patch('sentinel.requests.post')
    def test_gerar_proposta_gemini_success(self, mock_post):
        # Mocking Gemini Response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'candidates': [
                {
                    'content': {
                        'parts': [{'text': "I will build a Dockerized Python script using CAPI and GEO. Diego"}]
                    }
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        with patch('sentinel.GEMINI_API_KEY', 'test_key'):
            proposal = sentinel.gerar_proposta_groq("Scraping Project", "freelancer")

        self.assertIn("Dockerized Python", proposal)
        self.assertIn("Diego", proposal)
        self.assertEqual(mock_post.call_count, 1)

    @patch('sentinel.save_memory')
    @patch('sentinel.gerar_proposta_groq')
    def test_fetch_leads_flow(self, mock_gen, mock_save):
        mock_gen.return_value = "Mocked Proposal"

        sentinel.fetch_leads()

        self.assertEqual(mock_gen.call_count, 2)
        self.assertTrue(mock_save.called)

        # Verify data structure passed to save_memory
        args, _ = mock_save.call_args
        leads_list = args[0]
        self.assertEqual(len(leads_list), 2)
        self.assertEqual(leads_list[0]['platform'], 'freelancer')
        self.assertEqual(leads_list[0]['proposal'], 'Mocked Proposal')

if __name__ == "__main__":
    unittest.main()
