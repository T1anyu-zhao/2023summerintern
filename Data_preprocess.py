import os
from PIL import Image
import cv2

gt_path = r'D:\AllProjects\python\OCR\icdar2019\detection\train\gt'
img_path = r'D:\AllProjects\python\OCR\icdar2019\detection\train\ImagesPart1'
save_path = r'D:\AllProjects\python\OCR\icdar2019\detection\train\img'
word_gt = r'D:\AllProjects\python\OCR\icdar2019\detection\train\All_word_gt.txt'
gt_files = os.listdir(gt_path)
img_files = os.listdir(img_path)
# print(img_files)
# print(gt_files)
# loading images 1
# gt_file = f'{gt_path}\{gt_files[0]}'
# img_file = f'{img_path}\{img_files[0]}'
# print(gt_file)
# print(img_file)
# print(gt_files[0])

count = 0
index = 0

for i in range(0, len(gt_files)):
    gt_file = f'{gt_path}\{gt_files[i]}'
    img_file = f'{img_path}\{img_files[i]}'
    img = Image.open(img_file)
    # print(i)
    if i % 1000 == 0:
        print(f'{i / 10000}% of images has done')

    with open(gt_file, 'r', encoding='UTF-8') as f:
        text = f.readlines()
        # print(text)
        # print(len(text))
        count += len(text)
    with open('image.txt', 'w', encoding='UTF-8') as number:
        number.write('\n' + str(i) + '\n')

    for line in text:
        gt = line.split(',')
        # print(gt)
        if gt[9] == '###\n':
            continue
        else:
            coor = []
            coor = list(map(int, gt[0:8]))
            # print(coor)
            left = min(coor[0], coor[2], coor[4], coor[6])
            upper = min(coor[1], coor[3], coor[5], coor[7])
            right = max(coor[0], coor[2], coor[4], coor[6])
            lower = max(coor[1], coor[3], coor[5], coor[7])
            if right == left:
                right += 1
            if upper == lower:
                lower += 1
            box = (left, upper, right, lower)
            crop = img.crop(box)
            indexstr = str(index).zfill(6)
            save_img = f'{save_path}\icdar_2019_word_{indexstr}.png'
            crop.save(save_img)
            with open(word_gt, "a", encoding='UTF-8') as file:
                script = gt[9].rstrip('\n')
                lan = gt[8]
                content = f'icdar_2019_word_{indexstr}.png\t{script}\t{lan}'
                file.write(content + "\n")
            with open('image.txt', 'w', encoding='UTF-8') as number:
                number.write(indexstr + '\t')
            index += 1

print(count)

#
# with open(gt_file, 'r', encoding='UTF-8') as f:
#     text = f.readlines()
#     print(text)
#     print(len(text))
# # loading the coresponding gt txt
# img = Image.open(img_file)
# for line in text:
#     gt = line.split(',')
#     print(gt)
#     if gt[9] == '###\n':
#         continue
#     else:
#         coor = []
#         coor = list(map(int, gt[0:8]))
#         print(coor)
#         x_left = min(coor[0],coor[2],coor[4],coor[6])
#         x_right = max(coor[0],coor[2],coor[4],coor[6])
#         y_top = min(coor[1],coor[3],coor[5],coor[7])
#         y_bot = max(coor[1],coor[3],coor[5],coor[7])
#         box = (x_left,y_top,x_right,y_bot)
#         crop = img.crop(box)
#         indexstr = str(index).zfill(6)
#         save_img = f'{save_path}\icdar_2019_word_{indexstr}.png'
#         crop.save(save_img)
#         with open(word_gt, "a", encoding='UTF-8') as file:
#             script = gt[9].rstrip('\n')
#             lan = gt[8]
#             content = f'icdar_2019_word_{indexstr}.png\t{script}\t{lan}'
#             file.write(content + "\n")
#         index += 1
#
# # read the txt file. seperate the coor , language , script
