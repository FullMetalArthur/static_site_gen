import unittest
from markdown_to_blocks import markdown_to_blocks, BlockType
from block_to_blocktype import block_to_blocktype

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
        print("test: markdown_to_block... PASSED")

    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
        print("test: empty markdowns... PASSED")

    def test_excessive_newlines(self):
        md = "Block 1\n\n\n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2"])
        print("test: excessive_newlines... PASSED")

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_blocktype_code(self):
        block = "``` this is a \n" \
        "code block\n" \
        "with multiple lines\n" \
        "```"
        blocktype = block_to_blocktype(block)
        self.assertEqual(blocktype, BlockType.CODE)
        print("block to blocktype:CODE... ¨PASSED!")

    def test_block_to_blocktype_code_empty(self):
        block = "``` ```"
        blocktype = block_to_blocktype(block)
        self.assertEqual(blocktype, BlockType.CODE)
        print("block to empty blocktype:CODE... ¨PASSED!")

    def test_block_to_blocktype_heading_lv1(self):
        block = "# This is a level one heading"
        blocktype = block_to_blocktype(block)
        self.assertEqual(blocktype, BlockType.HEADING)
        print("block to blocktype heading... PASSED")

    def test_block_to_blocktype_heading_lv6(self):
        block = "###### This is a level six heading"
        blocktype = block_to_blocktype(block)
        self.assertEqual(blocktype, BlockType.HEADING)
        print("block to blocktype heading level 6... PASSED")

    def test_block_to_blocktype_quote(self):
        block = (
            ">quote one\n"
            ">quote two\n"
            ">quote three"
            )
        blocktype = block_to_blocktype(block)
        self.assertEqual(blocktype, BlockType.QUOTE)
        print("test block to blocktype quote... PASSED")

    def test_to_blocktype_missed_quote(self):
        block = (
            ">quote one\n"
            ">quote two\n"
            "<wrong quote"
        )
        blocktype = block_to_blocktype(block)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)
        print("test block to blocktype, false quote... PASSED")

    def test_block_to_blocktype_unordered(self):
        block = (
            "- item one\n"
            "- item two\n"
            "- item three"
        )
        blocktype = block_to_blocktype(block)
        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)
        print("test block to blocktype unordered list... PASSED")

    def test_block_to_blocktype_ordered(self):
        block = (
            "1. one\n"
            "2. two\n"
            "3. three"
        )
        blocktype = block_to_blocktype(block)
        self.assertEqual(blocktype, BlockType.ORDERED_LIST)
        print("test block to blocktype ordered list... PASSED")

    def test_block_to_blocktype_false_ordered(self):
        block = (
            "1. one\n"
            "2. two\n"
            "2. three"
        )
        blocktype = block_to_blocktype(block)
        self.assertEqual(blocktype, BlockType.PARAGRAPH)
        print("test block to blocktype false ordered list... PASSED")

if __name__ == "__main__":
    unittest.main()