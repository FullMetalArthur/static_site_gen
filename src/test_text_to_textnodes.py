import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import text_to_textnodes

class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(node)
        
        self.assertEqual(len(new_nodes), 10)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " with an ")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[3].text, "italic")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[4].text, " word and a ")
        self.assertEqual(new_nodes[4].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[5].text, "code block")
        self.assertEqual(new_nodes[5].text_type, TextType.CODE)
        self.assertEqual(new_nodes[6].text, " and an ")
        self.assertEqual(new_nodes[6].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[7].text, "obi wan image")
        self.assertEqual(new_nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(new_nodes[8].text, " and a ")
        self.assertEqual(new_nodes[8].text_type, TextType.NORMAL)        
        self.assertEqual(new_nodes[9].text, "link")
        self.assertEqual(new_nodes[9].text_type, TextType.LINK)
        self.assertEqual(new_nodes[9].url, "https://boot.dev")
        
        for nodes in new_nodes:
            print(nodes)
        print("text_to_textnodes... PASSED!")