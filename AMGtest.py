import cv2 as cv
import numpy as np

import time
import busio
import board

import adafruit_amg88xx
import colorsys

# I2Cの初期化
i2c = busio.I2C(board.SCL, board.SDA)
# サーモセンサーの初期化
sensor = adafruit_amg88xx.AMG88XX(i2c, addr=0x68)

# 初期化のために待つ
time.sleep(0.2)

# 表示のための配列を用意する
img = np.full((320, 320, 3), 128, dtype=np.uint8)

# セルサイズ
cellsize = 40

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def mapVal(val, inMin, inMax, outMin, outMax):
    return (val - inMin) * (outMax - outMin) / (inMax - inMin) + outMin

# 8x8の温度配列
pixels = sensor.pixels
for x in range(len(pixels)):
    for y in range(len(pixels[0])):
        # 15〜28の値を、270〜0の範囲に変換する
        val = mapVal(pixels[x][y], 15, 28, 270, 0)
        # 値を0〜270の範囲に収める
        val = min(max(0, val), 270)
        # HSVで指定した色をRGBに変換する
        color = tuple(reversed(hsv2rgb(val/360, 1.0, 0.5)))
        # 1ピクセルずつ表示する
        cv.rectangle(img, (x*cellsize, y*cellsize), (x*cellsize+cellsize, y*cellsize+cellsize), color, thickness=-1)

# 結果の画像を表示する
cv.imshow('image', img);
# 何かキーが押されるまで待機する
cv.waitKey()

# 表示したウィンドウを閉じる
cv.destroyAllWindows()