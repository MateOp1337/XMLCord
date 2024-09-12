# parser.py

import xml.etree.ElementTree as ET

def convert_bool(value):
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    return value

def xml_to_dict(element) -> dict:
    result = {element.tag: {}}

    if element.attrib:
        result[element.tag]['@attributes'] = {
            key: convert_bool(value) for key, value in element.attrib.items()
        }

    if element.text and element.text.strip():
        text = element.text.strip()
        result[element.tag]['#text'] = convert_bool(text)

    children = list(element)
    if children:
        child_dict = {}
        for child in children:
            child_data = xml_to_dict(child)
            for key, value in child_data.items():
                if key in child_dict:
                    if isinstance(child_dict[key], list):
                        child_dict[key].append(value)
                    else:
                        child_dict[key] = [child_dict[key], value]
                else:
                    child_dict[key] = value
        if result[element.tag]:
            result[element.tag].update(child_dict)
        else:
            result[element.tag] = child_dict

    return result

def parse(file) -> dict:
    tree = ET.parse(f'{file}.xml')
    root = tree.getroot()
    data = xml_to_dict(root)
    return data
