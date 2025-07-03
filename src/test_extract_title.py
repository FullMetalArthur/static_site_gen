import unittest
from main import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        md = "# This is a Title"
        title = extract_title(md)
        self.assertEqual(title, "This is a Title")
        print("title succesfully extracted")

    def test_empty_title(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_only_hash(self):
        with self.assertRaises(ValueError):
            extract_title("#")

    def test_hash_with_whitespaces(self):
        with self.assertRaises(ValueError):
            extract_title("  #   ")

    def test_double_hash(self):
        with self.assertRaises(ValueError):
            extract_title("##")


if __name__ == "__main__":
    unittest.main()