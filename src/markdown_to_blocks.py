from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    delimiter = "\n\n"
    blocks = markdown.split(delimiter)
    cleaned_blocks = []

    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            cleaned_blocks.append(stripped_block)
    
    return cleaned_blocks