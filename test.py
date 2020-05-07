import xml.etree.ElementTree as et

class WaH:
    def __init__(self):
        self.width = 0
        self.height = 0


class TopView:
    def __init__(self):
        self.pts = list()
        self.index = 0
        self.size = WaH()

def convert(string, item):
    tmp_line = item.find(string).text.strip()
    tmp_line = tmp_line.replace('"', '')
    return eval(tmp_line)


tree = et.parse("config_data.xml")
root = tree.getroot()

camera_id = 2


frame_area = []
frame_area_output = tuple()

# top view
top_view = TopView()
top_view_output = TopView()

# counting line
counting_line_lst = []
counting_line_lst_calc = []


# XML 파일에서 데이터 읽어오기.
for cctv in root.iter('cctv'):
    if camera_id == int(cctv.get('id')):
        frame_area_output = convert('frame_area', cctv)
        print(frame_area_output)
        top_view_output.pts = convert('top_view_point', cctv)
        print(top_view_output.pts)
        tmp_tuple = convert('top_view_size', cctv)
        print(tmp_tuple)
        top_view_output.size.width = int(tmp_tuple[0])
        top_view_output.size.height = int(tmp_tuple[1])
        tmp_list = convert('counting_line', cctv)
        print(tmp_list)

