import os
import numpy as np
import pprint
import torch
from utils.hgnet.model import KFSGNet
from utils.hgnet.utils import get_device, get_peak_points
from tqdm import tqdm
from torch.autograd import Variable
from torchvision import transforms
from PIL import Image, ImageDraw

pred_configs = {
    "model_path": "utils/hgnet/model.ckpt",
    "mode": "coordinate", # mode包括image, coordinate和r_coordinate3种，其中r_coordinate为相对坐标
    "input_shape": (256, 256),
    "device": get_device()
}

# 定义预测函数
def predict(img, model, mode=pred_configs["mode"], device=pred_configs["device"], input_shape=pred_configs["input_shape"]):
    """预测函数"""
    #---------------------------------------------------#
    #   导入并预处理图片
    #---------------------------------------------------#
    origin_image = img
    image = origin_image.copy()
    iw, ih = image.size
    h, w = input_shape
    scale = min((w/iw, h/ih))
    nw = int(iw * scale)
    nh = int(ih * scale)
    # 添加灰条
    image = image.resize((nw, nh), Image.Resampling.BICUBIC)
    new_image = Image.new('RGB', [w, h], (128, 128, 128))
    new_image.paste(image, ((w-nw)//2, (h-nh)//2))
    # 转化为tensor
    image = np.array(new_image, np.uint8)
    arr2tensor = transforms.ToTensor()
    image = arr2tensor(image)
    # 添加batchsize维度
    image = image.unsqueeze(0)
    #---------------------------------------------------#
    #   预测过程
    #---------------------------------------------------#
    image = Variable(image).to(device)
    model.eval()
    with torch.no_grad():
        output = model(image)
    peak_point = get_peak_points(output.cpu().data.numpy())
    coor = (int(peak_point[0][0]), int(peak_point[0][1]))
    orig_x = coor[0] - (w-nw)//2
    orig_y = coor[1] - (h-nh)//2
    coor = (int(orig_x), int(orig_y))
    orig_ann = (orig_x / nw, orig_y / nh)
    # 根据模式导出结果
    if mode == "coordinate":
        orig_coor = (int(orig_ann[0] * iw), int(orig_ann[1] * ih))
        return orig_coor
    elif mode == "r_coordinate":
        return orig_ann
    elif mode == "image":
        result = (int(orig_ann[0] * iw), int(orig_ann[1] * ih))
        draw = ImageDraw.Draw(origin_image)
        p1 = np.array(result) - 3
        p2 = np.array(result) + 3
        draw.ellipse(((p1[0], p1[1]), (p2[0], p2[1])), fill = (255, 255, 255), outline = None)
        return origin_image
    else:
        raise AttributeError(f"The mode must be one of 'image' or 'coordinate' or 'r_coordinate', Received unexpected mode: '{mode}'")

# 调用函数
if __name__ == '__main__':
    pprint.pprint(pred_configs)
    while True:
        img_path = input("Input image file path:")
        # 模型预测
        try:
            img = Image.open(img_path)
        except:
            print("Open File Error, check the file name and try again!")
            continue
        else:
            output = predict(
                img=img,
                mode=pred_configs["mode"],
                device=pred_configs["device"],
                input_shape=pred_configs["input_shape"],
            )
            if pred_configs["mode"] == "image":
                output.show()
            if pred_configs["mode"] == "coordinate":
                print(output)
            if pred_configs["mode"] == "r_coordinate":
                print(output)