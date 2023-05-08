import gradio as gr
import time
import cv2
import numpy as np
import pandas as pd
import os
from PIL import Image
import threading
import webbrowser

from segformer import SegFormer_Segmentation

root_path = os.path.abspath('.')
dir_input_path = os.path.join(root_path, "img")
dir_pupil_path = os.path.join(dir_input_path, "pupil_radius.xlsx")

def open_webpage():
    webbrowser.open("http://127.0.0.1:7860/")  # 使用默认端口 7860

def detect(input_img, is_dir, pupil, dir_origin_path, pupil_r, mix_type_3=True, output_path="outputs/"):
    segformer = SegFormer_Segmentation()
    #----------------------------------------------------------------------------------------------------------#
    #   mode用于指定测试的模式：
    #   'predict'           表示单张图片预测，如果想对预测过程进行修改，如保存图片，截取对象等，可以先看下方详细的注释
    #   'dir_predict'       表示遍历文件夹进行检测并保存。默认遍历img文件夹，保存img_out文件夹，详情查看下方注释。
    #----------------------------------------------------------------------------------------------------------#
    if is_dir:
        mode = "dir_predict"
    else:
        mode = "predict"    
    #----------------------------------------------------------------------------------------------------------#
    #   pupil用于指定检测瞳孔与TZ和PSZ的相交面积，如果为True则
    #----------------------------------------------------------------------------------------------------------#
    if pupil:
        if is_dir:
            radius_table = pd.read_excel(pupil_r)
            radius_table = radius_table.set_index('file_name')
        else:
            try:
                radius = float(pupil_r)
            except:
                raise AttributeError("Pupil radius must be a number.")
    else:
        radius = None
    #-------------------------------------------------------------------------#
    #   count               指定了是否进行目标的像素点计数（即面积）与比例计算
    #   name_classes        区分的种类，和json_to_dataset里面的一样，用于打印种类和数量
    #
    #   count、name_classes仅在mode='predict'时有效
    #-------------------------------------------------------------------------#
    count           = True
    name_classes    = ["background", "Treatment_Zone", "Defocus_Ring"]
    #-------------------------------------------------------------------------#
    #   dir_origin_path     指定了用于检测的图片的文件夹路径
    #   dir_save_path       指定了检测完图片的保存路径
    #   
    #   dir_origin_path和dir_save_path仅在mode='dir_predict'时有效
    #-------------------------------------------------------------------------#
    dir_save_path   = os.path.join(root_path, "img_out")

    if mode == "predict":
        while True:
            # 创建新文件名
            target_list = os.listdir(output_path)
            indexes = []
            for i in range(len(target_list)):
                imname, _ = os.path.splitext(target_list[i])
                try:
                    index = int(imname)
                    indexes.append(index)
                except:
                    pass
            try:
                new_name = str(max(indexes)+1) + ".png"
            except:
                new_name = "0.png"
            out_img = os.path.join(output_path, new_name)

            if mix_type_3:
                r_image, _ = segformer.detect_image(input_img, count=count, name_classes=name_classes, r=radius)
            else:
                r_image = segformer.detect_image(input_img, count=count, name_classes=name_classes)
            r_image.save(out_img)
            return r_image, f'Successfully detected, and saved as "{os.path.join(root_path, out_img)}"'
     
    elif mode == "dir_predict":
        from tqdm import tqdm

        img_names = os.listdir(dir_origin_path)
        # 批量检测
        all_decent_areas = []
        for img_name in tqdm(img_names):
            # 导入图片
            if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                # 如果需要检测瞳孔，则先获取每张图片对应的半径信息
                if pupil:
                    radius = radius_table.loc[img_name, 'radius']
                    radius = float(radius)
                else:
                    radius = None
                image_path  = os.path.join(dir_origin_path, img_name)
                image       = Image.open(image_path)
                new_name    = os.path.splitext(img_name)[0] + ".png"
                if mix_type_3:
                    r_image, decent_area= segformer.detect_image(image, r=radius)
                    decent_area.insert(0, img_name)
                    all_decent_areas.append(decent_area)
                else:
                    r_image = segformer.detect_image(image)
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                r_image.save(os.path.join(dir_save_path, new_name))
        # 将列表转为表格
        if mix_type_3:
            dcarea_arr = np.array(all_decent_areas)
            dcarea_df = pd.DataFrame(dcarea_arr)
            if len(dcarea_arr[0]) == 7:
                dcarea_df.columns=["filename", "decent_length", "decent_angle", "TZ_area", "PSZ_area", "TZ_over_Pupil", "PSZ_over_Pupil"]
                dcarea_df.to_excel(os.path.join(dir_save_path, "Dec_Area_Data.xlsx"), index=False)
            elif len(dcarea_arr[0]) == 5:
                dcarea_df.columns=["filename", "decent_length", "decent_angle", "TZ_area", "PSZ_area"]
                dcarea_df.to_excel(os.path.join(dir_save_path, "Dec_Area_Data.xlsx"), index=False)
            else:
                pass
        else:
            pass
        return None, f'Successful detected image, and the results saved in "{dir_save_path}"'

demo = gr.Interface(
    fn=detect,
    inputs=[gr.Image(type='pil', label="Input Image"),
            gr.Checkbox(label="Batch Detection"), 
            gr.Checkbox(label="Pupil Overlap (can only be enabled when the unit file generated correctly)"), 
            gr.Textbox(dir_input_path, label="Batch Detection Input Directory"),
            gr.Textbox(label="Pupil Overlap Input (number / path)", 
                       info='- Single detection: Please input radius value (example: 2.5). \n'
                            f'- Batch detection: Please input the absolute path of the table contained image name and radius data (example: {dir_pupil_path}).')],
    outputs=[gr.Image(type='pil', label="Output Image"), 
             gr.Text(label="Output images saving path")],
    title="OKseg: Automatic detection model for Treatment Zone and Peripheral Steepened Zone after Orthokeratology Treatment",
    allow_flagging="never"
    )

threading.Timer(3, open_webpage).start()  # 延迟 3 秒打开浏览器
demo.launch()