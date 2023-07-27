import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

thresholds_red = (30, 100, 15, 127, 15, 127)
thresholds_blue = (23, 53, 7, 29, -57, -24)
while True:
    clock.tick()
    img = sensor.snapshot().lens_corr(1.8)
    for c in img.find_circles(threshold=3500, x_margin=10, y_margin=10, r_margin=10,
                              r_min=2, r_max=100, r_step=2):
        area = (c.x() - c.r(), c.y() - c.r(), 2 * c.r(), 2 * c.r())
        # area为识别到的圆的区域，即圆的外接矩形框
        statistics = img.get_statistics(roi=area)  # 像素颜色统计

        # (0,100,0,120,0,120)是红色的阈值，所以当区域内的众数（也就是最多的颜色），
        # 范围在这个阈值内，就说明是红色的圆。l_mode()，a_mode()，b_mode()是L通道，A通道，B通道的众数。
        if thresholds_red[0] < statistics.l_mode() < thresholds_red[1] and \
           thresholds_red[2] < statistics.a_mode() < thresholds_red[3] and \
           thresholds_red[4] < statistics.b_mode() < thresholds_red[5]:
            # 如果圆圈是红色
            img.draw_circle(c.x(), c.y(), c.r(), color=(255, 0, 0))  # 用红色圆圈框出识别到的红色圆圈
        else:
            if thresholds_blue[0] < statistics.l_mode() < thresholds_blue[1] and \
               thresholds_blue[2] < statistics.a_mode() < thresholds_blue[3] and \
               thresholds_blue[4] < statistics.b_mode() < thresholds_blue[5]:
                # 如果圆圈是蓝色
                img.draw_circle(c.x(), c.y(), c.r(), color=(0, 0, 255))  # 用蓝色圆圈框出识别到的蓝色圆圈
