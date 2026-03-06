Sleep Breathing Irregularity Detection

Overview
   This project analyzes overnight sleep recordings to detect abnormal breathing events    such as Hypopnea and Obstructive Apnea.

   The workflow includes:
	- Visualization of physiological signals
	- Signal preprocessing and windowing
	- Dataset creation
	- Classification using a 1D Convolutional Neural Network (CNN)
	- Leave-One-Participant-Out cross validation

  The goal is to demonstrate a complete pipeline for detecting breathing irregularities    from sleep recordings.


Dataset Description
    The dataset contains overnight recordings from 5 participants.  
    Each participant includes the following signals:
	- Nasal Airflow (32 Hz)
	- Thoracic Movement (32 Hz)
	- SpO2 (4 Hz)
	- Flow event annotations
	- Sleep profile information

    The event annotations indicate when breathing irregularities occur during sleep.



Project Structure


breathing_project/
¦
+-- scripts/
¦   +-- vis.py
¦   +-- create_dataset.py
¦   +-- train_model.py
¦
+-- Visualizations/
¦   +-- AP01_visualization.pdf
¦   +-- AP02_visualization.pdf
¦   +-- AP03_visualization.pdf
¦   +-- AP04_visualization.pdf
¦   +-- AP05_visualization.pdf
¦
+-- requirements.txt
+-- README.md
+-- report.pdf

Note:  
The dataset files are not included in the repository due to size limitations.



Visualization
   The `vis.py` script generates visualizations of the physiological signals.

    For each participant it plots:
	- Nasal Airflow
	- Thoracic Movement
	- SpO2

    Breathing events are overlaid on the airflow signal.

    The plots are saved as PDF files in the `Visualizations` folder.



Signal Preprocessing
   Respiratory signals were filtered using a Butterworth bandpass filter (0.17–0.4 Hz) to     isolate the breathing frequency range.

   The filtered signals were divided into:
	- 30-second windows
	- 50% overlap

Each window contains 960 samples (30 seconds × 32 Hz).



Window Labeling
   Each window was labeled based on overlap with annotated breathing events.

   If more than 50% of a window overlapped with an event, the window was labeled    with that event type.  
   Otherwise it was labeled as "Normal".

   All windows from the five participants were combined into a single dataset.


Modeling
    A 1D Convolutional Neural Network (CNN) was used to classify breathing patterns.

    Model evaluation was performed using Leave-One-Participant-Out Cross Validation     (LOPO):

	1. Train on 4 participants  
	2. Test on the remaining participant  
	3. Repeat for all participants  



Results
    Average performance across all folds:
	- Accuracy: 0.53  
	- Precision (macro): 0.19  
	- Recall (macro): 0.14  

   Performance is limited due to strong class imbalance between normal and abnormal     breathing events.



Requirements

  Install dependencies using:
   pip install -r requirements.txt

   Required libraries:
	- numpy
	- pandas
	- scipy
	- matplotlib
	- scikit-learn
	- torch


 Author
   Project developed as part of an assignment on physiological signal analysis and    machine learning.