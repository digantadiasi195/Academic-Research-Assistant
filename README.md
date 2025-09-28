# Human Action Recognition with MS-TCN

This demo uses a **Multi-Stage Temporal Convolutional Network (MS-TCN)** to recognize human actions from skeleton data on the **PKU-MMDv2 dataset**.

## Files

- `train_ms_tcn.py` – Trains the MS-TCN model  
- `inference.py` – Runs real-time action recognition on videos with visual output

## How to Run

### 1. Train the model
```bash
python train_ms_tcn.py

profile
Qwen3-Max
8:01 pm
markdown


1
2
3
4
5
6
7
8
9
10
11
12
13
14
⌄
⌄
⌄
⌄
⌄
# Human Action Recognition with MS-TCN

This demo uses a **Multi-Stage Temporal Convolutional Network (MS-TCN)** to recognize human actions from skeleton data on the **PKU-MMDv2 dataset**.

## Files

- `train_ms_tcn.py` – Trains the MS-TCN model  
- `inference.py` – Runs real-time action recognition on videos with visual output

## How to Run

### 1. Train the model
```bash
python train_ms_tcn.py
Saves model to models/ms_tcn_pku.pth and normalization stats to models/.

2. Run inference
bash


1
python inference.py
Prompts you to select a video (e.g., 0002-M)
Shows live skeleton + predicted action with ID, name, and confidence
Press q or ESC to exit
Note: Make sure your dataset is at E:/CARET_Project/CARET/PKUMMDv2/ (or update paths in the code). 

Demo
Inference Screenshot 1

Inference Screenshot 2

Requirements
Python 3.8+
PyTorch
OpenCV
pandas, numpy
Install dependencies:

bash


1
pip install torch opencv-python pandas numpy
Built for the CARET Project | PKU-MMDv2 dataset required 



1
