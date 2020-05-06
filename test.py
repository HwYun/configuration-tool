import xml.etree.ElementTree as et

tree = et.parse("config_data.xml")
root = tree.getroot()

camera_id = '1'

for cctv in root.iter('cctv'):
    if camera_id == cctv.get('id'):

        new_frame_area = ((0, 0), (1600, 900))
        cctv.find('frame_area').text = str(new_frame_area)
        # cctv.find('frame_area').set('updated', 'yes')

        new_top_view_point = [[1, 2], [1, 2], [1, 2], [1, 2]]
        cctv.find('top_view_point').text = str(new_top_view_point)
        # cctv.find('top_view_point').set('updated', 'yes')

        new_top_view_size = (1200, 800)
        cctv.find('top_view_size').text = str(new_top_view_size)

        new_counting_line = [[[[300, 400], [500, 600]], True]]
        cctv.find('counting_line').text = str(new_counting_line)

        new_ROI = "Sample String"
        cctv.find('ROI_mask').text = new_ROI

        new_HOI = ""
        cctv.find('HOI_shelf').text = new_HOI

tree.write('output.xml')