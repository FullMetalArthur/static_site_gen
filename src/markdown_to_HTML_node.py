from HTMLnode import ParentNode, text_node_to_html_node
from markdown_to_blocks import markdown_to_blocks, BlockType
from block_to_blocktype import block_to_blocktype
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

# ---- Helper Functions: ----
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    text_nodes = split_nodes_delimiter(text_nodes, "`", "code")
    text_nodes = split_nodes_delimiter(text_nodes, "**", "bold")
    text_nodes = split_nodes_delimiter(text_nodes, "_", "italic")

    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)

    return html_nodes

def count_heading_level(block):
    h_level = 0
    for char in block:
        if char == "#":
            h_level += 1
        else:
            break
    return h_level

def extract_code_content(block):
    lines = block.strip().split("\n")
    
    if len(lines) >= 2:
        content_lines = lines[1:-1]
        return "\n".join(content_lines) + "\n"
    else:
        return ""

def extract_code_content(block):
    lines = block.split("\n")
    content_lines = []
    for line in lines:
        if line.strip() == "```":
            continue
        content_lines.append(line)
        content = "\n".join(content_lines) + "\n"
    return content

# ----------------------------

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [], {})

    for block in blocks:
        block_type = block_to_blocktype(block)

        if block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            children = text_to_children(block)
            paragraph_node = ParentNode("p", children, {})
            parent_node.children.append(paragraph_node)

        elif block_type == BlockType.HEADING:
            block = block.replace("\n", " ")
            level = count_heading_level(block)
            content = block[level:].strip()
            children = text_to_children(content)
            heading_node = ParentNode(f"h{level}", children, {})
            parent_node.children.append(heading_node)

        elif block_type == BlockType.CODE:
            content = extract_code_content(block)
            text_node = TextNode(content, TextType.NORMAL)
            text_html_node = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [text_html_node], {})
            pre_node = ParentNode("pre", [code_node], {})
            parent_node.children.append(pre_node)

        elif block_type == BlockType.QUOTE:
            block = block.replace("\n", " ")
            content = block[1:].strip()
            children = text_to_children(content)
            quote_node = ParentNode("blockquote", children, {})
            parent_node.children.append(quote_node)

        elif block_type == BlockType.UNORDERED_LIST:
            # Split the block into lines
            lines = block.split("\n")
            # Create an empty list to hold the li nodes
            list_items = []
            # Process each line as a list item
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue
                # Remove the "- " or "* " prefix
                # Find the first position after the list marker
                content_start = 0
                for i, char in enumerate(line):
                    if char == '-' or char == '*':
                        content_start = i + 1
                        break
                # Extract the content (skipping the marker and any space after it)
                content = line[content_start:].strip()
                # Process inline markdown in the list item
                item_children = text_to_children(content)
                # Create li node
                li_node = ParentNode("li", item_children, {})
                list_items.append(li_node)
    
            # Create the ul node with all list items as children
            unordered_list_node = ParentNode("ul", list_items, {})
            parent_node.children.append(unordered_list_node)

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            list_items = []
            
            for line in lines:
                if not line.strip():
                    continue
                
                content_start = 0
                found_digit = False
                for i, char in enumerate(line):
                    if not found_digit and char.isdigit():
                        found_digit = True
                    elif found_digit and char == ".":
                        content_start = i + 1
                        break
                content = line[content_start:].strip()
                item_children = text_to_children(content)

                li_node = ParentNode("li", item_children, {})
                list_items.append(li_node)

            ordered_list_node = ParentNode("ol", list_items, {})
            parent_node.children.append(ordered_list_node)

    return parent_node