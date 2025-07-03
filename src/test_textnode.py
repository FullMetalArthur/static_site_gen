import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_type(self):
        node3 = TextNode("This is a text node", TextType.NORMAL, "http://www.boot.dev")
        node4 = TextNode("This is a text node", TextType.BOLD, "http://www.boot.dev")
        self.assertNotEqual(node3, node4)

    def test_different_url(self):
        node5 = TextNode("This is a text node", TextType.NORMAL, "http://www.boot.dev")
        node6 = TextNode("This is a text node", TextType.NORMAL, "http://www.boot.dev/playground/py")
        self.assertNotEqual(node5, node6)

    def test_no_url(self):
        node7 = TextNode("This is a text node", TextType.CODE)
        self.assertIsNone(node7.url)

if __name__ == "__main__":
    unittest.main()
