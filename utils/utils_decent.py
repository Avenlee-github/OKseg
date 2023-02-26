from multiprocessing.context import _default_context
from tkinter import font
from PIL import Image
import cv2
import numpy as np

# 导入单位文件，导入失败则使用像素作为单位
try:
    from utils.units import length_unit, square_unit
    units_setting = True
except:
    units_setting = False


def pil2cv(img):
    # 图片转换PIL到opencv格式
    image = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return image

def cv2pil(img):
    # 将opencv转化为PIL格式
    image = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    return image

class Decentration_Cal:
    def __init__(self, segment, image, optic_center, tag, defocus):
        self.segment = segment
        self.image = image
        self.optic_center = optic_center
        self.tag = tag
        assert isinstance(defocus, bool), "defocus必须是布尔值, True为检测离焦环, Fasle为不检测离焦环!"
        self.defocus = defocus

    def centers_cal(self):
        ## 计算图片中心和治疗区中心，坐标以图片左上角为原点
        segment = pil2cv(self.segment)
        # 计算图片中心
        im_center = self.optic_center
        gray = cv2.cvtColor(segment, cv2.COLOR_BGR2GRAY)
        # 计算治疗区中心，根据是否检测离焦环选择
        if self.defocus == False:
            _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        elif self.defocus == True:
            _, thresh_1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
            _, thresh_2 = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY)
            thresh = thresh_1 - thresh_2
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            # 再找出最大的离焦环
            df_contours, _ = cv2.findContours(thresh_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            df_areas = []
            for df_c in df_contours:
                df_area = cv2.contourArea(df_c)
                df_areas.append(df_area)
            max_dfsq = np.argmax(df_areas)
            defocus_cnt = df_contours[max_dfsq]
        # 找出最大轮廓最为光区
        areas = []
        for c in contours:
            area = cv2.contourArea(c)
            areas.append(area)
        max_sq = np.argmax(areas)
        cnt = contours[max_sq]
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"]+float("1e-8"))
        cY = int(M["m01"] / M["m00"]+float("1e-8"))
        tz_center = tuple([cX, cY])
        tz_center
        if self.defocus == True:
            return im_center, tz_center, cnt, defocus_cnt
        else:
            return im_center, tz_center, cnt

    def decentration_cal(self):
        # 计算偏心度
        if self.defocus == True:
            im_center, tz_center, _, df_ = self.centers_cal()
        else:
            im_center, tz_center, _ = self.centers_cal()
        t_x = tz_center[0] - im_center[0]
        t_y = -(tz_center[1] - im_center[1])
        dist = np.sqrt(np.square(t_x) + np.square(t_y))
        sin = t_y / dist+float("1e-8")
        # 修正sin确保范围在-1~1之间
        if 1.0 < sin:
            sin = 1.0
        theta = np.abs(np.rint(np.degrees(np.arcsin(sin))))
        # 象限判定
        if t_x >= 0 and t_y >= 0:
            alpha = theta
        elif t_x < 0 and t_y >= 0:
            alpha = 180 - theta
        elif t_x < 0 and t_y < 0:
            alpha = 180 + theta
        elif t_x >= 0 and t_y < 0:
            alpha = 360 - theta
        # 将结果转换为整数
        res = np.array([np.rint(dist), alpha]).astype("int64")
        return res

    def plot_decentration(self):
        ## 绘制中心点和偏心度
        image = pil2cv(self.image)
        res = image.copy()
        if self.defocus == True:
            im_center, tz_center, cnt, df_cnt = self.centers_cal()
        else:
            im_center, tz_center, cnt = self.centers_cal()
        # 设置中心点颜色，颜色顺序为BGR
        optic_center_color = (0, 255, 0)
        tz_center_color = (255, 0, 0)
        line_color = (255, 255, 255)# 白色
        tz_color = (0, 215, 255)
        df_color = (238, 130, 238)
        point_size = 1
        thickness = 5
        line_size = 1
        font_type = cv2.FONT_HERSHEY_SIMPLEX # 字体
        font_size = 0.3
        font_thickness = 1
        # 绘制线段
        res = cv2.line(res, im_center, tz_center, line_color, line_size)
        # 绘制图片中心点
        res = cv2.circle(res, im_center, point_size, optic_center_color, thickness)
        # 绘制治疗区中心
        res = cv2.circle(res, tz_center, point_size, tz_center_color, thickness)
        # 绘制光区边缘和离焦环边缘
        area = int(cv2.contourArea(cnt))
        res = cv2.drawContours(res, [cnt], -1, tz_color, 2)
        if self.defocus == True:
            df_area = int(cv2.contourArea(df_cnt))
            res = cv2.drawContours(res, [df_cnt], -1, df_color, 2)
        else:
            pass
        # 添加文字
        if im_center[1] > tz_center[1]:
            res = cv2.putText(res, "Optic Center", (im_center[0] - 30, im_center[1] + 20), font_type, font_size, (255, 255, 255), font_thickness)
            res = cv2.putText(res, "TZ Center", (tz_center[0] - 20, tz_center[1] - 20), font_type, font_size, (255, 255, 255), font_thickness)
        else:
            res = cv2.putText(res, "Optic Center", (im_center[0] - 30, im_center[1] - 20), font_type, font_size, (255, 255, 255), font_thickness)
            res = cv2.putText(res, "TZ Center", (tz_center[0] - 20, tz_center[1] + 20), font_type, font_size, (255, 255, 255), font_thickness)
        # 添加偏心率面积
        decentration = self.decentration_cal()
        if units_setting == True:
            decent_len = np.round(decentration[0] / length_unit, 2)
            decent_angle = decentration[1]
            tzarea = np.round(area / square_unit, 2)
            decent_str = f"Decentration: {decent_len} mm @ {decent_angle}"
            tz_area = f"TZ Area: {tzarea} mm^2"
        elif units_setting == False:
            decent_len = decentration[0]
            decent_angle = decentration[1]
            tzarea = area
            decent_str = f"Decentration: {decent_len} pxs @ {decent_angle}"
            tz_area = f"TZ Area: {tzarea} pxs"
        if self.defocus == True:
            if units_setting == True:
                dfarea = np.round((df_area - area) / square_unit, 2)
                df_area_text = f"PSZ Area: {dfarea} mm^2"
                # 根据tag判断是否添加左上角标注
                if self.tag:
                    res = cv2.rectangle(res, (0, 0), (250, 45), (255, 255, 255), -1)
                    res = cv2.circle(res, (210, 3), 2, (0, 0, 0), 1)
            elif units_setting == False:
                dfarea = df_area - area
                df_area_text = f"PSZ Area: {dfarea} pxs"
                if self.tag:
                    res = cv2.rectangle(res, (0, 0), (220, 45), (255, 255, 255), -1)
                    res = cv2.circle(res, (200, 3), 2, (0, 0, 0), 1)
            if self.tag:
                res = cv2.putText(res, df_area_text, (15, 40), font_type, 0.38, df_color, 1)
            # 返回面积和偏心率
            decent_area = [decent_len, decent_angle, tzarea, dfarea]
        else:
            if self.tag:
                res = cv2.rectangle(res, (0, 0), (220, 30), (255, 255, 255), -1)
            # 返回面积和偏心率
            decent_area = [decent_len, decent_angle, tzarea]
        if self.tag:
            res = cv2.putText(res, decent_str, (15, 10), font_type, 0.38, (0, 0, 0), 1)
            res = cv2.putText(res, tz_area, (15, 25), font_type, 0.38, tz_color, 1)
        # 最后转化为Image格式
        res = cv2pil(res)
        return res, decent_area