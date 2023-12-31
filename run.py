import os
import subprocess
import random
import glob


# path = './002.JPG'
def run(dir):
    # path = dir+'/*.JPG'
    files = []
    img = []

    for x in os.listdir(dir):
        if os.path.isfile(dir + x):
            files.append(x)

    for y in files:
        if (y[-4:].lower() == '.jpg' or y[-5:].lower() == '.jpeg'or y[-4:].lower() == '.png'):  # ファイル名の後ろ4文字を取り出してそれが.txtなら
            img.append(y)  # リストに追加
    print(f'imag_list:{img}')
    return img


def mk_dataset(path):
    cnt = 0
    z = 100
    y = 10
    test_num = 180
    for j in range(y):
        pitch = (80 * j / y) - 40
        for i in range(z):
            cnt += 1
            yaw = (360 * i / z) - 180
            print(f"frames:{cnt}")
            subprocess.call(['python','01_simple_image_convert.py','--image',f'input/{path}','--width','853','--height','480','--output',f'./out/{path}/images/train_{path}_{cnt}.png','--imagepoint','1','--roll','0','--pitch',f'{int(pitch)}','--yaw',f'{int(yaw)}'])
    print('testStart')
    for cnt in range(test_num):
        yaw = random.randint(0,360)
        pitch = random.randint(-40,40)
        roll = random.randint(0,360)
        scale = random.uniform(.5,3.0)
        print(f"frames:{cnt}")
        subprocess.call(
            ['python', '01_simple_image_convert.py', '--image', f'input/{path}', '--width', '853', '--height', '480', '--output',
             f'./out/{path}/images/test_{path}_{cnt}.png', '--imagepoint', f'{scale}', '--roll', f'{roll}', '--pitch', f'{pitch}',
             '--yaw', f'{yaw}'])

if __name__ == '__main__':
    imgs = run('./input/')
    for img in imgs:
        mk_dataset(img)
