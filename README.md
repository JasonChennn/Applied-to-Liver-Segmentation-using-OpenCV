# Abstract

*   The research mainly used liver volume to calculate with image post-processing algorithms. Accurate prediction is the key to improving the efficacy of liver transplantation and enabling the fair and reasonable application of liver resources. It is generally believed that the remaining liver volume needs to account for more than 40% of the standard liver volume (cirrhosis) or more than 30% of the standard liver volume (without cirrhosis) as a necessary condition for resection. In the medical images of the liver, there are differences due to different ages, body types, genders, etc., but these liver images have similar gray value ranges. The image post-processing algorithm is used to calculate, from the DICOM file; The image acquisition parameters to calculate the liver volume. Liver volume assessment information will enable more liver cancer and other patients benefiting from liver transplant surgery is a very important reference.

*   For the liver volume of liver transplant patients, the post-image processing algorithm is used to calculate the DICOM image file scanned by the medical equipment. The purpose is to segment all organs in the DICOM image file by this system. Identify, and finally produce the required organ model to assist doctors in medical diagnosis as an auxiliary tool to diagnose the condition, which has an indispensable influence on patients or doctors. The volume data is a very important reference for evaluating liver transplantation, especially for patients with small liver cancer who have a background of decompensated cirrhosis and are not suitable for resection. Obtain liver volume data of liver transplant patients, and achieve results similar to or even more accurate with semi-manual or automated circle selection.

# Introduction
 
*   In modern society, the development of science and technology has gradually progressed faster and faster over time, and new technologies are changing with each passing day; How to solve many problems in life,the scope of science and technology can help is quite wide, it is an inalienable part of the inviolable territory. In order to improve people's quality of life, human beings are constantly innovating in computer vision, which has resulted in the rapid development of algorithm program. In the medical industry, Image Processing have also greatly improved medical technology. Diagnosing patients medically is not only more convenient, but the most important thing, is to improve the quality of medical care, and thus benefit society.

*   The development of medical technology nowadays is very different from that in the past. Early doctors made judgments based on the skills and experience. They learned in the past. However, with the advancement of science and technology, doctors in addition to their own skills , It can also use technology to assist its diagnosis, and it can also reduce the occurrence of misjudgments.
   
*   In the early days of medical treatment, the scanned negatives were washed out for diagnosis when doing any medical scan, but only a single negative and the doctor’s personal experience were used to make judgments. This misjudgment rate was higher than that of modern image digitization. After the image is digitized, the negative film step can be omitted. After the patient has completed X-ray photography or tomography, the photography results will be immediately displayed on the computer screen, and the physician can simulate the required 3D model of the organ. For the physician's auxiliary judgment in medical treatment.


# Proposed Method

*    The purpose of this system is to identify DICOM images in a semi-automated manner, calculate the patient’s liver volume, there by eliminating the time spent in manual circle selection, and providing physicians to build a 3D liver model so that the physician can confirm the patient’s liver shape and Whether the appearance is correct or reasonable.
 
*    To read DICOM medical images into this system, we have set a preset threshold in gray image. The physician can first see which slice image is the correct preset circle, and then let the system follow the dynamic programming of DICOM images one by one Circle the liver area and calculate the area of the liver in this image at the same time. After each image is calculated, the circled area will be displayed, and the doctor can also confirm whether the circled area is correct. After discussing and confirming with the doctor, the circle selection speed of this system is about five times faster than manual selection . Therefore, if the accuracy is stable, it can be of great help in the evaluation of the volume of liver surgery and can also reduce the evaluation of surgery. Time to improve medical quality.

# Experiment Result
* If you want to watch full version,please visit to our video connection below: 
*     https://www.youtube.com/watch?v=Tektj0gkPww
![image](https://i.imgur.com/Kjxc7AQ.png) ![image](https://i.imgur.com/3itmM32.png)

# Source Code
* If you have interested in it, please send a email to me; I am very honored to share and communicate with you for academic research.
*     Contact us for email address: M10915047@mail.ntust.edu.tw

# References
* MRI image data source from: 
*     Far Eastern Hospita, New Taipei City, Taiwan.
