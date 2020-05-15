# SIFT 구현

import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import operator
import math
import sys

from functools import reduce
from PIL import Image

from gaussian_blur import make_space
from orientation import make_direction
from find_mm import find_mm
from DoG import DoG

from gaussian_blur import gaussian_filter

def draw(octave, orientation_img):
    row = octave.shape[0]
    col = octave.shape[1]
    octave_img = octave[:]
    for i in range(row):
        for j in range(col):
            if orientation_img[i][j] != 0:
                cv.arrowedLine(octave_img, (i,j), (i+5, j+5), (255, 0, 0), thickness=2)
            else:
                pass
    cv.imshow('arroweline', octave)
    cv.waitKey(0)


if __name__ == "__main__":
    '''
    1. "scale space" 만들기
    2. Difference of Gaussian(DoG) 연산
    3. keypoint들 찾기
    4. 나쁜 keypoint 들 제거하기
    5. keypoint들에 방향 할당 해주기
    6. 최종적으로 SIFT 특징들 산출하기
    '''
    # 연산 시간이 너무 오래 걸려서 numpy array로 저장값 불러옴
    # img_path ='imgs/img1.ppm'
    # octaves = make_space(img_path)
    octaves = np.load('octave_imgs/octave_imgs.npy', allow_pickle=True)
    blur_octaves = np.load('blur_result/blur_image_array.npy', allow_pickle=True)
    
    # DoG_octaves = DoG(blur_octaves)
    DoG_octaves = np.load('DoG_result/DoG_result_array.npy', allow_pickle=True)
    
    # mm_check_img = find_mm(DoG_octaves)
    mm_check_img = np.load('mm_check_img/mm_check_imgs.npy', allow_pickle=True)
    
    orientation_img = make_direction(octaves, mm_check_img)
    orientation_img = np.load('orientation/orientation.npy', allow_pickle=True)
    draw(octaves[0], orientation_img[0])
    
