import gradio as gr
import time
import cv2
import numpy as np
import pandas as pd
import os
from PIL import Image
import threading
import webbrowser
from utils.utils_unitcalc import unit_cal_ui
from segformer import SegFormer_Segmentation

# 默认路径设置
root_path = os.path.abspath('.')
dir_input_path = os.path.join(root_path, "img")
dir_pupil_path = os.path.join(dir_input_path, "pupil_radius.xlsx")
ckpt_save_dir = "model_data/"

# 获取权重文件夹内文件目录
ckpt_list = []
file_dir = os.listdir(ckpt_save_dir)
for ck in file_dir:
    if os.path.splitext(ck)[-1] == ".pth":
        ckpt_list.append(ck)

# 定义模型加载函数
def model_load(ckpt_path, backbone, tag):
    # 定义一个全局变量方便保存加载好的模型
    global model
    print("Model Loading...")
    pthfile = ckpt_save_dir + ckpt_path
    try:
        model = SegFormer_Segmentation(model_path=pthfile, phi=backbone, tag=tag)
        load_result = "Model Loading Finshed."
    except:
        model = None
        load_result = "Model Loading Failed, please ensure that the weight file and the backbone set crrectly."
    return load_result

# 定义检测函数
def detect(input_img, is_dir, pupil, dir_origin_path, pupil_r, mix_type_3=True, output_path="outputs/"):
    global model
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
                r_image, _ = model.detect_image(input_img, count=count, name_classes=name_classes, r=radius)
            else:
                r_image = model.detect_image(input_img, count=count, name_classes=name_classes)
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
                    r_image, decent_area= model.detect_image(image, r=radius)
                    decent_area.insert(0, img_name)
                    all_decent_areas.append(decent_area)
                else:
                    r_image = model.detect_image(image)
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

app = gr.Blocks()
with app:
    gr.Markdown(value="""
        # OKseg: Automatic detection model for Treatment Zone and Peripheral Steepened Zone after Orthokeratology Treatment

        """)
    # 模型加载部分
    with gr.Row():
        choice_ckpt = gr.Dropdown(label="Model Selection", choices=ckpt_list, value="model_b0.pth")
        ckpt_backbone = gr.Radio(label="Network Backbone", choices=["b0", "b1", "b2", "b3"], value="b0")
        show_tag = gr.Checkbox(value=True, label="Show the tag in the lefttop result image")
    load_result = gr.Textbox(label="Model Loading Result:")
    ckpt_submit = gr.Button("Load Model", variant="primary")

    ckpt_submit.click(model_load, [choice_ckpt, ckpt_backbone, show_tag], [load_result])

    # 网格图像处理
    with gr.Row():
        grid_img = gr.Image(type='pil', label="Metric Grid Image", value="utils/metric/metric.png")
        units_result = gr.Textbox(label="Units Calculation Result")
    unit_calculation = gr.Button("Unit Calculation", variant="primary")

    unit_calculation.click(unit_cal_ui, [grid_img], [units_result])

    # 检测模块
    with gr.Row():
        input_img = gr.Image(type='pil', label="Input Image", value="img/1.jpg")
        output_img = gr.Image(type='pil', label="Output Image")
    with gr.Row():
        input_dir = gr.Textbox(dir_input_path, label="Batch Detection Input Directory")
        output_path = gr.Text(label="Output images saving path")
    gr.Markdown(value=f"""
        ### Pupil Overlap Area Calculation (Test)

        - Single Detection: Please input radius value (example: 2.5).

        - Batch Detection: Please input the absolute path of the table contained image name and radius data (example: {dir_pupil_path}).

        """)
    pupil_radius = gr.Textbox(label="Pupil Overlap Input (number / path)")
    with gr.Row():
        is_batch = gr.Checkbox(label="Batch Detection")
        is_pupil = gr.Checkbox(label="Pupil Overlap")
    img_submit = gr.Button("Cornea Topography Detection", variant="primary")

    img_submit.click(detect, [input_img,is_batch, is_pupil, input_dir, pupil_radius], [output_img, output_path])

    # 服务器运行
    app.queue().launch(server_name="127.0.0.1",inbrowser=True,quiet=True)