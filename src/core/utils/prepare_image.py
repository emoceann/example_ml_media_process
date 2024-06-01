from typing import Any

import cv2
import numpy as np
from cv2 import Mat

type CvImage = Mat | np.ndarray[Any, np.dtype[np.generic]] | np.ndarray


def center_crop(
        img: CvImage,
        out_height: int,
        out_width: int
) -> CvImage:
    height, width, _ = img.shape
    left = int((width - out_width) / 2)
    right = int((width + out_width) / 2)
    top = int((height - out_height) / 2)
    bottom = int((height + out_height) / 2)
    img = img[top:bottom, left:right]
    return img


def resize_with_aspectratio(
        img: CvImage,
        out_height: int,
        out_width: int,
        scale=87.5,
        inter_pol=cv2.INTER_LINEAR
) -> CvImage:
    height, width, _ = img.shape
    new_height = int(100. * out_height / scale)
    new_width = int(100. * out_width / scale)
    if height > width:
        w = new_width
        h = int(new_height * height / width)
    else:
        h = new_height
        w = int(new_width * width / height)
    img = cv2.resize(img, (w, h), interpolation=inter_pol)
    return img


def pre_process_edgetpu(
        img: CvImage,
        dims: tuple[int, int, int]
) -> np.ndarray:
    output_height, output_width, _ = dims
    img = resize_with_aspectratio(img, output_height, output_width, inter_pol=cv2.INTER_LINEAR)
    img = center_crop(img, output_height, output_width)
    img = np.asarray(img, dtype='float32')
    img -= [127.0, 127.0, 127.0]
    img /= [128.0, 128.0, 128.0]
    return img
