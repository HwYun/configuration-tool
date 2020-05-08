import xml.etree.ElementTree as et
import copy

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
        # tmp_list 의 첫번째 index는 각각의 line의 index
        # 두번째 index는 line의 시작&끝 좌표, counting 방향(T/F)
        # 세번째 index는 두번째 index이 [0]일 경우 시작 or 끝 좌표 (0: 시작, 1: 끝)
        print(tmp_list[0][0][0])
        print(tmp_list[0][0][1])

print("---------------------------------")
top_view = top_view_output
print(top_view)
print(top_view.pts)
print(top_view.size.width)
print(top_view.size.height)

top_view = copy.deepcopy(top_view_output)

top_view_output.pts.pop()
print(top_view.pts)
