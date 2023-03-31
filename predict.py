#----------------------------------------------------#
#   将单张图片预测、摄像头检测和FPS测试功能
#   整合到了一个py文件中，通过指定mode进行模式的修改。
#----------------------------------------------------#
import time

import cv2
import numpy as np
import pandas as pd
import os
from PIL import Image

from segformer import SegFormer_Segmentation

if __name__ == "__main__":
    #-------------------------------------------------------------------------#
    #   如果想要修改对应种类的颜色，到generate函数里修改self.colors即可
    #-------------------------------------------------------------------------#
    segformer = SegFormer_Segmentation()
    #----------------------------------------------------------------------------------------------------------#
    #   mode用于指定测试的模式：
    #   'predict'           表示单张图片预测，如果想对预测过程进行修改，如保存图片，截取对象等，可以先看下方详细的注释
    #   'dir_predict'       表示遍历文件夹进行检测并保存。默认遍历img文件夹，保存img_out文件夹，详情查看下方注释。
    #----------------------------------------------------------------------------------------------------------#
    mode = "dir_predict"
    #-------------------------------------------------------------------------#
    #   mix_type_3          图片输出类型是否为3，即边缘检测和返回偏心率及面积,需要同步修改segformer.py中的mix_type参数
    #-------------------------------------------------------------------------#
    mix_type_3 = True
    #-------------------------------------------------------------------------#
    #   count               指定了是否进行目标的像素点计数（即面积）与比例计算
    #   name_classes        区分的种类，和json_to_dataset里面的一样，用于打印种类和数量
    #
    #   count、name_classes仅在mode='predict'时有效
    #-------------------------------------------------------------------------#
    count           = True
    name_classes    = ["background", "Treatment_Zone", "Defocus_Ring"]
    # name_classes    = ["background","cat","dog"]
    #-------------------------------------------------------------------------#
    #   dir_origin_path     指定了用于检测的图片的文件夹路径
    #   dir_save_path       指定了检测完图片的保存路径
    #   
    #   dir_origin_path和dir_save_path仅在mode='dir_predict'时有效
    #-------------------------------------------------------------------------#
    dir_origin_path = "img"
    dir_save_path   = "img_out"
    #-------------------------------------------------------------------------#
    #   simplify            使用Simplify onnx
    #   onnx_save_path      指定了onnx的保存路径
    #-------------------------------------------------------------------------#
    simplify        = True
    onnx_save_path  = "model_data/models.onnx"

    if mode == "predict":
        '''
        predict.py有几个注意点
        1、该代码无法直接进行批量预测，如果想要批量预测，可以利用os.listdir()遍历文件夹，利用Image.open打开图片文件进行预测。
        具体流程可以参考get_miou_prediction.py，在get_miou_prediction.py即实现了遍历。
        2、如果想要保存，利用r_image.save("img.jpg")即可保存。
        3、如果想要原图和分割图不混合，可以把blend参数设置成False。
        4、如果想根据mask获取对应的区域，可以参考detect_image函数中，利用预测结果绘图的部分，判断每一个像素点的种类，然后根据种类获取对应的部分。
        seg_img = np.zeros((np.shape(pr)[0],np.shape(pr)[1],3))
        for c in range(self.num_classes):
            seg_img[:, :, 0] += ((pr == c)*( self.colors[c][0] )).astype('uint8')
            seg_img[:, :, 1] += ((pr == c)*( self.colors[c][1] )).astype('uint8')
            seg_img[:, :, 2] += ((pr == c)*( self.colors[c][2] )).astype('uint8')
        '''
        while True:
            img = input('Input image filename:')
            # 设置文件导出路径和导出文件名，这里将后缀改为了png格式
            _, imname = os.path.split(img)
            imname, _ = os.path.splitext(imname)
            new_name = imname + ".png"
            out_img = os.path.join("outputs/", new_name)
            try:
                image = Image.open(img)
            except:
                print('Open Error! Try again!')
                continue
            else:
                if mix_type_3:
                    r_image, _ = segformer.detect_image(image, count=count, name_classes=name_classes)
                else:
                    r_image = segformer.detect_image(image, count=count, name_classes=name_classes)
                r_image.save(out_img)
                r_image.show()
     
    elif mode == "dir_predict":
        import os
        from tqdm import tqdm

        img_names = os.listdir(dir_origin_path)
        all_decent_areas = []
        for img_name in tqdm(img_names):
            if img_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                image_path  = os.path.join(dir_origin_path, img_name)
                image       = Image.open(image_path)
                if mix_type_3:
                    r_image, decent_area= segformer.detect_image(image)
                    decent_area.insert(0, img_name)
                    all_decent_areas.append(decent_area)
                else:
                    r_image = segformer.detect_image(image)
                if not os.path.exists(dir_save_path):
                    os.makedirs(dir_save_path)
                r_image.save(os.path.join(dir_save_path, img_name))
        # 将列表转为表格
        if mix_type_3:
            dcarea_arr = np.array(all_decent_areas)
            dcarea_df = pd.DataFrame(dcarea_arr)
            if len(dcarea_arr[0]) == 5:
                dcarea_df.columns=["filename", "decent_length", "decent_angle", "TZ_area", "PSZ_area"]
                dcarea_df.to_excel(os.path.join(dir_save_path, "Dec_Area_Data.xlsx"), index=False)
            elif len(dcarea_arr[0]) == 4:
                dcarea_df.columns=["filename", "decent_length", "decent_angle", "TZ_area"]
                dcarea_df.to_excel(os.path.join(dir_save_path, "Dec_Area_Data.xlsx"), index=False)
            else:
                pass
        else:
            pass
    elif mode == "export_onnx":
        segformer.convert_to_onnx(simplify, onnx_save_path)
        
    else:
        raise AssertionError("Please specify the correct mode: 'predict' or 'dir_predict'.")
