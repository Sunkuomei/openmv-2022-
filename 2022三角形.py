import sensor, image, time
from pyb import UART

#uart = UART(1, 115200)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(20)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)


# 修改颜色阈值
thresholds_red = (30, 100, 15, 127, 15, 127)
thresholds_blue = (23, 53, 7, 29, -57, -24)

def opv_find_color_blobs():
    img = sensor.snapshot()
   
    for b in img.find_blobs([thresholds_red, thresholds_blue], pixels_threshold=30, merge=True, margin=50):

        if b.code() == 1:
            print('颜色为红色')
            if 0.2 < b.density() <0.52:
              img.draw_cross(b.cx(), b.cy())
              print('三角形', b.cx(), b.cy(), b.density(),)
        if b.code() == 2:
            print('颜色为蓝色')
            if 0.2 < b.density() <0.52:
              img.draw_cross(b.cx(), b.cy())
              print('三角形', b.cx(), b.cy(), b.density(),)
        

        
        

        
while True:
    opv_find_color_blobs()