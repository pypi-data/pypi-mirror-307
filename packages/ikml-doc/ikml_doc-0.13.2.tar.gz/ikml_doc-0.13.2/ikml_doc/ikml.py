# Written by: Chaitanya S Lakkundi (chaitanya.lakkundi@gmail.com)

import re
import requests
import copy
import json
from .utils import Node, ikml_to_anytree, dict_to_anytree, PreOrderIter, LevelOrderIter


class IKML_Document:
    INDENT = 2

    def __init__(self, url=None, data=None):
        # does dummy root exist or not
        self.exclude_root = False
        # auto load
        self.load(url=url, data=data)

    def mount(self, root):
        # mount root node
        self.root = root

    def load(self, url=None, data=None):
        if url is not None:
            self.url = url
            self.raw_data = str(requests.get(self.url).content, encoding="utf-8")
            self.root = ikml_to_anytree(self.raw_data)
            self.exclude_root = True

        if data is not None:
            # data is either a dict or a list of dicts
            if isinstance(data, dict) or isinstance(data, list):
                self.raw_data = data
                self.root = dict_to_anytree(self.raw_data)
            else:
                self.raw_data = data
                self.root = ikml_to_anytree(self.raw_data)
            self.exclude_root = True

    def save(self, filename="out_ikml.txt"):
        with open(filename, "w", encoding="utf-8") as fd:
            fd.write(self.to_txt())

    def to_dict(self, max_depth=-1):
        # dot-attributes are automatically added for its parent node
        return self.root.to_dict(max_depth=max_depth)

    def to_json(self, max_depth=-1):
        d = self.to_dict(max_depth=max_depth)
        return json.dumps(d, ensure_ascii=False, indent=self.INDENT)

    # TODO: implement exclude_root in to_xml and tree_as_xml_list
    def to_xml(self):
        r2 = copy.deepcopy(self.root)
        # put_attrs_inside is only required for to_xml method.
        # to_dict and to_json check for attributes appropriately by default
        r2.put_attrs_inside()
        return r2.to_xml(quoted_attr=True)

    def to_txt(self, quoted_attr=False, max_depth=-1):
        # returns IKML text
        return self.root.to_txt(quoted_attr=quoted_attr, max_depth=max_depth)

    def tags(self, fmt="node"):
        out = []
        for n in self.root.node_children:
            # out.append(str(n))
            match fmt:
                case "node":
                    out.append(n)
                case "dict":
                    out.append(n.to_dict(max_depth=0))
        return out

    # Return child tags of a given tag_id
    def child_tags(self, tag_id, fmt="node"):
        for node in self.iter():
            try:
                if node["id"] == tag_id:
                    # return [str(n) for n in node.node_children]
                    match fmt:
                        case "node":
                            return [n for n in node.node_children]
                        case "dict":
                            return [n.to_dict(max_depth=0) for n in node.node_children]
            except:
                pass
        return f"Node with id {tag_id} not found."

    # TODO: implement expand_inline
    def find_children(
        self, tag_name, expand_inline=False, max_depth=-1, fmt="node", apply=None
    ):
        if max_depth <= -1:
            max_depth = 9999
        for node in self.iter():
            try:
                if node.tag_name == tag_name and node.depth <= max_depth:
                    match fmt:
                        case "node":
                            if apply is not None:
                                yield apply(node)
                            else:
                                yield node
                        case "dict":
                            if apply is not None:
                                yield apply(node.to_dict(max_depth=max_depth))
                            else:
                                yield node.to_dict(max_depth=max_depth)
            except:
                pass
        return f"Nodes with tag_name {tag_name} not found."

    def get(self, tag_id, fmt="node"):
        for node in PreOrderIter(self.root):
            try:
                if node["id"] == tag_id:
                    match fmt:
                        case "dict":
                            return node.to_dict()
                        case "xml":
                            return node.to_xml()
                        case "txt":
                            return node.to_txt()
                        case "node":
                            return node
            except:
                pass
        return f"Node with id {tag_id} not found."

    def find_children_regex(
        self,
        tagid_pattern=None,
        tag_names=set(),
        max_depth=0,
        fmt="node",
        apply=None,
        no_attributes=True,
    ):
        base_depth = None
        # max_depth = 1 yields sibling nodes
        if max_depth == -1:
            max_depth = 9999
        # do not replace dot with \. for re match. let the input pass correct regex
        # tagid_pattern = tagid_pattern.replace(".", "\\.")
        for node in LevelOrderIter(self.root):
            node_id = node.get("id", "")
            if (
                tagid_pattern is None or re.match(rf"{tagid_pattern}", node_id)
            ) and not (no_attributes and node.is_attribute):
                if node.tag_name in tag_names or not tag_names:
                    if base_depth is None:
                        base_depth = node.depth
                        max_depth += base_depth

                    if node.depth > max_depth:
                        break

                    match fmt:
                        case "node":
                            if apply is not None:
                                yield apply(node)
                            else:
                                yield node
                        case "dict":
                            if apply is not None:
                                yield apply(node.to_dict(max_depth=max_depth))
                            else:
                                yield node.to_dict(max_depth=max_depth)
                        case "txt":
                            if apply is not None:
                                yield apply(node.to_txt(max_depth=max_depth))
                            else:
                                yield node.to_txt(max_depth=max_depth)

    def iter(self):
        for node in PreOrderIter(self.root):
            yield node

    @staticmethod
    def create_node(data, *args, **kwargs):
        data = data.strip()
        if data[0] != "[":
            data = f"[{data}]"
        return Node(data, *args, **kwargs)

    def validate_schema(self, schema_doc):
        valid = True
        valid_schema = set()
        try:
            root = list(schema_doc.find_children("ikml_schema"))[0]
            root.tag_name = "root"
        except:
            pass

        for node in schema_doc.iter():
            if not node.parent:
                ptag = "root"
            else:
                ptag = node.parent.tag_name
            valid_schema.add((ptag, node.tag_name))

        for node in self.iter():
            if not node.parent:
                ptag = "root"
            else:
                ptag = node.parent.tag_name
            if (ptag, node.tag_name) not in valid_schema:
                print("Alert: Invalid tag ", node)
                valid = False
        print(valid_schema)
        return valid