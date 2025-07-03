import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from extract_markdown import extract_markdown_images, extract_markdown_links

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_snd_simple_bold(self):
        node = TextNode("This is some **bold text**", TextType.NORMAL)
        old_nodes = [node]
        delimiter = "**"
        text_type = TextType.BOLD

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is some ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

        print("Simple bold test... PASSED")

    def test_snd_multiple_delimiters(self):
        node = TextNode("This is _italic_ and then some more _italic_ text", TextType.NORMAL)
        old_nodes = [node]
        delimiter = "_"
        text_type = TextType.ITALIC

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " and then some more ")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[3].text, "italic")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[4].text, " text")
        self.assertEqual(new_nodes[4].text_type, TextType.NORMAL)

        print("Multiple delimiter test... PASSED")

    def test_snd_no_delimiter(self):
        node = TextNode("There is nothing to see here, move along", TextType.NORMAL)
        old_nodes = [node]
        delimiter = "**"
        text_type = ""

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "There is nothing to see here, move along")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)

        print("No delimiter test... PASSED")

    def test_unclosed_delimiter(self):
        node = TextNode("This is some **bold text", TextType.NORMAL)
        old_nodes = [node]
        delimiter = "**"
        text_type = TextType.BOLD

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)

        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is some ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        
        print("Unclosed delimiter test... PASSED?")

    def test_empty_text(self):
        node = TextNode("", TextType.NORMAL)
        old_nodes = [node]
        delimiter = "**"
        text_type = TextType.BOLD

        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)

        print("Empty text test... PASSED")

    def test_mixed_delimiters(self):
        node = TextNode("Here is a mix **bold and _italic_** text", TextType.NORMAL)
        old_nodes = [node]

        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Here is a mix ")
        self.assertEqual(new_nodes[1].text, "bold and _italic_")  # `_italic_` remains untouched
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

        print("Mixed delimiters, italic ignored... PASSED")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.NORMAL),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ],
        new_nodes,
        )
        print("split nodes images... PASSED!")

    def test_split_images_between_text(self):
        node = TextNode(
            "This is a node with just an ![image](https://i.imgur.com/zfghru.jpeg) between text",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is a node with just an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zfghru.jpeg"),
            TextNode(" between text", TextType.NORMAL),
        ],
        new_nodes,
        )
        print("split nodes images in between text... PASSED!")

    def test_split_node_no_image(self):
        node = TextNode(
            "This is a node with just text",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a node with just text", TextType.NORMAL),
            ],
            new_nodes,
        )
        print("split nodes images without image... PASSED!")

    def test_split_nodes_image_no_text(self):
        node = TextNode("![image](https://i.imgur.com/img.png)![second image](https://i.imgur.com/2ndimg.png)", TextType.NORMAL)
        new_node = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/img.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/2ndimg.png")
            ],
            new_node,
        )
        print("split node image with no text... PASSED!")

    def test_split_node_empty_text(self):
        node = TextNode("![](https://i.imgur.com/no_name.png)", TextType.NORMAL)
        new_node = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("", TextType.IMAGE, "https://i.imgur.com/no_name.png")
            ],
            new_node
        )
        print("split node image with empty alt_text value... PASSED!")

    def test_split_node_image_non_normal_text_type(self):
        node = TextNode("This text is bold ![image](https://i.imgur.com/cat_pics.png)", TextType.BOLD)
        new_node = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This text is bold ", TextType.BOLD),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/cat_pics.png"),
            ],
            new_node,
        )
        print("split node image with bold text... PASSED!")