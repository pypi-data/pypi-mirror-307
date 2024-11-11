import unittest
import sys
sys.path.append("../topic_gpt")
from generation_1 import *
from utils import TopicTree, Node

class TestTopicTree(unittest.TestCase):

    def setUp(self):
        # Initialize a TopicTree with a root node for testing
        self.topics_root = TopicTree()
        self.root_node = Node("Root", count=0)
        self.topics_root.root = self.root_node

    def test_duplicate_topic_addition(self):
        # Add a topic for the first time
        self.topics_root._add_node(1, "Sample Topic", 1, "A test description", self.root_node)
        
        # Verify topic is added with count=1
        sample_topic = self.topics_root.find_duplicates("Sample Topic", 1)
        self.assertIsNotNone(sample_topic, "Topic not added correctly")
        self.assertEqual(sample_topic[0].count, 1, "Initial count should be 1")

        # Add the duplicate topic to increment count
        self.topics_root._add_node(1, "Sample Topic", 1, "A test description", self.root_node)
        
        # Check if count is incremented
        sample_topic = self.topics_root.find_duplicates("Sample Topic", 1)
        self.assertEqual(sample_topic[0].count, 2, "Count should be incremented to 2")

    def test_non_duplicate_topic_addition(self):
        # Add a unique topic
        self.topics_root._add_node(1, "Unique Topic", 1, "Unique description", self.root_node)
        
        # Check that the topic count is 1 and is separate from other topics
        unique_topic = self.topics_root.find_duplicates("Unique Topic", 1)
        self.assertIsNotNone(unique_topic, "Unique topic not added correctly")
        self.assertEqual(unique_topic[0].count, 1, "Count for unique topic should be 1")
        
        # Verify that adding a different topic doesn't affect the count of existing topics
        self.topics_root._add_node(1, "Another Topic", 1, "Another description", self.root_node)
        self.assertEqual(unique_topic[0].count, 1, "Count for unique topic should remain 1")

if __name__ == "__main__":
    unittest.main()
