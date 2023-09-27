# 仿射转换，用图片的转换矩阵，与原bbox矩阵运算即可得到新的bbox
# 封装 一个函数，输入图片和gt info，返回变换后的图片和变换后的gt

import cv2
import numpy as np
import os
import random

def get_list(list_path: str):
    #get all filename as a list in the folder
    datalist = os.listdir(f"{list_path}")
    return datalist

def mat_generator(img):
    #each section respresent a operation
    #the range can be modified to adjust the degree of random
    # identity
    h, w = img.shape[:2]
    mat_i = np.float32([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    # reflection  0 means no reflection along the x or y axis
    rx = random.randint(0, 1)
    ry = random.randint(0, 1)
    offset = np.float32([[2 * rx, 0, (-w if rx else 0)], [0, 2 * ry, (-h if ry else 0)], [0, 0, 0]])
    mat_ref = mat_i - offset

    # scale
    # sx and sy represents the scale ratio
    sx = random.randint(50, 150)
    sy = random.randint(50, 150)
    mat_scale = np.float32([[sx / 100, 0, 0], [0, sy / 100, 0], [0, 0, 1]])

    # rotation
    # the degree is set to be n*15° ( 0<n<5)
    # direction is also random generated
    direction = random.randint(0,1)
    theta = (random.randint(0, 6)) * np.pi / 12 *(1 if direction else -1)
    # theta = np.pi / 6
    mat_rot = (np.float32([[1, 0, (w / 2)], [0, 1, (h / 2)], [0, 0, 1]])
               @ np.float32([[np.cos(theta), np.sin(theta), 0], [np.sin(theta), -np.cos(theta), 0], [0, 0, 1]])
               @ np.float32([[1, 0, (-w / 2)], [0, 1, (-h / 2)], [0, 0, 1]])
               )

    # shear
    lambda1 = random.randint(0, 4)
    mat_shear = np.float32([[1, lambda1 / 10, 0], [lambda1 / 10, 1, 0], [0, 0, 1]])

    # because the transform can be seen as matrix operation
    # the final matrix for the operation is equal to all matrix multiplied together
    matrix = mat_i @ mat_ref @ mat_scale @ mat_rot @ mat_shear
    return matrix

def padding_corner(x, y, M):
    #calculate the coordinate of four corner after transform
    left_top = M[:2] @ np.array([0, 0, 1])
    left_bot = M[:2] @ np.array([0, y, 1])
    right_top = M[:2] @ np.array([x, 0, 1])
    right_bot = M[:2] @ np.array([x, y, 1])
    #find the limit value for x and y
    x_min = min(left_bot[0], left_top[0], right_bot[0], right_top[0])
    x_max = max(left_bot[0], left_top[0], right_bot[0], right_top[0])
    y_min = min(left_bot[1], left_top[1], right_bot[1], right_top[1])
    y_max = max(left_bot[1], left_top[1], right_bot[1], right_top[1])
    #padding the image by translating the image to the middle and changing the dsize
    pad_M = np.array([[1, 0, 0 - x_min], [0, 1, 0 - y_min], [0, 0, 1]]) @ M
    dsize = [int(y_max-y_min), int(x_max-x_min)]
    # print(dsize)
    return dsize, pad_M

def coor_trans(polygon:list, matrix):
    #calculate the polygon for gt after transform
    res = []
    for i in range(0, 4):
        new_coor = matrix[:2] @ np.array([int(polygon[i*2]),int(polygon[i*2+1]),1])
        res.append(new_coor[0])
        res.append(new_coor[1])
    return res

def get_bbox(polygon:list):
    #the limit value is the bbox edge
    left = min(polygon[0], polygon[2], polygon[4], polygon[6])
    upper = min(polygon[1], polygon[3], polygon[5], polygon[7])
    right = max(polygon[0], polygon[2], polygon[4], polygon[6])
    lower = max(polygon[1], polygon[3], polygon[5], polygon[7])
    return [left,upper,right,lower]

def affine_trans(scr, M, x, y):
    #apply the affine transform by opencv
    rows, cols = scr.shape[:2]
    trans = cv2.warpAffine(scr, M, dsize=(y, x))
    return trans

def main():

    word_count=1
    # load all file in the traget folder
    for i in range(0,3):
        img_file = f'{image_path}\{img_list[i]}'
        gt_file = f'{gt_path}\{gt_list[i]}'
        scr = cv2.imread(img_file)
        matrix = mat_generator(scr)
        dsize, newM = padding_corner(scr.shape[1], scr.shape[0], matrix)
        trans = affine_trans(scr, newM[:2], dsize[0], dsize[1])

        # with open('image.txt', 'w', encoding='UTF-8') as number:
        #     number.write('\n' + str(i) + '\n')
        #     # to record original image number of the cropped images

        with open(gt_file, 'r', encoding='UTF-8') as f:
            text = f.readlines()
        for line in text:
            gt = line.split(',')
            # print(gt)
            if gt[9] == '###\n':
                # jump the gt that doesn't work
                continue
            else:
                res = []
                res = coor_trans(gt[:8], newM)
                bbox = get_bbox(res)
                crop = trans[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]

                index = str(word_count).zfill(6)
                save_name = f'{save_path}\{index}.{img_format}'
                cv2.imwrite(save_name,crop)

                with open(gt_for_crop, "a", encoding='UTF-8') as file:
                    script = gt[9].rstrip('\n')
                    lan = gt[8]
                    content = f'{index}.png\t{script}\t{lan}'
                    file.write(content + "\n")


                # with open('image.txt', 'w', encoding='UTF-8') as number:
                #     number.write(indexstr + '\t')


                word_count += 1



if __name__ == '__main__':
    #modify the file path according to the database
    image_path = "D:\AllProjects\DATAbase\OCRdata\icdar2019\detection\\train\ImagesPart1"
    gt_path = "D:\AllProjects\DATAbase\OCRdata\icdar2019\detection\\train\gt"
    save_path = "D:\AllProjects\DATAbase\OCRdata\icdar2019\detection\\train\\test"
    gt_for_crop = "D:\AllProjects\DATAbase\OCRdata\icdar2019\detection\\train\\test\gt.txt"
    img_format = 'jpg' #set to jpg or png or etc.
    img_list = get_list(image_path)
    gt_list = get_list(gt_path)
    main()



