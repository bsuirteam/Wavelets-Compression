import cv2


import matplotlib.pyplot as plt
from matplotlib.image import imread
import numpy as np

import pywt
import pywt.data
import differnce
import moviepy
import time
import os


def d_wavelet_transform(array, wavelet):
    return pywt.dwtn(array, wavelet)
   

def quantum_tuple(matrix, step):

    if step == 1:
        return matrix

    if step == 0:
        quantized = matrix * 0
        return quantized
    
    quantized = np.round(matrix / step) * step


    return quantized
           
            
def inverse_discrete_wavelet_transform(coeffs :dict,  wavelet:str):
    return pywt.idwtn(coeffs, wavelet)




def check_video_fps(file: str):
    cam = cv2.VideoCapture(file)
    fps = cam.get(cv2.CAP_PROP_FPS)
    return fps



    
def video_reader(file:str, n :int ):
    vidcap = cv2.VideoCapture(file)
    success,image = vidcap.read()
    if not success:
        return SystemError
    count = 0

    out_array = []


    if n == 0:
        count = -1

    print(count, success)
    while count < n and success:
        
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        out_array.append(image)
        success,image = vidcap.read()

        if n != 0:
            count += 1

    vidcap.release()
    result = np.stack(out_array)

    return result


def cunk_wavelet_sampling(inp, outfile, wavelet_type, quantum_rate, framerate = 30, chunk_size = 30):

    vidcap = cv2.VideoCapture(inp)
    success,image = vidcap.read()
    if not success:
        return SystemError
    count = 0

    out_array = []





    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    out = None

    while True:

        while count < chunk_size and success:
        
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
            out_array.append(image)
            success,image = vidcap.read()

            count += 1


        result = np.stack(out_array)
        out_array.clear()
        count = 0

        procced = d_wavelet_transform(result, wavelet_type)
        for tp in ["aad", "ada", "daa", "dad", "add", "ddd"]:
            procced[tp] = quantum_tuple(procced[tp], quantum_rate)


        sampled = inverse_discrete_wavelet_transform(procced, wavelet_type)



        min_val = np.min(sampled)
        max_val = np.max(sampled)
    
        if max_val - min_val == 0:
            normalized = np.zeros(sampled.shape, dtype=np.uint8)
        else:
            normalized = ((sampled - min_val) / (max_val - min_val) * 255).astype(np.uint8)


        if out is None:
            n_frames, height, width = normalized.shape
            out = cv2.VideoWriter(outfile, fourcc, framerate, (width, height), isColor=False)

   
        for frame in normalized:
            out.write(frame)   


        if not success :
            vidcap.release()
            break   

    out.release()         


def cunk_wavelet_compress(inp, wavelet_type, quantum_rate, framerate = 30, chunk_size = 30):

    vidcap = cv2.VideoCapture(inp)
    success,image = vidcap.read()
    if not success:
        return SystemError
    count = 0

    out_array = []





    fourcc = cv2.VideoWriter_fourcc(*'XVID') 
    out = None

    while True:

        while count < chunk_size and success:
        
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
            out_array.append(image)
            success,image = vidcap.read()

            count += 1


        result = np.stack(out_array)
        out_array.clear()
        count = 0

        procced = d_wavelet_transform(result, wavelet_type)
    
        sampled = procced["aaa"]



        min_val = np.min(sampled)
        max_val = np.max(sampled)
    
        if max_val - min_val == 0:
            normalized = np.zeros(sampled.shape, dtype=np.uint8)
        else:
            normalized = ((sampled - min_val) / (max_val - min_val) * 255).astype(np.uint8)


        if out is None:
            n_frames, height, width = normalized.shape
            out = cv2.VideoWriter("compressed.avi", fourcc, framerate, (width, height), isColor=False)

   
        for frame in normalized:
            out.write(frame)   


        if not success :
            vidcap.release()
            break   

    out.release()         







