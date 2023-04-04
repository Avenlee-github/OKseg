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
4. Enter the OKseg directory and use the <font color=#FFFF00>***"installment.py"***</font> to set up the environment for OKseg:
```cmd
cd your_path/OKseg
python installment.py
```
5. Environment requist: **"python>=3.7.0"**, **"torch>=1.12.0"** and **"opencv-python>=4.6.0"**

## Preparation
The model requires following setting:
1. Weight file: The model needs to load a weight file for prediction. All weight files are stored in the <font color=#FFFF00>***"model_data"***</font> folder. To load the corresponding weight file during runtime, rename the weight file you want to load as <font color=#FFFF00>***"model.pth"***</font>. When modifying the weight file, you also need to modify the <font color=#008000>***"phi"***</font> parameter in the <font color=#FFFF00>***"segformer.py"***</font> file to the corresponding backbone of the weight file. For example, if the weight file is named <font color=#FFFF00>***"b1_weights.pth"***</font>, modify it to <font color=#008000>***"b1"***</font>. By default, the value is <font color=#008000>***"b0"***</font>, and the weight file in the <font color=#FFFF00>***"model_data/"***</font> folder is also "b0" by default.
2. Unit file: Due to the inability of the Medmont Topographer to export topography files of the same size, this experiment uses cropped topography images for training. Therefore, when exporting prediction results, different devices may have different image sizes, so it is necessary to first obtain a grid screenshot without color topography (as shown in the <font color=#FFFF00>***"metric.png"***</font> image in the <font color=#FFFF00>***"utils/metric/"***</font> folder), and use the same screenshot captured on the computer connected to the topographer for calculation. After obtaining the image, replace <font color=#FFFF00>***"metric.png"***</font> file in the <font color=#FFFF00>***"utils/metric/"***</font> folder. During usage, a <font color=#FFFF00>***"units.py"***</font> file will be automatically generated in the <font color=#FFFF00>***"utils/"***</font> folder, which contains the pixel values corresponding to each millimeter and square millimeter. If the <font color=#FFFF00>***"metric.png"***</font> file is not available, the output image will be in pixel units for distance and area.
3. Image preparation: The images were captured using the computer's built-in screenshot tool and saved as screenshots of the topography to be detected. Save the images to be detected in the <font color=#FFFF00>***"img/images/"***</font> folder. The image formats of "png" and "jpg" are allowed for the model.
4. Make sure that all of the previous prediction result files have been cleared from the <font color=#FFFF00>***"img_out/"***</font> folder.

## Utilization
1. General usage: We have provided an <font color=#FF000>***"OK-Detection.bat"***</font> file to start the model. After configuring the environment, place the images to be detected in the <font color=#FFFF00>***"img/"***</font> folder. When you run the <font color=#FF000>***"OK-Detection.bat"***</font> file, the model will automatically detect the Treatment Zone and Peripheral Steepened Zone, and save the detected images and the detection results table <font color=#FFFF00>***(Dec_Area_Data.xlsx)***</font> in the <font color=#FFFF00>***"img_out/"***</font> folder.

2. Untagged images: If you need to export untagged images without the label in the top left corner, set the <font color=#008000>***"tag"***</font> parameter in the <font color=#FFFF00>***"segformer.py"***</font> file to <font color=#008000>***"False"***</font>.

3. Single Image Segmentation: If you want to perform segmentation prediction for only one image, please set the <font color=#008000>***"mode"***</font> parameter in <font color=#FFFF00>***"predict.py"***</font> as follow:
```python
mode = "predict"
```
and input commond in Powershell as follow to launch the model:
```cmd
python installment.py
```
and the segmentation result will be saved in <font color=#FFFF00>***"outputs/"***</font> folder.

## Weights
All trained model information can be obtained by contacting the author. The weight file for the built-in "backbone 0" is included in the repository (<font color=#FFFF00>***"model_data/model.pth"***</font>).

## Configuration
Here are some parameter settings in <font color=#FFFF00>***"segformer.py"***</font>, but it is recommended to only modify the <font color=#008000>***"phi", "cuda", and "tag"***</font> parameters based on your computer's actual situation:
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
    #   The default weights in the repository is "b0"
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