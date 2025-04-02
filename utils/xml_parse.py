from xml.etree import ElementTree as ET
tree = ET.parse(r"D:\Code\auto-deployment\data\resource\interfaceCode.xml")
root = tree.getroot()
print(root)
print(tree.findall('@bankName'))

#
# from xml.dom.minidom import parse
# import xml.dom.minidom
#
# # 使用minidom解析器打开 XML 文档
# DOMTree = xml.dom.minidom.parse(r"D:\Code\auto-deployment\data\resource\interfaceCode.xml")
# collection = DOMTree.documentElement
# if collection.hasAttribute("bankInfo"):
#     print("Root element : %s" % collection.getAttribute("bankInfo"))
#
# # 在集合中获取所有电影
# movies = collection.getElementsByTagName("rd")
#
# # 打印每部电影的详细信息
# for movie in movies:
#     print("*****Movie*****")
#
#     if movie.hasAttribute("title"):
#         print("Title: %s" % movie.getAttribute("title"))
#
#     type = movie.getElementsByTagName('type')[0]
#     print("Type: %s" % type.childNodes[0].data)
#
#     format = movie.getElementsByTagName('format')[0]
#     print("Format: %s" % format.childNodes[0].data)
#
#     rating = movie.getElementsByTagName('rating')[0]
#     print("Rating: %s" % rating.childNodes[0].data)
#
#     description = movie.getElementsByTagName('description')[0]
#     print("Description: %s" % description.childNodes[0].data)
