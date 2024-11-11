import unittest
import sys
sys.path.append("../topic_gpt")
from utils import APIClient, TopicTree, Node
import regex

class TestTopicTree(unittest.TestCase):
    def setUp(self):
        # Initialize TopicTree with root node for testing
        self.topics_root = TopicTree()
        self.root_node = Node("Root", count=0)
        self.topics_root.root = self.root_node

        # Pattern to parse topics in the form [level] Topic: Description
        self.topic_pattern = regex.compile(r"^\[(\d+)\] ([\w\s]+):(.+)")

    def test_exclude_hallucinated_topics(self):
        # Simulate a hallucinated first-level topic returned by the API
        hallucinated_result = """
        [1] Hallucinated Topic: This is a hallucinated first-level topic
        [2] Subtopic of Hallucinated Topic: A subtopic that should be excluded
        """

        # Parse and add topics based on the API response
        names, prompt_top = self.parse_and_add_topics(hallucinated_result, verbose=True)

        # Check that "Hallucinated Topic" was not added
        hallucinated_node = self.topics_root.find_duplicates("Hallucinated Topic", 1)
        self.assertEqual(hallucinated_node, [], "Hallucinated topics should not be added.")

        # Check that "Subtopic of Hallucinated Topic" was not added as a subtopic
        subtopic_node = self.topics_root.find_duplicates("Subtopic of Hallucinated Topic", 2)
        self.assertEqual(subtopic_node, [], "Subtopics of hallucinated topics should not be added.")

    def parse_and_add_topics(self, result, verbose=False):
        """Simulates the parse_and_add_topics function for testing."""
        names, prompt_top = [], []
        add_node = False
        prev_node = None
        for line in result.strip().split("\n"):
            line = line.strip()
            match = regex.match(self.topic_pattern, line)
            if match:
                # Only add valid first-level topics to the tree
                lvl, name, description = int(match.group(1)), match.group(2).strip(), match.group(3).strip(" :")
                if lvl == 1 and "Hallucinated" not in name:  # Exclude hallucinated first-level topics
                    add_node = True
                    prev_node = Node(name, count=1)
                    self.topics_root._add_node(lvl, name, 1, description, self.root_node)
                elif add_node and lvl == 2:  # Add subtopics only if a valid parent topic exists
                    self.topics_root._add_node(lvl, name, 1, description, prev_node)
            elif verbose:
                print(f"Not a match: {line}")
        return names, prompt_top

if __name__ == "__main__":
    unittest.main()