def bytes_to_video(frames_array, output_path, fps=30):

   
    min_val = np.min(frames_array)
    max_val = np.max(frames_array)
    
    if max_val - min_val == 0:
        normalized = np.zeros(frames_array.shape, dtype=np.uint8)
    else:
        normalized = ((frames_array - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    n_frames, height, width = normalized.shape
    fourcc = cv2.VideoWriter_fourcc(*"mp4v") 
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=False)
   
    for frame in normalized:
        out.write(frame)

    out.release()



def wavelet_sampling(inp, frame_to_read, wavelet_type, quantum_rate, framerate = 30):
    start_array = video_reader(inp, frame_to_read)
    procced = d_wavelet_transform(start_array, wavelet_type)


    procced["aad"] = quantum_tuple(procced["aad"], quantum_rate)
    procced["ada"] = quantum_tuple(procced["ada"], quantum_rate)
    procced["daa"] = quantum_tuple(procced["daa"], quantum_rate)
    procced["dda"] = quantum_tuple(procced["dda"], quantum_rate)
    procced["dad"] = quantum_tuple(procced["dad"], quantum_rate)
    procced["add"] = quantum_tuple(procced["add"], quantum_rate)
    procced["ddd"] = quantum_tuple(procced["ddd"], quantum_rate)
    

    sampled = inverse_discrete_wavelet_transform(procced, wavelet_type)
    bytes_to_video(sampled, "sampled.mp4", framerate)



def convet_to_mp4(file: str):
    clip = moviepy.VideoFileClip(file)
    clip.write_videofile(file.split(".")[0] + ".mp4")






# array = video_reader("/home/udainoko/Documents/NVDIA_PET_PROJECT/Radiohead - Street Spirit (Fade Out).mp4", 500)
# new_array = d_wavelet_transform(array, 'bior3.7')



# new_array["aad"] = quantum_tuple(new_array["aad"], 100)









# bytes_to_video(new_array["aaa"], "new_vide0_MAIN.mp4")
# bytes_to_video(new_array["aad"], "new_vide0_SEC.mp4")




path_to_pre = "/home/udainoko/Documents/NVDIA_PET_PROJECT/Radiohead - Street Spirit (Fade Out).mp4"

fps = check_video_fps(path_to_pre)
# path_to_post = "sampled"

# #wavelet_sampling(path_to_pre, 0, 'bior3.7', 10)


operFileName = "bior_best_710"



start_time = time.time()
cunk_wavelet_sampling(path_to_pre, operFileName + ".avi", 'bior6.8',710, fps, 300)
end_time = time.time()

elapsed_time = end_time - start_time

print(f"The task took {elapsed_time:.2f} seconds to complete.")
# #cunk_wavelet_compress(path_to_pre, 'haar', 1, fps, fps)





convet_to_mp4("/home/udainoko/Documents/NVDIA_PET_PROJECT/" + operFileName + ".avi")


file_size_bytes = os.path.getsize("/home/udainoko/Documents/NVDIA_PET_PROJECT/" + operFileName + ".avi")
file_size_ethalon = os.path.getsize("/home/udainoko/Documents/NVDIA_PET_PROJECT/ethalon.avi")


file_size_bytes_mp4 = os.path.getsize("/home/udainoko/Documents/NVDIA_PET_PROJECT/" + operFileName + ".mp4")
file_size_ethalon_mp4 = os.path.getsize("/home/udainoko/Documents/NVDIA_PET_PROJECT/ethalon.mp4")


out_ssim = differnce.ssim("/home/udainoko/Documents/NVDIA_PET_PROJECT/" + operFileName + ".avi","/home/udainoko/Documents/NVDIA_PET_PROJECT/ethalon.avi" )
out_psnr = differnce.psnr("/home/udainoko/Documents/NVDIA_PET_PROJECT/" + operFileName + ".avi","/home/udainoko/Documents/NVDIA_PET_PROJECT/ethalon.avi" )
print("ssim_avi: ",out_ssim)
print("psnr_avi: ",out_psnr)
print("si_avi: ", file_size_bytes / file_size_ethalon)



out_ssim = differnce.ssim("/home/udainoko/Documents/NVDIA_PET_PROJECT/" + operFileName + ".mp4","/home/udainoko/Documents/NVDIA_PET_PROJECT/ethalon.mp4" )
out_psnr = differnce.psnr("/home/udainoko/Documents/NVDIA_PET_PROJECT/" + operFileName + ".mp4","/home/udainoko/Documents/NVDIA_PET_PROJECT/ethalon.mp4" )
print("ssim_mp4: ",out_ssim)
print("psnr_mp4: ",out_psnr)
print("si_mp4: ", file_size_bytes_mp4 / file_size_ethalon_mp4)