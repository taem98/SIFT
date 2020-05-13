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
    blur_octaves = np.load('blur_result/blur_image_array.npy', allow_pickle=True)
    DoG_octaves = DoG(blur_octaves)
