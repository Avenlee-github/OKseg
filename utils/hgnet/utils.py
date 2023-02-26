import numpy as np
import cv2
import torch
from torch import nn
from PIL import Image
from torch.autograd import Variable

"""This file defined some assisted function"""

def cv2pil(img):
    """将opencv转化为PIL格式"""
    image = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
    return image

#-----------------------------------#
#   训练相关辅助函数
#-----------------------------------#
def get_device():
    """检查是否有可用的GPU"""
    return 'cuda' if torch.cuda.is_available() else 'cpu'

def get_peak_points(heatmaps):
    """
    :param heatmaps: numpy array (N,1,256,256)
    :return:numpy array (N, 2) # 
    """
    N,C,H,W = heatmaps.shape   # N= batch size C=4 hotmaps
    all_peak_points = []
    for i in range(N):
        yy,xx = np.where(heatmaps[i,0] == heatmaps[i,0].max())
        y = yy[0]
        x = xx[0]
        peak_point = [x, y]
        all_peak_points.append(peak_point)
    all_peak_points = np.array(all_peak_points)
    return all_peak_points

def get_mse(pred_points,gts,indices_valid=None):
    """
    :param pred_points: numpy (N,4,2)
    :param gts: numpy (N,4,2)
    :return:
    """
    pred_points = pred_points[indices_valid,:]
    gts = gts[indices_valid,:]
    pred_points = Variable(torch.from_numpy(pred_points).float(),requires_grad=False)
    gts = Variable(torch.from_numpy(gts).float(),requires_grad=False)
    criterion = nn.MSELoss()
    loss = criterion(pred_points,gts)
    return loss

# 计算mask ？？ 
def calculate_mask(heatmaps_targets):
    """
    :param heatmaps_target: Variable (N,4,256,256)
    :return: Variable (N,4,256,256)
    """
    N,_,_,_ = heatmaps_targets.size()  #N =8 C = 1
    N_idx = []
    # C_idx = []
    for n in range(N):      # 0-7
        max_v = heatmaps_targets[n,0,:,:].max().item()
        if max_v != 0.0:
            N_idx.append(n)
            # C_idx.append(0)
    mask = Variable(torch.zeros(heatmaps_targets.size()))
    mask[N_idx, 0,:,:] = 1.0
    mask = mask.float().cuda()
    return mask,N_idx
