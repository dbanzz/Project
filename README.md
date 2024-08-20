# Using deep learning to measure stem length from images 

This repository is the further applications and improved version for the paper [A deep learning-based approach for high throughput plant phenotyping, 
Dobos et al.](http://www.plantphysiol.org/content/181/4/1415). 

[The image datasets used in the project can be found at this page](https://drive.google.com/drive/folders/1ysAulbQ1Lj0XKlTA5YLSI9xKnl1tPXid?usp=drive_link).

[The previous research pretrained model used in the project can be downloaded here.](https://drive.google.com/open?id=1SlUui64l-k63vxysl0YAflKaECfpj8Rr)
[The final model of this project can be downloaded here.](https://drive.google.com/file/d/1z3pDonZzANgknQZ17vv6HgAUnmmKue3z/view?usp=drive_link)
For details on how to generate training and validation dataset and how to train the model, please refer to the detailed introduction provided in previous research, which can be viewed from the following link.(https://github.com/biomag-lab/hypocotyl-UNet)
## Contents
- [Newly added code in the project](#intro)
- [Method for processing images for measurement](#processing)
- [Method for measuring the true length of plant stems](#measuring)

## Newly added code in the project <a name="intro"></a>
# train.py:
Basically the same as the initial version
# measure.py(new version): 
Compared with the initial version, the application of thresholds has been increased, and a complete measurement prediction is performed for each set threshold.
# draw_roc_total.py: 
This is a code that visualizes the data generated in measure.py, and finally generates a model to identify plants in the data.
# draw_roc_sameday.py:
This is a code that visualizes the data generated in measure.py. It will eventually generate a model to identify plants in the data. The difference from the above is that the data used is different. The data used here is the plant data of the same day.
# draw_scatter.py:
This is a code that compares the model's predicted results when measuring plant stem length with the actual stem length, and calculates the corresponding R-squared value and MSE value.
# bar.py:
This is a code that visualizes the R-squared and MSE values ​​obtained in draw_scatter
# src/unet/utils.py:
In this code, the metrics for evaluating model performance are expanded to include accuracy, precision, and recall.

