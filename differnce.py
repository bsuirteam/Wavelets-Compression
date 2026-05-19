
import numpy as np
import cv2
import math
from skimage.metrics import structural_similarity as ssim_computate

def ssim(compressed:str, original:str) ->float:

    comp = get_imagaes(compressed)
    orig = get_imagaes(original)

    seq_len = min(len(comp), len(orig))
    ssim_total = 0

    for i in range(seq_len):
        ssim_total += ssim_computate(orig[i], comp[i], data_range = 255)


    return ssim_total/seq_len


def psnr(compressed: str, original: str) -> float:


    comp = get_imagaes(compressed)
    orig = get_imagaes(original)

    seq_len = min(len(comp), len(orig))
    total_psnr = 0
    

    for i in range(seq_len):
        mse = np.mean((orig[i] - comp[i]) ** 2)
        if(mse == 0):  # MSE is zero means no noise is present in the signal .
            total_psnr += 100
            continue
        max_pixel = 255.0
        total_psnr  += 20 * math.log10(max_pixel / math.sqrt(mse))


    return total_psnr / seq_len




def get_imagaes(video:str):
    vidcap = cv2.VideoCapture(video)
    success,image = vidcap.read()
    if not success:
        return SystemError

    out_array = []
    while success:
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        out_array.append(image)
        success,image = vidcap.read()


    vidcap.release()
    result = np.stack(out_array)

    return result