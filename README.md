## OKseg: Automatic Dtection Model for Treatment Zone and Peripheral Steepened Zone after Orthokeratology Treatment Based on Segformer
  <img src=".\figures\okseg_logo.png" alt="logo" style="zoom:5%;" />
---

### Catalogue
1. [Installment](#Installment)
2. [Preparation](#Preparation)
3. [GUI_Utilization](#GUI_Utilization)
4. [Declaration](#Declaration)
5. [Acknowledgments](#Acknowledgments)
6. [Reference](#Reference)

## Installment 
1. Please ensure that Python 3 (**"python>=3.7.0"**) has been installed on your computer (and has been set in System Path).
2. Clone or donwload the <font color=#FFFF00>***"main"***</font> repository to your computer/device.

  <img src=".\figures\download_page.png" alt="stable" style="zoom:40%;" />

3. Open the Powershell or Command Line Interface;
4. Enter the OKseg directory and use the <font color=#FFFF00>***"installment.py"***</font> to set up the environment for OKseg:
```cmd
cd your_path/OKseg
python installment.py
```

## Preparation
The model requires 3 files and 1 folder listed following:
1. Weight file: The model needs to load a weight file for prediction. All weight files ahould be put in the <font color=#FFFF00>***"model_data"***</font> folder, and there are a default weight file named <font color=#FFFF00>***"model_b0.pth"***</font>. More weight files can be acquired by contacting the author.

2. Unit file: Due to the inability of the Medmont Topographer to export topography files of the same size, this experiment uses cropped topography images for training. Therefore, when exporting prediction results, different devices may have different image sizes, so it is necessary to first obtain a grid screenshot without color topography (as shown in the <font color=#FFFF00>***"metric.png"***</font> image in the <font color=#FFFF00>***"utils/metric/"***</font> folder, see following figure), and use the same screenshot captured on the computer connected to the topographer for calculation. If the Unit file is not available, the output image will be in pixel units for distance and area.

   <img src=".\utils\metric\metric.png" alt="metric" style="zoom:40%;" />

3. Image preparation: The images were captured using the computer's built-in screenshot tool and saved as screenshots of the topography to be detected. Save the images to be detected in the <font color=#FFFF00>***"img/images/"***</font> folder for batch detection (customized path is also available). The image formats of ***".png"*** and ***".jpg"*** are allowed for the model.

4. Make sure that all of the previous prediction result files have been cleared from the <font color=#FFFF00>***"img_out/"***</font> folder.

## GUI_Utilization
1. **Running the Model:** We provide a GUI interface to facilitate the user's invocation of the model. By double clicking on the <font color=#FFFF00>***"OK-Detection.bat"***</font> file, the model can be run, and by accessing [**http://127.0.0.1:7860**](http://127.0.0.1:7860/), the GUI interface (shown in the figure below) can be opened.
  
  <img src=".\figures\GUI.png" alt="GUI" style="zoom:40%;" />

2. **Model weight loading:** 
- Select the model checkpoint file from the available options.
- Choose the network backbone (b0, b1, b2, b3).
- Toggle the option to show the tag in the top-left corner of the result image in needed.
- Click the "Load Model" button to load the selected model.
- The following figure shows that the model has been loaded successfully.

  <img src=".\figures\model_loading.png" alt="GUI" style="zoom:40%;" />

3.  **Metric Grid Image Processing:**
- Upload the grid screenshot (shown as metric.png) of the metric grid.
- Click the "Unit Calculation" button to perform unit calculation on the grid image.
- The result of the unit calculation will be displayed.
- The following figure shows that the unit file generated successfully

  <img src=".\figures\metric_unit.png" alt="metric_unit" style="zoom:40%;" />

4.  **Automatic Detection:**
- Upload an input image for cornea topography detection.
- Toggle the option for batch detection if you want to process multiple images in a directory.
- Toggle the option for pupil overlap calculation if needed.
- Provide the pupil radius value or the absolute path of the table containing image names and radius data.
- The detection results savint path will show in the output textbox.
- Click the "Cornea Topography Detection" button to start the detection process.
- The output image with the detected zones will be displayed.
- Single image detection result be like:

  <img src=".\figures\detection_result.png" alt="Single Detection" style="zoom:40%;" />

- The following figure shows the difference between normal detection mode and pupil overlap detection mode.

  <img src=".\figures\pupil_overlap_comparison.png" alt="Pupil Overlap Comparison" style="zoom:17%;" />

- The result tag (located at the top left of the result image) displays the detailed values of the detection results. This tag can be disabled in the model loading block by deselecting the option "Show the tag in the top left of the result image". The following figure illustrates the contrast between tagged and untagged detection results.

  <img src=".\figures\comparison.png" alt="Comparison" style="zoom:20%;" />

## Declaration
This project is for academic use only. The purpose is to explore AI's potential in myopia-related research, and it is not intended for commercial or clinical use. The data used comply with ethical and legal guidelines. This project is not intended to replace professional judgment, and is not certified for clinical use. The results are solely for academic and research purposes and should not inform medical decisions.

## Acknowledgments

- The OKseg model is based on the SegFormer_Segmentation model.
- The Gradio library is used for creating the user interface.

## Reference
- https://github.com/ggyyzm/pytorch_segmentation  
- https://github.com/NVlabs/SegFormer  
- https://github.com/bubbliiiing/segformer-pytorch