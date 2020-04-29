import xml.etree.ElementTree as et

tree = et.parse("C:/Users/YHawon/PycharmProjects/PyQt5_Prac/config_data.xml")

cctv = tree.find('./cctv')

print(cctv.tag)
print(cctv.attrib)
print(cctv.get('id'))

cctv_frame_area = cctv.find('frame_area')
print(cctv_frame_area.text)