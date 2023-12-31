import os
import subprocess
import random
import glob

from scipy.spatial.transform import Rotation as R
import numpy as np
import json


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def write_json(d:dict,path="./images.json"):
    # write json set path ,dict data
    with open(path,"w") as f:
        json.dump(d, f, indent=2,cls=NumpyEncoder)
def set_frameinfo(d):
    frames = []
    for k in d:
        frame = {}
        frame["file_path"] = k
        frame["transform_matrix"] = d[k]
        frames.append(frame)
    return frames
        # print(k)
def set_json_dict(d):
    # print(d)m
    cam_info = {}
    frames = set_frameinfo(d)
    # print(frames)
    cam_info["frames"] = frames
    print("result-json",cam_info)
    return cam_info


# path = "./002.JPG"
def run(dir):
    # path = dir+"/*.JPG"
    files = []
    img = []

    for x in os.listdir(dir):
        if os.path.isfile(dir + x):
            files.append(x)

    for y in files:
        if (y[-4:].lower() == ".jpg" or y[-5:].lower() == ".jpeg"or y[-4:].lower() == ".png"):  # ファイル名の後ろ4文字を取り出してそれが.txtなら
            img.append(y)  # リストに追加
            os.makedirs(f"./wide/{y[:-4]}",exist_ok=True)

    print(f"imag_list:{img}")
    return img

def degree2radian(x):
    return np.radians(x)
def trans_ngp(x,y,z):
    x,y,z = y,x,z
    x,y,z = x,-y,z
    
    return x,y,z

# def trans_nerf(matrix):
#     return matrix[[0, 2, 1 ,3], :]

def make_r_p(d,x=0,y=0,z=0):
    d += [x,y,z]
    return d

def make_r_x(d):
    r_x = np.zeros((3,3),dtype=np.float64)
    r_x[0,0]  = 1
    r_x[1,1]=np.cos(d)
    r_x[1,2]=np.sin(d)
    r_x[2,1]=-np.sin(d)
    r_x[2,2]=np.cos(d)
    return r_x


def make_r_y(d):
    r_y = np.zeros((3,3),dtype=np.float64)
    r_y[1,1] = 1
    r_y[0,0]=np.cos(d)
    r_y[0,2]=-np.sin(d)
    r_y[2,0]=np.sin(d)
    r_y[2,2]=np.cos(d)
    return r_y

def make_r_z(d):
    r_z = np.zeros((3,3),dtype=np.float64)
    r_z[2,2]  = 1
    r_z[0,0]=np.cos(d)
    r_z[0,1]=np.sin(d)
    r_z[1,0]=-np.sin(d)
    r_z[1,1]=np.cos(d)

    return r_z
def make_r_s(s):
    r_s = np.zeros((3,3),dtype=np.float64)
    r_s[0,0]=s
    r_s[1,1]=s
    r_s[2,2]=s
    return r_s

def make_r_m(x,y,z,s):
    r_m = make_r_x(x)
    r_m = r_m@make_r_y(y)
    r_m = r_m@make_r_z(z) 
    r_m = r_m@make_r_s(s)
    return r_m

def calc_potition(mat,dx,dy,dz,x,y,z,s):
    r_m = np.zeros((3,3),dtype=np.float32)
    p = np.zeros((3),dtype=np.float32)
    p[:] = mat
    # print(s)
    p[:] += dx,dy,dz
    r_m = make_r_m(x,y,z,s)
    # print(r_m.shape)
    # print(p.shape)
    # print(p)
    p = r_m@p
    return p    

def make_potition(d_x,d_y,d_z,x,y,z,dx=0.3):
    potitions = np.zeros((1,3),dtype=np.float64)
    potitions[0:3]=[0,-dx,0]

    potitions = calc_potition(potitions,d_x,d_y,d_z,x,y,z,dx)

    return potitions

def make_matrix(x,y,z):
    print("x,y,z:=",x,y,z)

    x,y,z = trans_ngp(x,y,z)
    d_x,d_y,d_z = 1,1,1#移動量
    cam_matrix = np.zeros((4,4),dtype=np.float64)
    cam_matrix[3,3] = 1
    
    x,y,z = degree2radian(x),degree2radian(y),degree2radian(z)
    r = R.from_rotvec([x,y,z])
    rotete_matrix = r.as_matrix()
    cam_matrix[0:3,0:3] = rotete_matrix
    # potitions = make_potition(d_x,d_y,d_z,x,y,z,2)
    potitions = make_potition(d_x,d_y,d_z,x,y,z,0)
    # campoti = rotete_matrix@potitions
    # print(campoti)
    # print(cam_matrix[0:3,3])

    cam_matrix[0:3,3] =potitions
    # print(cam_matrix)
    result = cam_matrix
    # result = trans_ngp(cam_matrix)
    # result = trans_nerf(cam_matrix)
    return result

def mk_dataset(path):
    cnt = 0
    z = 3
    y = 1
    test_num = 0 
    matrix_dict = {}
    
    for j in range(y):
        pitch = (80 * j / y) - 40
        #pitch = 0 
        for i in range(z):
            cnt += 1
            yaw = (40 * i / z) - 20
            roll = 0
            print(f"frames:{cnt}frames,\n./images/train_{path[:-4]}_{cnt}.png")
            mat = make_matrix(roll,pitch,yaw)
            print(mat)
            # matrix_dict[f"./images/train_{path}_{cnt}.png"] = mat
            # print(mat)
            subprocess.call(["python","01_simple_image_convert.py","--image",f"input/{path}","--width","853","--height","480","--output",f"./wide/{path[:-4]}/images/train_{path}_{cnt}.png","--imagepoint","1","--roll","0","--pitch",f"{int(pitch)}","--yaw",f"{int(yaw)}"])
            #subprocess.call(["python","01_simple_image_convert_depth.py","--image",f"input/{path}","--width","853","--height","480","--output",f"./out/{path}/images/train_{cnt}.png","--imagepoint","1","--roll","0","--pitch",f"{int(pitch)}","--yaw",f"{int(yaw)}"])
    print("testStart")
    for cnt in range(test_num):
        yaw = random.randint(0,360)
        pitch = random.randint(-40,40)
        roll = random.randint(0,360)
        scale = random.uniform(.5,3.0)
        print(f"frames:{cnt}")
        mat = make_matrix(yaw,pitch,roll)
        matrix_dict[f"./images/test_{path}_{cnt}.png"] = mat

        subprocess.call(
            ["python", "01_simple_image_convert.py", "--image", f"input/{path}", "--width", "853", "--height", "480", "--output",
             f"./wide/{path[:-3]}/images/test_{path}_{cnt}.png", "--imagepoint", f"{scale}", "--roll", f"{roll}", "--pitch", f"{pitch}",
             "--yaw", f"{yaw}"])
    cam_extrisics = set_json_dict(matrix_dict)
    write_json(cam_extrisics,f"./wide/{path[:-4]}/transforms.json")
        
    

if __name__ == "__main__":
    imgs = run("./input/")
    for img in imgs:
        mk_dataset(img)
