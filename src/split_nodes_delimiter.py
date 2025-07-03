from textnode import TextType, TextNode
from extract_markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not old_nodes:
        return []
    if not delimiter:
        raise ValueError("Delimiter can not be empty")
    if not text_type:
        raise ValueError("text_type can not be empty or null")
    
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue

        # For normal text nodes, look for delimiters
        text = old_node.text
        current_position = 0
        remaining_text = text
        
        # While we still have text to process
        while remaining_text:
            # Find the next opening delimiter
            start_index = remaining_text.find(delimiter)
            
            # If no opening delimiter, add remaining text and stop
            if start_index == -1:
                if remaining_text:
                    new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
                break
            
            # Add text before the delimiter
            if start_index > 0:
                new_nodes.append(TextNode(remaining_text[:start_index], TextType.NORMAL))
            
            # Move past the opening delimiter
            remaining_text = remaining_text[start_index + len(delimiter):]
            
            # Find the closing delimiter
            end_index = remaining_text.find(delimiter)
            
            # If no closing delimiter, raise error
            if end_index == -1:
                raise ValueError("Unclosed delimiter found")
            
            # Add the content inside delimiters
            delimited_content = remaining_text[:end_index]
            new_nodes.append(TextNode(delimited_content, text_type))

            # Move past the closing delimiter
            remaining_text = remaining_text[end_index + len(delimiter):]
    
    return new_nodes

# ------- OLD CODE --------
#        parts = old_node.text.split(delimiter)
#        for index, part in enumerate(parts):
#            if index % 2 == 0:
#                new_nodes.append(TextNode(part, TextType.NORMAL))
#            else:
#                new_nodes.append(TextNode(part, text_type))
#    if len(new_nodes) % 2 == 0:
#        raise ValueError("WARNING: input contains unclosed delimiter")


def split_nodes_image(old_nodes):
    if not old_nodes:
        return []
        
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
        
        current_text = old_node.text
        for alt_text, url in images:
            markdown = f"![{alt_text}]({url})"
            parts = current_text.split(markdown, 1)  
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))  
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
    return new_nodes
            

def split_nodes_link(old_nodes):
    if not old_nodes:
        return []
        
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        
        current_text = old_node.text
        for alt_text, url in links:
            markdown = f"[{alt_text}]({url})"
            parts = current_text.split(markdown, 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.NORMAL))
            
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.NORMAL))
    return new_nodes

def text_to_textnodes(text):
    if not text:
        return []

    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

