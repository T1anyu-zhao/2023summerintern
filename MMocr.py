import json
from PIL import Image
import os
ROOT_PATH = f'./icdar2019/detection/train'
data = {
        "metainfo":
        {
          "dataset_type": "TextDetDataset",  # 可选项: TextDetDataset/TextRecogDataset/TextSpotterDataset
          "task_name": "textdet",  #  可选项: textdet/textspotter/textrecog
          "category": [{"id": 0, "name": "text"}]  # 在 textdet/textspotter 里用到
        },
        "data_list":
        []
    }
FILE_PATH = f'./icdar2019/detection/train/train.json'
def get_bbox(polygon:list):
    left = min(polygon[0], polygon[2], polygon[4], polygon[6])
    upper = min(polygon[1], polygon[3], polygon[5], polygon[7])
    right = max(polygon[0], polygon[2], polygon[4], polygon[6])
    lower = max(polygon[1], polygon[3], polygon[5], polygon[7])
    return [left,upper,right,lower]
def convert_to_dict(path:str,height:int,width:int,all_instances_list:list):
    global data
    one_image_info = {
        "img_path": path,
        "height": height,
        "width": width,
        "instances":  # 一图内的多个实例
            all_instances_list
    }
    data['data_list'].append(one_image_info)

def get_image_list():
    return os.listdir(ROOT_PATH+'/ImagesPart1')

def get_all_instances(instance_list):
    data = []
    for instance in instance_list:
        new_instance_dict = {
            "bbox": get_bbox(instance),  # textdet/textspotter 内用到, [x1, y1, x2, y2]。
            "bbox_label": 0,  # 对象类别, 在 MMOCR 中恒为 0 (文本)
            "polygon": instance,  # textdet/textspotter 内用到。 [x1, y1, x2, y2, ....]
            "text": "",  # textspotter/textrecog 内用到
            "ignore": False  # textspotter/textdet 内用到，决定是否在训练时忽略该实例
        }
        data.append(new_instance_dict)
    return data

def save_json():
    global data
    with open(FILE_PATH,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=2)
def main():
    global data
    for idx,image in enumerate(image_list):
        print(f"Processing {idx}th image")
        width,height = Image.open(ROOT_PATH+'/ImagesPart1/'+image).size
        gt_path = f"{ROOT_PATH}/gt/{image.split('.')[0]}.txt"
        instance_list = []
        with open(gt_path,'r',encoding='utf=8') as f:
            for line in f:
                line.strip()
                if not line:
                    continue
                #print(line)
                str_list = line.split(',')[:8]
                #print(str_list)
                int_list = list(map(int, str_list))
                instance_list.append(int_list)
        all_instance_list = get_all_instances(instance_list)
        convert_to_dict(image,height,width,all_instance_list)

    save_json()




#
# if __name__ == '__main__':
#     image_list = get_image_list()
#     main()
#

