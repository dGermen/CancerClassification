# CancerClassification
Classifies the tumor as malignant or benign.
2020 - July
---
This project was coded for BIN500 course in METU. Main goal of the code is to differenciate between a malignant and benign tumor by looking it at the tumor's physical properties.

First it finds the average properties of the known tumor for per class, then these learned averages are used to decide on a tumor's status. Classes' properties' averages are averaged again to find the mid-points. 

For an unknown tumor, each of the properties are compared to mid points. Whichever average is closest for the property that property's result is labeled as that class. After all properties of the unknown tumor is labeled, scores are summed up and the class with highest score (or a predetermined threshold) is decided as the unknown tumor's class. 

## Tasks

Train the classifier by feeding known tumors. Essentially, finding averages per class.

Application of the classifier and reporting the accuracy.

Outouts results, showing statistical information per class per property. Display patient's properties and classifier results with supplied patient ID.

Take input for a new patient.

Generate new data according to found statistical values.

## Sample Outputs

Starting the program

![alt text](https://raw.githubusercontent.com/dGermen/CancerClassification/main/Screen%20Shot%202022-09-10%20at%2015.13.55.png)

Results for patient id of 922840.

![alt text](https://github.com/dGermen/CancerClassification/blob/main/Screen%20Shot%202022-09-10%20at%2015.15.06.png?raw=true)
