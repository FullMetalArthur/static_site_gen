import unittest
from textnode import TextNode, TextType
from HTMLnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from markdown_to_blocks import markdown_to_blocks

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_empy(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        # Test with a single prop
        node2 = HTMLNode(props={"href": "https://example.com"})
        self.assertEqual(node2.props_to_html(), ' href="https://example.com"')

    def test_props_to_html_multiple_props(self):
        # Test with multiple props
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        # Note: The order of props might vary, so we check if both are in the result
        result = node.props_to_html()
        self.assertIn(' href="https://example.com"', result)
        self.assertIn(' target="_blank"', result)
        # Make sure the total length is correct (accounting for both props)
        self.assertEqual(len(result), len(' href="https://example.com" target="_blank"'))

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href="https://www.google.com">Click me!</a>')

    def test_value_only(self):
        node = LeafNode(None, "Click me!")
        self.assertEqual(node.to_html(), "Click me!")

    def test_leaf_no_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_multiple_prop_no_tag(self):
        node = LeafNode(None, "This is some text", {"length": "1080px", "width": "720px"})
        self.assertEqual(node.to_html(), "This is some text")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_TextNodeToToHtmlNode(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, None)
    
    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.props, None)
    
    def test_code(self):
        node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")
        self.assertEqual(html_node.props, None)
    
    def test_link(self):
        node = TextNode("Link text", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props, {"href": "https://example.com"})



if __name__ == "__main__":
    unittest.main()