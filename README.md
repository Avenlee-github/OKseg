## OKseg: Automatic Dtection Model for Treatment Zone and Peripheral Steepened Zone after Orthokeratology Treatment Based on Segformer
---

### Catalogue
1. [Installment](#Installment)
2. [Preparation](#Preparation)
3. [Utilization](#Utilization)
4. [Weights](#Weights)
5. [Configuration](#Configuration)
6. [Declaration](#Declaration)
7. [Reference](#Reference)

## Installment
1. Please ensure that Python 3 has been installed on your computer.
2. Clone the repository to your computer/device.
3. Open the Powershell or Command Line Interface;
4. Enter the OKseg directory:
```cmd
cd your_okseg_path
```
5. Input command:
```cmd
pip install -r requirements.txt
```
6. Environment requist: **"python>=3.7.0"**, **"torch>=1.12.0"** and **"opencv-python>=4.6.0"**
7. We do recommend using the Anaconda (https://www.anaconda.com/) to deploy a new environment for OKseg.

## Preparation
The model requires following setting:
1. Weight file: The model needs to load a weight file for prediction. All weight files are stored in the "model_data" folder. To load the corresponding weight file during runtime, rename the weight file you want to load as "model.pth". When modifying the weight file, you also need to modify the "phi" parameter in the "segformer.py" file to the corresponding backbone of the weight file. For example, if the weight file is named "b1_weights.pth", modify it to "b1". By default, the value is "b0", and the weight file in the "model_data" folder is also "b0" by default.
2. Unit file: Due to the inability of the Medmont Topographer to export topography files of the same size, this experiment uses cropped topography images for training. Therefore, when exporting prediction results, different devices may have different image sizes, so it is necessary to first obtain a grid screenshot without color topography (as shown in the "metric.png" image in the "utils/metric" folder), and use the same screenshot captured on the computer connected to the topographer for calculation. After obtaining the image, replace "metric.png" file in the "utils/metric" folder, and run the "utils_unitcalc.py" file in the "utils" folder. This will generate a "units.py" file in the "utils" folder, which contains the pixel values corresponding to each millimeter and square millimeter. If the "units.py" file is missing, the length and area of the output prediction results will be in pixel units.
```cmd
cd utils
python utils_unitcalc.py
```
3. Image preparation: The images were captured using the computer's built-in screenshot tool and saved as screenshots of the topography to be detected. Save the images to be detected in the "img/images" folder.
4. Make sure that all of the previous prediction result files have been cleared from the "img_out" folder.

## Utilization
1. General usage: The usage method is to open the command line tool in the main directory and enter:
```cmd
python predict.py
```
The general usage method will predict and segment all images in the "img" folder, and the segmentation results will be exported to the "img_out" folder, including predicted and segmented images, as well as an Excel table file with exported data on the Treatment Zone and Peripheral Steepened Zone.

2. Untagged images: If you need to export untagged images without the label in the top left corner, set the "tag" parameter in the "segformer.py" file to "False".

3. Single Image Segmentation: If you want to perform segmentation prediction for only one image, please set the "mode" parameter in "predict.py" as follows:
```python
mode = "dir_predict"
```
and the segmentation result will be saved in "outputs" folder.

## Weights
All trained model information can be obtained by contacting the author. The weight file for the built-in "backbone 0" is included in the repository ("model_data/model.pth").

## Configuration
Here are some parameter settings in "segformer.py", but it is recommended to only modify the "phi", "cuda", and "tag" parameters based on your computer's actual situation:
```python
_defaults = {
    #-------------------------------------------------------------------#
    #   The "model_path" parameter refers to the weight file in the "logs" folder.
    #-------------------------------------------------------------------#
    "model_path"        : "model_data/model.pth",
    #----------------------------------------#
    #   The number of classes to be distinguished + 1.
    #----------------------------------------#
    "num_classes"       : 3,
    #----------------------------------------#
    #   The backbone network being used is:
    #   b0、b1、b2、b3、b4、b5
    #----------------------------------------#
    "phi"               : "b0",
    #----------------------------------------#
    #   Input image shape
    #----------------------------------------#
    "input_shape"       : [512, 512],
    #-------------------------------------------------#
    #   The "mix_type" parameter is used to control the visualization method of the detection results.
    #
    #   mix_type = 0: Mix the origin image and segmentation result.
    #   mix_type = 1: Only output the segmentation result.
    #   mix_type = 2: exclude the background result.
    #   mix_type = 3: return the image including segmentation, TZ decentration result
    #   In this study we do recommend using the "mix_type = 3" as the default setting in segmentation.
    #-------------------------------------------------#
    "mix_type"          : 3,
    #-------------------------------#
    #   If the device does not have a GPU or is not configured with CUDA, please set it to False here.
    #   Default setting is False
    #-------------------------------#
    "cuda"              : False,
    #-------------------------------#
    #   Add tag on the image topleft cornor if True
    #-------------------------------#
    "tag"               : True,
}
```

## Declaration
This project is for academic use only. The purpose is to explore AI's potential in myopia-related research, and it is not intended for commercial or clinical use. The data used comply with ethical and legal guidelines. This project is not intended to replace professional judgment, and is not certified for clinical use. The results are solely for academic and research purposes and should not inform medical decisions.

## Reference
https://github.com/ggyyzm/pytorch_segmentation  
https://github.com/NVlabs/SegFormer  
https://github.com/bubbliiiing/segformer-pytorch