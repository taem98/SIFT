
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import operator
import math
import sys

from gaussian_blur import gaussian_filter

def find_orientation(img_box, img_idx):
    bins = 36
    histogram = []

    orientation_box = np.zeros((17, 17))
    
    # orientation 구하기
    for i in range(1, 16):
        for j in range(1, 16):
            dx = img_box[i][j+1] - img_box[i][j-1]
            dy= img_box[i+1][j] - img_box[i-1][j]
            orientation = np.rad2deg(np.arctan2(dy, dx))
            orientation_box[i][j] = orientation
    
    # 칼만 필터 적용
    size = 17
    sigma = (2) ** (img_idx + 1)
    kerner = gaussian_filter(size, sigma)
    orientation_box = orientation_box * kerner

    # histogram 구하기
    for i in range(1, 16):
        for j in range(1, 16):
            histogram_index = int(round(orientation_box[i][j] * bins / 360.))
            histogram.append(histogram_index)

    # -17 ~ +18
    histogram = np.array(histogram) 
    
    check_list = {} # ex > {1: 13, -1: 12, 2: 3}
    for ht in histogram:
        try:
            if ht == 0:
                pass
            else:
                check_list[str(ht)] += 1
        except:
            check_list[str(ht)] = 1
    
    if len(check_list.values()) == 0 :
        return 0

    ht_max = max(check_list.values())
    for max_value in check_list:
        if check_list[max_value] == ht_max:
            ht_max_key = max_value

    ht_max_key = int(ht_max_key)
    if ht_max_key > 0 :
        ht_max_key *= 10
    else:
        ht_max_key = 360 - (ht_max_key-1)*10

    return ht_max_key


def draw(octaves, orientation_img):
    pass

def make_direction(octaves, mm_check_img):
    '''
    size of box = 17
    '''
    # key point img 한장씩만 출력
    octaves_key_imgs = []
    for imgs in mm_check_img:
        if imgs[1].sum() != 0:
            octaves_key_imgs.append(imgs[1])
        else:
            octaves_key_imgs.append(imgs[0])

    orientation_imgs = []
    for img_idx, key_img in enumerate(octaves_key_imgs):
        row = key_img.shape[0]
        col = key_img.shape[1]
        
        key_img_pd = np.zeros((row+2, col+2))
        key_img_pd[1:row+1, 1:col+1] = key_img[:]
        
        # 검사를 위한 padding
        n_key_img_pd = np.zeros((row+18, col+18))
        n_key_img_pd[8:-8, 8:-8] = key_img_pd[:]
        octave_img_pd = np.zeros((row+18, col+18))
        octave_img_pd[8:-8, 8:-8] = octaves[img_idx][:]

        orientation_img = np.zeros((row+18, col+18))

        # 연산량.. 
        for i in range(9, row+9):
            for j in range(9, col+9):
                try:
                    if n_key_img_pd[i][j] == 255:
                        box = octave_img_pd[8+(i-8):8+(i+9), 8+(j-8):8+(j+9)]

                        orientation_img[i][j] = find_orientation(box, img_idx)
                except:
                    pass
            print(i)

        
        orientation_imgs.append(orientation_img[8:-8, 8:-8])
     
    # draw(octaves, orientation_imgs)

        np.save('orientation/orientation', orientation_imgs)
        # 연산량 때문에 일단은 한번 하고 끝
        break
    return np.array(orientation_imgs)
    