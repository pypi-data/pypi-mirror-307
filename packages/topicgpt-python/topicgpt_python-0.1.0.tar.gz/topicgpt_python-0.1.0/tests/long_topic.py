import unittest
from unittest.mock import MagicMock
import sys
sys.path.append("../topic_gpt")
from generation_1 import prompt_formatting

class TestPromptFormatting(unittest.TestCase):
    def setUp(self):
        self.api_client = MagicMock()
        self.api_client.estimate_token_count.side_effect = lambda x: len(x.split())  
        self.api_client.truncating = lambda doc, max_len: " ".join(doc.split()[:max_len])  
        
        self.generation_prompt = "Document: {Document}\nTopics: {Topics}"
        self.doc = "This is a test document that has a moderate length."
        self.seed_file = "seed_file"
        self.context_len = 100  
        self.verbose = True

    def test_prompt_with_long_topic_list(self):
        # Simulate a long list of topics
        topics_list = [f"Topic {i}: Description of topic {i}" for i in range(100)]  # 100 topics

        # Run prompt formatting with long topic list
        formatted_prompt = prompt_formatting(
            self.generation_prompt,
            self.api_client,
            self.doc,
            self.seed_file,
            topics_list,
            self.context_len,
            self.verbose,
            max_top_len=50  # Set a very short max topic length to force pruning
        )

        truncated_topics = formatted_prompt.split("Topics: ")[1]
        total_len = self.api_client.estimate_token_count(truncated_topics)

        self.assertTrue(total_len <= 50, "The topics were not truncated to fit within the max_top_len.")

if __name__ == '__main__':
    unittest.main()
