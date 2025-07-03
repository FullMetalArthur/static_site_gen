from markdown_to_blocks import BlockType


def block_to_blocktype(block):
    if len(block) > 6 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    count = 0
    for char in block[0:6]:
        if char == "#":
            count += 1
    if (
        count >= 1
        and count <= 6
        and len(block) > count
        and block[count] == " "
        ):
        return BlockType.HEADING
        
    split_block = block.split("\n")
    is_quote = True
    
    for line in split_block:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    is_unordered_list = True
    for line in split_block:
        if not line.startswith("- "):
            is_unordered_list = False
            break
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    
    line_number = 1
    is_ordered_list = True
    for line in split_block:
        if not line.startswith(f"{line_number}. "):
            is_ordered_list = False
            break
        else:
            line_number += 1
    if is_ordered_list:
        return BlockType.ORDERED_LIST


    return BlockType.PARAGRAPH