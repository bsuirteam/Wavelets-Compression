import cv2


import matplotlib.pyplot as plt
from matplotlib.image import imread
import numpy as np

import pywt
import pywt.data



def d_wavelet_transform(array, wavelet):
    return pywt.dwtn(array, wavelet)
   

def quantum_tuple(matrix, step):


    quantized = np.round(matrix / step) * step


    return quantized
           
            
def inverse_discrete_wavelet_transform(coeffs :dict,  wavelet:str):
    return pywt.idwtn(coeffs, wavelet)
    
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





    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
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





    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
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
            out = cv2.VideoWriter("compressed.mp4", fourcc, framerate, (width, height), isColor=False)

   
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
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
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





# array = video_reader("/home/udainoko/Documents/NVDIA_PET_PROJECT/Radiohead - Street Spirit (Fade Out).mp4", 500)
# new_array = d_wavelet_transform(array, 'bior3.7')



# new_array["aad"] = quantum_tuple(new_array["aad"], 100)









# bytes_to_video(new_array["aaa"], "new_vide0_MAIN.mp4")
# bytes_to_video(new_array["aad"], "new_vide0_SEC.mp4")




path_to_pre = "/home/udainoko/Documents/NVDIA_PET_PROJECT/Radiohead - Street Spirit (Fade Out).mp4"
path_to_post = "sampled"

#wavelet_sampling(path_to_pre, 0, 'bior3.7', 10)
#cunk_wavelet_sampling(path_to_pre, "sample_step_1000.mp4", 'haar', 24, 10000)
cunk_wavelet_compress(path_to_pre, 'bior3.7', 1, 24, 1000)
