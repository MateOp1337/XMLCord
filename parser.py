import xml.etree.ElementTree as ET

def xml_to_dict(element):
    result = {element.tag: {} if element.attrib or element.text else None}
    
    if element.attrib:
        result[element.tag]['@attributes'] = element.attrib
    
    if element.text:
        text = element.text.strip()
        if text.lower() == 'true':
            result[element.tag] = True
        elif text.lower() == 'false':
            result[element.tag] = False
        elif text:
            result[element.tag] = text
    
    children = list(element)
    if children:
        default_dict = {}
        for child in children:
            child_dict = xml_to_dict(child)
            for key, value in child_dict.items():
                if key in default_dict:
                    if isinstance(default_dict[key], list):
                        default_dict[key].append(value)
                    else:
                        default_dict[key] = [default_dict[key], value]
                else:
                    default_dict[key] = value
        result[element.tag] = default_dict
    
    return result

def parse(file):
    tree = ET.parse(f'{file}.xml')
    root = tree.getroot()
    data = xml_to_dict(root)
    return data