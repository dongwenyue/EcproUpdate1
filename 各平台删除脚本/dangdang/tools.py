from xml.dom.minidom import Document
from xml.dom.minidom import parseString

# from src.dangdang.exceptions import OpenApiError

XMLERROR = "xml_error"
XMLERRORFORMAT = "xml输入格式错误, 只能有单一最外层"
XMLERRORKEY = "xml输入格式错误, 键值不能为数字"


class DictToXml():
    def __init__(self, data):
        self.Rnode = Document()
        if len(data) > 1:
            raise OpenApiError(error_code=XMLERROR, error_msg=XMLERRORFORMAT)
        self.data = data
        self.cdata_map = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;",
        }

    def transport(self):
        return self._transport(self.Rnode, self.data)

    def _transport(self, this_node, data, Attribute=None):
        for key, value in data.items():
            if isinstance(value, str):
                self.set_node_StrValue(this_node, key, value, Attribute)
            elif isinstance(value, list):
                self.set_node_ListValue(this_node, key, value, Attribute)
            elif isinstance(value, dict):
                self.set_node_DictValue(this_node, key, value, Attribute)
            else:
                raise OpenApiError(error_code=XMLERROR, error_msg="未知格式")

        return self.Rnode.toprettyxml(indent="", newl="")

    def set_node_StrValue(self, this_node, key, value: str, Attribute: dict = None):
        _node = self.Rnode.createElement(key)
        this_node.appendChild(_node)
        if Attribute:
            for AttributeKey, AttributeValue in Attribute.items():
                _node.setAttribute(AttributeKey, AttributeValue)
        else:
            value = self.CDATA(str(value))
            _value = self.Rnode.createTextNode(str(value))
            _node.appendChild(_value)
        return _node

    def CDATA(self, value):
        for x, y in self.cdata_map.items():
            value = value.replace(x, y)
        return value

    def set_node_DictValue(self, this_node, key, value: dict, Attribute: dict = None):
        NextNode = self.Rnode.createElement(key)
        this_node.appendChild(NextNode)
        self._transport(NextNode, value, Attribute)

    def set_node_ListValue(self, this_node, key, value: list, Attribute: dict = None):
        for V in value:
            if isinstance(V, str):
                self.set_node_StrValue(this_node, key, V, Attribute)
            elif isinstance(V, list):
                self.set_node_ListValue(this_node, key, V, Attribute)
            elif isinstance(V, dict):
                self.set_node_DictValue(this_node, key, V, Attribute)
        return this_node


class XmlToDict():
    def __init__(self, xml):
        self.xml = xml
        self.data = {}
        self.dom = parseString(self.xml)

    def transport(self):
        rootNode = self.dom.documentElement  # 获取根节点
        key = rootNode.localName
        return {key: self._transport(rootNode)}

    def _transport(self, Node):
        res = {}
        for cNode in Node.childNodes:
            if not hasattr(cNode,"tagName"): continue
            key = cNode.tagName
            if len(cNode.childNodes) == 1 and cNode.childNodes[0].nodeType in (3,4):
                # 只有唯一节点，且唯一节点为文字节点 真节点 - 文字
                self.setValue(res, key, cNode.childNodes[0].data)
            else:
                KV = self._transport(cNode)
                self.setValue(res, key, KV)
        return res

    def setValue(self, P_data, key, value):
        # 设定值
        if key not in P_data:
            P_data[key] = value
        elif key in P_data and isinstance(P_data[key], list):
            P_data[key].append(value)
        elif key in P_data and (isinstance(P_data[key], dict) or isinstance(P_data[key], str)):
            P_data[key] = [P_data[key]]
            P_data[key].append(value)
        return P_data


if __name__ == "__main__":
    data = {"ItemsList":
                {"ItemAddInfo": {"t1212": "l1",
                                 "VLA": ["l1", "2", {"df1": "ds"}, {"df1": "ds2"}],
                                 "cd": {"te": {"te": "vr", "te2": "cd", "te3": "21", "te4": "rvc"},
                                        "te2": "23",
                                        "te3": "cv",
                                        "te4": "v12"},
                                 "cd2": {"te": "v12"},
                                 "cd3": {"te": "vd"},
                                 "cd4": {"te": "d1"}},
                 "f1": "vf1"}}
    xml = DictToXml(data).transport()
    dic = XmlToDict(xml).transport()
    print(xml)
    print(dic)
    print(dic == data)
