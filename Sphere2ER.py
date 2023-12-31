import cv2
import numpy as np
import os

def equirectangular_to_dome(equi_img):
    height, width = equi_img.shape[:2]

    # ドームマスターのサイズ（仮で512x512に設定）
    dome_size = (512, 512, 3)
    dome_img = np.zeros(dome_size, dtype=np.uint8)

    # ドームマスターの中心座標
    dome_center = (dome_size[0] // 2, dome_size[1] // 2)

    # 各ピクセルごとに変換
    for y in range(dome_size[0]):
        for x in range(dome_size[1]):
            # ドーム座標系での座標
            phi = ((y / dome_size[0]) - 0.5) * np.pi
            theta = (x / dome_size[1]) * 2 * np.pi

            # エクイレクタングラー座標系での座標
            equi_x = int((theta / (2 * np.pi)) * width) % width
            equi_y = int((phi / np.pi + 0.5) * height)

            # ドームマスターにピクセルをコピー
            dome_img[y, x] = equi_img[equi_y, equi_x]

    return dome_img

def dome_to_equirectangular(dome_img):
    height, width = dome_img.shape[:2]

    # エクイレクタングラーのサイズ
    equi_img = np.zeros((height, width, 3), dtype=np.uint8)

    # ドームマスターの中心座標
    dome_center = (dome_img.shape[0] // 2, dome_img.shape[1] // 2)

    # 各ピクセルごとに逆変換
    for y in range(height):
        for x in range(width):
            # ドーム座標系での座標
            phi = ((y / height) - 0.5) * np.pi
            theta = (x / width) * 2 * np.pi

            # エクイレクタングラー座標系での座標
            equi_x = int((theta / (2 * np.pi)) * width) % width
            equi_y = int((phi / np.pi + 0.5) * height)

            # エクイレクタングラーにピクセルをコピー
            equi_img[y, x] = dome_img[equi_y, equi_x]

    return equi_img

# 入力ディレクトリ内のすべてのエクイレクタングラー画像を処理
input_directory = './input'
output_directory = './output'

# 複数のドームマスター画像に変換し、再度エクイレクタングラーに逆変換
for filename in os.listdir(input_directory):
    if filename.endswith(('.jpg', '.jpeg', '.png','.JPG')):
        input_path = os.path.join(input_directory, filename)

        # エクイレクタングラー画像を読み込み
        equi_img = cv2.imread(input_path)

        # エクイレクタングラーからドームマスターへ変換
        dome_img = equirectangular_to_dome(equi_img)

        # 変換結果を保存
        output_path = os.path.join(output_directory, f'dome_{filename}')
        cv2.imwrite(output_path, dome_img)

        # ドームマスターからエクイレクタングラーへ逆変換
        reconstructed_equi_img = dome_to_equirectangular(dome_img)

        # 逆変換結果を保存
        output_path = os.path.join(output_directory, f'reconstructed_equirectangular_{filename}')
        cv2.imwrite(output_path, reconstructed_equi_img)