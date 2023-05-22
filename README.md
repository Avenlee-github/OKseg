## OKseg: Automatic Dtection Model for Treatment Zone and Peripheral Steepened Zone after Orthokeratology Treatment Based on Segformer
  <img src=".\figures\okseg_logo.png" alt="logo" style="zoom:7%;" />
---

### Catalogue
1. [Installment](#Installment)
2. [Preparation](#Preparation)
3. [GUI_Utilization](#GUI_Utilization)
4. [Weights](#Weights)
5. [Configuration](#Configuration)
6. [Declaration](#Declaration)
7. [Reference](#Reference)

## Installment 
### Stable Version
This version provides a virtual environment for the program, which has been contained in the <font color=#FFFF00>***"venv.rar"***</font> file.

1. Please ensure that Python 3 has been installed on your computer (and has been set in System Path).
2. Clone or donwload the <font color=#FFFF00>***"stable"***</font> branch to your computer/device.

  <img src=".\figures\stable_shift.png" alt="stable" style="zoom:40%;" />

3. Please extract the contents of <font color=#FFFF00>***"venv.rar"***</font> in the current folder and ensure that the <font color=#FFFF00>***"venv"***</font> folder is correctly present in the program folder. Since <font color=#FFFF00>***"venv.rar"***</font> is a split volume compression, please decompress all <font color=#FFFF00>***"venv.part0*.rar"***</font> after downloading.
4. The <font color=#FFFF00>***"venv"***</font> folder should contain the "include", "Lib", "Scripts", and "share" folders, as well as the "pyvenv.cfg" file.

### Main Branch Version
This version dosen't provide virtual environment for the program, and the environment could be set up by following steps:

1. Please ensure that Python 3 has been installed on your computer (and has been set in System Path).
2. Clone or donwload the <font color=#FFFF00>***"main"***</font> branch to your computer/device.

  <img src=".\figures\main_shift.png" alt="stable" style="zoom:40%;" />

3. Open the Powershell or Command Line Interface;
4. Enter the OKseg directory and use the <font color=#FFFF00>***"installment.py"***</font> to set up the environment for OKseg:
```cmd
cd your_path/OKseg
python installment.py
```
5. Environment requist: **"python>=3.7.0"**, **"torch>=1.12.0"** and **"opencv-python>=4.6.0"**

## Preparation
The model requires following setting:
1. Weight file: The model needs to load a weight file for prediction. All weight files are stored in the <font color=#FFFF00>***"model_data"***</font> folder. To load the corresponding weight file during runtime, rename the weight file you want to load as <font color=#FFFF00>***"model.pth"***</font>. When modifying the weight file, you also need to modify the ***"phi"*** parameter in the <font color=#FFFF00>***"segformer.py"***</font> file to the corresponding backbone of the weight file. For example, if the weight file is named <font color=#FFFF00>***"b1_weights.pth"***</font>, modify it to ***"b1"***. By default, the value is ***"b0"***, and the weight file in the <font color=#FFFF00>***"model_data/"***</font> folder is also "b0" by default.

2. Unit file: Due to the inability of the Medmont Topographer to export topography files of the same size, this experiment uses cropped topography images for training. Therefore, when exporting prediction results, different devices may have different image sizes, so it is necessary to first obtain a grid screenshot without color topography (as shown in the <font color=#FFFF00>***"metric.png"***</font> image in the <font color=#FFFF00>***"utils/metric/"***</font> folder, see following figure), and use the same screenshot captured on the computer connected to the topographer for calculation. After obtaining the image, replace <font color=#FFFF00>***"metric.png"***</font> file in the <font color=#FFFF00>***"utils/metric/"***</font> folder. During usage, a <font color=#FFFF00>***"units.py"***</font> file will be automatically generated in the <font color=#FFFF00>***"utils/"***</font> folder, which contains the pixel values corresponding to each millimeter and square millimeter. If the <font color=#FFFF00>***"metric.png"***</font> file is not available, the output image will be in pixel units for distance and area.

   <img src=".\utils\metric\metric.png" alt="metric" style="zoom:20%;" />

3. Image preparation: The images were captured using the computer's built-in screenshot tool and saved as screenshots of the topography to be detected. Save the images to be detected in the <font color=#FFFF00>***"img/images/"***</font> folder (customized path is available). The image formats of ***".png"*** and ***".jpg"*** are allowed for the model.

4. Make sure that all of the previous prediction result files have been cleared from the <font color=#FFFF00>***"img_out/"***</font> folder.

## GUI_Utilization
1. **Running the Model:** We provide a GUI interface to facilitate the user's invocation of the model. By double clicking on the <font color=#FFFF00>***"OK-Detection.bat"***</font> file, the model can be run, and by accessing [**http://127.0.0.1:7860**](http://127.0.0.1:7860/), the GUI interface (shown in the figure below) can be opened.
  
  <img src=".\figures\GUI.png" alt="GUI" style="zoom:40%;" />

2.  **Single Image Detection:** Drag the image into the ***"Input Image"*** column on the left-hand side of the GUI interface, then simply click the ***"Submit"*** button below to run the detection. The output results will be displayed in the ***"Output Image"*** column on the right-hand side, and the saving path will be shown in the ***"Output images saving path"*** column below on the right-hand side.

  <img src=".\figures\single_detection.png" alt="Single Detection" style="zoom:40%;" />

3. **Batch Detection:** Batch detection can be achieved by checking the ***"Batch Detection"*** option on the right-hand side. Enter the directory path where the images to be detected are located in the ***"Batch Detection Input Directory"*** section below it. Click the ***"Submit"*** button below to automatically batch detect the images. The detection results will be saved in the path indicated in the ***"Output images saving path"*** column on the right-hand side.

  <img src=".\figures\batch_detection.png" alt="Batch Detection" style="zoom:40%;" />

4. **Untagged images:** If you need to export untagged images without the label in the top left corner, set the ***"tag"*** parameter in the ***"segformer.py"*** file to ***"False"***.

  <img src=".\figures\comparison.png" alt="Comparison" style="zoom:20%;" />

5. **Pupil Overlap Mode:** If you want to acquire the overlaped area of Pupil with Treatment Zone or Peripheral Steepened Zone, please enable the "Pupil Overlap" button. The single image detection and batch detection mode were show in follow image, and the pupil radius is required for overlap area calculation.

  <img src=".\figures\single_pupil_detection.png" alt="Single Pupil Detection" style="zoom:40%;" />

  The following image show the Batch Pupil Overlap Detection mode, and the pupil radius data are required and formated as .xlsx table (an example file could be found in <font color=#FFFF00>***"img/pupil_radius.xlsx"***</font>), and the absolute path for the table file should be provided.

  <img src=".\figures\batch_pupil_detection.png" alt="Batch Pupil Detection" style="zoom:40%;" />

And the following image show the comparison of normal detection result and pupil overlap detection result.

  <img src=".\figures\pupil_overlap_comparison.png" alt="Pupil Overlap Comparison" style="zoom:20%;" />

## Weights
All trained model information can be obtained by contacting the author. The weight file for the built-in "backbone 0" is included in the repository (<font color=#FFFF00>***"model_data/model.pth"***</font>).

## Configuration
Here are some parameter settings in <font color=#FFFF00>***"segformer.py"***</font>, but it is recommended to only modify the ***"phi", "cuda", and "tag"*** parameters based on your computer's actual situation:
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