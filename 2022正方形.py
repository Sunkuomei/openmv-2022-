import sensor, image, time
from pyb import UART
##初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# 红色和蓝色的阈值
thresholds_red = (30, 100, 15, 127, 15, 127)
thresholds_blue =(23, 53, 7, 29, -57, -24)

while True:
    clock.tick()
    img = sensor.snapshot()

    for r in img.find_rects(threshold=3500, x_margin=10, y_margin=10, r_margin=10,
                            r_min=2, r_max=100, r_step=2):
        area = r.rect()
        statistics = img.get_statistics(roi=area)  # 像素颜色统计

        if thresholds_red[0] < statistics.l_mode() < thresholds_red[1] and \
           thresholds_red[2] < statistics.a_mode() < thresholds_red[3] and \
           thresholds_red[4] < statistics.b_mode() < thresholds_red[5]:
            # 如果矩形是红色，用红色矩形框出识别到的红色矩形
            img.draw_rectangle(area, color=(255, 0, 0))
        else: 
            if thresholds_blue[0] < statistics.l_mode() < thresholds_blue[1] and \
               thresholds_blue[2] < statistics.a_mode() < thresholds_blue[3] and \
               thresholds_blue[4] < statistics.b_mode() < thresholds_blue[5]:
                # 如果矩形是蓝色，用蓝色矩形框出识别到的蓝色矩形
                img.draw_rectangle(area, color=(0, 0, 255))

