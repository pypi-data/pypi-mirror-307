# ikml-doc

## IKML Document Parser

### Description
A parser for IKML (Indic Knowledge Markup Language)

### Installation
To install the IKML parser, use the following command:

```bash
pip install ikml_doc
```

### Usage
The IKML parser can be used to load IKML data from a URL or a local file, and then convert it into various formats such as JSON, XML, and plain text.

#### Loading IKML Data
You can load IKML data from a URL or a local file using the `IKML_Document` class.

```python
from ikml_doc import IKML_Document
```

```python
ikml_url = "https://siddhantakosha.org/libraries/smap-granthas/Naadi-Pariksha/vakyas-ikml.txt"
```

```python
doc = IKML_Document()
doc.load(url=ikml_url)
# IKML text data can be loaded directly using `doc.load(data=ikml_data)`

# url can be directly passed to IKML_Document as well.
_doc = IKML_Document(url=ikml_url)
_doc.tags()
```

## Print top-level tags


```python
tags = doc.tags()
tags[:10]
```

## Print child tags of a given id


```python
print(tags[0]["id"])
doc.child_tags(tags[0]["id"])
```

## Print a given node using id


```python
# Formats could either be "dict", "xml", "txt", "node"
# Default format is "node"
# doc.get(tags[10]["id"], fmt="node")
doc.get(tags[10]["id"], fmt="dict")
```

## Navigate a tag further


```python
tag_node = doc.get(tags[10]["id"])
tag_node.keys()
```

## Iterate over the entire tree


```python
for node in doc.iter():
    print(node)
```

## Iterate over children of tag


```python
for child in tag_node.node_children:
    print(child)
```

## Find Children with having tag_name


```python
list(doc.find_children(tag_name="va"))[:5]
```

## Convert text from `doc.get` to a new IKML Document


```python
node = doc.get(tags[10]["id"])
# print(node.to_txt())
new_doc = IKML_Document(data=node.to_txt())
new_doc.to_dict()
```

## Convert to other types (Dict, XML, Text)


```python
doc.to_dict()
```


```python
doc.to_xml()
```


```python
doc.to_txt()
```

## Save as IKML


```python
filename = "out_ikml.txt"
doc.save(filename)
```

## Save as XML


```python
xmlout = doc.to_xml()
with open("out_xml.txt", "w", encoding="utf-8") as fd:
    fd.write(xmlout)
```

## Load `all-ikml` with `.rel_id` attribute at root level


```python
from ikml_doc import IKML_Document
```


```python
all_ikml_url = "https://siddhantakosha.org/libraries/smap-granthas/Tarkasangraha-Moola/all-ikml.txt"
```


```python
doc2 = IKML_Document(url=all_ikml_url)
```


```python
new_dict = doc2.to_dict()
new_dict
```

## Reload exported dict back into IKML_Document


```python
doc3 = IKML_Document()
doc3.load(data=new_dict)
doc3.to_dict()
```

## Load Sambandhas


```python
from ikml_doc import IKML_Document
```


```python
smb_url = "https://siddhantakosha.org/libraries/smap-granthas/Tarkasangraha-Moola/sambandhas-ikml.txt"
```


```python
doc4 = IKML_Document()
doc4.load(url=smb_url)
```


```python
doc4.get('smaps.TarkaSM.r.1')
```


```python
n = doc4.get('smaps.TarkaSM.r.1', fmt='node')
print(n.keys())
n['.srcid']
```


### Contributing
Contributions are welcome. Please open an issue to discuss any changes before submitting a pull request.

### License
This project is licensed under the LGPL License.

### Acknowledgments
Special thanks to the contributors and maintainers of the IKML project.
