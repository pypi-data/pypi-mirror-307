import unittest
import sys
sys.path.append("../topicGPT")
from unittest.mock import MagicMock
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from utils import APIClient, TopicTree
from assignment import assign_topics, assignment, assignment_batch

class TestTopicTruncation(unittest.TestCase):
    def setUp(self):
        # Initialize a mock API client
        self.api_client = MagicMock()
        self.api_client.estimate_token_count = MagicMock(side_effect=lambda x: len(x.split()))
        self.api_client.truncate_text = MagicMock(side_effect=lambda text, max_len: " ".join(text.split()[:max_len]))
        self.api_client.iterative_prompt = MagicMock(return_value="Mocked response")
        self.api_client.batch_prompt = MagicMock(return_value=["Mocked batch response"])

        # Set up a long list of topics
        self.topics_root = TopicTree()
        long_topics = ["Topic {}".format(i) for i in range(1000)]
        self.topics_root.from_topic_list = MagicMock(return_value=self.topics_root)
        self.topics_root.to_topic_list = MagicMock(return_value=long_topics)

        # Define a document to test
        self.docs = ["This is a test document to check topic truncation handling."]
        self.assignment_prompt = "Assign the most relevant topics from the list to the document."

        # Set parameters
        self.context_len = 500  # Set a small context length to force truncation
        self.temperature = 0.7
        self.top_p = 0.9
        self.max_tokens = 100
        self.verbose = True

    def test_long_topic_truncation(self):
        # Run assignment function and assert that truncation occurs
        responses, prompted_docs = assignment(
            self.api_client,
            self.topics_root,
            self.docs,
            self.assignment_prompt,
            self.context_len,
            self.temperature,
            self.top_p,
            self.max_tokens,
            self.verbose,
        )

        # Check if topics were truncated correctly based on the context length
        truncated_topics = "\n".join(self.topics_root.to_topic_list())
        truncated_count = self.api_client.estimate_token_count(truncated_topics)
        print(f"Truncated token count: {truncated_count}")
        self.assertLessEqual(truncated_count, self.context_len)

        # Ensure that truncation method was called on the document if it was too long
        self.api_client.truncate_text.assert_called()

        print("Test passed: Topics were truncated to fit within the context length.")


    def test_assignment_batch(self):
        # Run assignment_batch function and assert correct handling
        responses, prompted_docs = assignment_batch(
            self.api_client,
            self.topics_root,
            self.docs,
            self.assignment_prompt,
            self.context_len,
            self.temperature,
            self.top_p,
            self.max_tokens,
            self.verbose,
        )

        # Ensure batch prompt was used
        self.api_client.batch_prompt.assert_called()
        
        # Check that responses are returned for each document
        self.assertEqual(len(responses), len(self.docs))
        print("Test passed: Batch assignment handled correctly.")

if __name__ == "__main__":
    unittest.main()
