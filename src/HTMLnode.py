from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        paired = []
        for key, value in self.props.items():
            paired.append(f' {key}="{value}"')
        result = "".join(paired)
        return result
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        #list of void tags that do not require self.value
        void_tags = {"img", "br", "hr", "input", "meta", "link"}
        if self.tag in void_tags:
            prop_str = self.props_to_html()
            return f"<{self.tag}{prop_str}>"
        elif not self.value:
            raise ValueError("LeafNode missing value")
        elif not self.tag:
            return self.value
        else:
            prop_str = self.props_to_html()
            return f"<{self.tag}{prop_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("value input is required")
        elif not self.children:
            print(f"Error: Node type {self.tag} has None children")
            raise ValueError("children input is required")
        elif len(self.children) == 0:
            print(f"Warning: Node type {self.tag} has empty children list")
        else:
            result = ""
            for child in self.children:
                result += child.to_html()
            return f"<{self.tag}>{result}</{self.tag}>"
        

def text_node_to_html_node(text_node):
    match text_node.text_type:

        case TextType.NORMAL:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            tag = "b"
            return LeafNode(tag, text_node.text, None)
        case TextType.ITALIC:
            tag = "i"
            return LeafNode(tag, text_node.text, None)
        case TextType.CODE:
            tag = "code"
            return LeafNode(tag, text_node.text, None)
        case TextType.LINK:
            tag = "a"
            props = {"href": text_node.url}
            return LeafNode(tag, text_node.text, props)
        case TextType.IMAGE:
            tag = "img"
            props = {"src": text_node.url, "alt": text_node.text}
            return LeafNode(tag, "", props)
        case _:
            raise Exception("Invalid text type")
        