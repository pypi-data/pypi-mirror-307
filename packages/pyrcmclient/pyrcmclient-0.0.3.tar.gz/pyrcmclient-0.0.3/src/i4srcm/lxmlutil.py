from logging import getLogger
import json
from lxml import etree
from lxml.etree import _ElementTree as ETree, _Element as Elem, _Comment as Comment

logger = getLogger('rcm.client')

def from_str( data:str ) -> Elem|None:
    try:
        root:Elem = etree.fromstring(data)
        return root
    except Exception as e:
        logger.exception('can not parse')
    return None

def to_str( obj ) ->str:
    try:
        if isinstance(obj,Elem):
            content_bytes:bytes = etree.tostring( obj, pretty_print=True, xml_declaration=True, encoding='UTF-8')
            content_txt:str = content_bytes.decode().strip()
            return content_txt
        elif isinstance(obj,dict|list):
            return json.dumps(obj,ensure_ascii=False,indent=2).strip()
        elif isinstance(obj,str|float|int):
            return str(obj)
        elif isinstance(obj,bool):
            return 'true' if obj else 'false'
        else:
            return str(obj)
    except:
        pass
    return ''

def from_file( xml_file:str ) -> Elem|None:
    try:
        parser = etree.XMLParser() 
        tree = etree.parse(xml_file,parser)
        root:Elem = tree.getroot()
        return root
    except Exception as e:
        logger.exception('can not parse')
    return None

def to_file( elem:Elem, filepath:str ):
    with open(filepath,'wb') as stream:
        stream.write( etree.tostring( elem, xml_declaration=True, pretty_print=True, encoding='UTF-8' ))

def xpath_to_obj( elem:Elem|None, xpath:str|None):
    try:
        if elem is None or xpath is None:
            return None
        result = elem.xpath(xpath)
        if isinstance(result, list):
            return result
        return [result]
    except Exception as e:
        logger.error(f"(getXPATH) XPATH={xpath} {e}")
        return None

def xpath_to_elem( elem:Elem|None, xpath:str|None) ->Elem|None:
    obj:list|None = xpath_to_obj(elem,xpath)
    if obj is not None and len(obj)>0:
        val = obj[0]
        if isinstance(val,Elem):
            return val
    return None

def xpath_to_str( elem:Elem|None, xpath:str|None, *, default:str|None=None):
    obj:list|None = xpath_to_obj(elem,xpath)
    if obj is None or len(obj)==0:
        return default
    val = obj[0]
    if isinstance(val,Elem):
        return val.text
    elif isinstance(val,etree._ElementUnicodeResult) or isinstance(val,int) or isinstance(val,float):
        return str(val)
    elif isinstance(val,bool):
        return 'true' if val else 'false'
    else:
        logger.error( f'invalid ret type {type(val)}')
        return default

def xpath_to_bool( elem:Elem|None, xpath:str|None, *, default:bool|None=None):
    obj:list|None = xpath_to_obj(elem,xpath)
    if obj is None or len(obj)==0:
        return default
    val = obj[0]
    text = ''
    if isinstance(val,Elem):
        text = val.text
    elif isinstance(val,bool):
        return val
    else:
        text = str(val)
    if text == 'true':
        return True
    if text == 'false':
        return False
    return default

def xpath_to_int( elem:Elem|None, xpath:str|None, *, default:int|None=None):
    obj:list|None = xpath_to_obj(elem,xpath)
    if obj is None or len(obj)==0:
        return default
    val = obj[0]
    if isinstance(val,Elem):
        if val.text:
            try:
                return int(float(val.text))
            except:
                pass
        return default
    elif isinstance(val,etree._ElementUnicodeResult) or isinstance(val,str):
        try:
            return int(float(val))
        except:
            pass
        return default
    elif isinstance(val,int) or isinstance(val,float):
        return int(val)
    elif isinstance(val,bool):
        return 1 if val else 0
    else:
        logger.error( f'invalid ret type {type(val)}')
        return default

def xpath_to_float( elem:Elem, xpath:str, *, default:float|None=None):
    obj:list|None = xpath_to_obj(elem,xpath)
    if obj is None or len(obj)==0:
        return default
    val = obj[0]
    if isinstance(val,Elem):
        if val.text:
            try:
                return float(val.text)
            except:
                pass
        return default
    elif isinstance(val,int) or isinstance(val,float):
        return float(val)
    elif isinstance(val,bool):
        return 1.0 if val else 0.0
    else:
        logger.error( f'invalid ret type {type(val)}')
        return default

def get_text(e:Elem) ->str:
    if isinstance(e,Elem):
        return e.text if e.text is not None else ""
    return str(e)

def add_node( parent:Elem, name:str, value:str )->Elem:
    e:Elem = etree.SubElement( parent, name )
    e.text = value
    return e

def set_text( parent:Elem, name:str, value:str|int|float )->Elem:
    """
    子要素のテキスト値を設定します。要素が存在しない場合は新しく作成します。

    Parameters
    ----------
    parent : Elem
        親XML要素。
    name : str
        子要素の名前。
    value : str or int or float
        子要素に設定する値。

    Returns
    -------
    Elem
        更新されたテキスト値を持つ子要素。
    """
    elem:Elem|None = parent.find(name)
    if elem is None:
        elem = etree.SubElement( parent, name )
    elem.text = str(value)
    return elem
