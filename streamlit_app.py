import sys
# !{sys.executable} -m pip install streamlit ultralytics opencv-python numpy streamlit-lottie requests  # (commented out – install packages via pip before running)

import streamlit as st
from ultralytics import YOLO
import cv2
import math
import time
import os
import numpy as np
from streamlit_lottie import st_lottie
import requests

# ---------------------------------------------------------------
# Config & Helper Functions
# ---------------------------------------------------------------
st.set_page_config(page_title="PPE Detection", layout="wide", page_icon="🦺")

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Custom CSS
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(135deg, #0e1117, #262730); color: #fafafa; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# Sidebar & Setup
# ---------------------------------------------------------------
st.sidebar.header("⚙️ Settings")
confidence_threshold = st.sidebar.slider("Confidence Threshold", 0.0, 1.0, 0.45, 0.05)
use_webcam = st.sidebar.toggle("Active Webcam", value=False)

# Load Assets
loading_lottie = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_jcikwtux.json")
violation_lottie = load_lottieurl("https://lottie.host/9339d26e-f56d-4b2a-b327-4740afde482b/nuZ3x3Q2y8.json")

# ---------------------------------------------------------------
# Model Loading
# ---------------------------------------------------------------
@st.cache_resource
def load_model():
    model_path = "models/best.pt"
    if not os.path.exists(model_path):
        st.warning("⚠️ Custom model not found. Downloading fallback YOLOv8n...")
        return YOLO("yolov8n.pt")
    return YOLO(model_path)

try:
    model = load_model()
    # Class Names for the standard PPE model
    classNames = ['hard-hat', 'gloves', 'mask', 'glasses', 'boots', 'vest', 'ppe-suit', 'ear-protector', 'safety-harness']
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ---------------------------------------------------------------
# Main App Layout
# ---------------------------------------------------------------
col1, col2 = st.columns([3, 1])

with col1:
    st.title("🦺 Real‑Time PPE Detection")
    video_placeholder = st.empty()

with col2:
    st.markdown("### 🚨 Status Panel")
    status_placeholder = st.empty()
    if loading_lottie:
        st_lottie(loading_lottie, height=150, key="loader")

# ---------------------------------------------------------------
# Video Logic
# ---------------------------------------------------------------
if use_webcam:
    cap = cv2.VideoCapture(0)

    # Metrics
    prev_frame_time = 0
    curr_frame_time = 0

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            st.error("Failed to read from webcam.")
            break

        # 1. Detection
        results = model(img, stream=True, verbose=False, conf=confidence_threshold)

        violation_count = 0
        safe_count = 0

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Class & Conf
                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])

                try:
                    currentClass = classNames[cls]
                except:
                    currentClass = "Unknown"

                # 2. Safety Logic (Green for Safe, Red for Unsafe)
                # Adjust this logic based on what your model actually detects
                if currentClass in ['hard-hat', 'vest', 'ppe-suit']:
                    color = (0, 255, 0) # Green
                    safe_count += 1
                else:
                    # If model detects 'NO-Hardhat' or just 'Person' without PPE
                    color = (0, 0, 255) # Red
                    violation_count += 1

                # Draw on image
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)

                # Label
                label = f'{currentClass} {conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=0.6, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1, y1), c2, color, -1, cv2.LINE_AA)  # Filled
                cv2.putText(img, label, (x1, y1 - 2), 0, 0.6, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

        # 3. FPS Calculation
        curr_frame_time = time.time()
        fps = 1 / (curr_frame_time - prev_frame_time)
        prev_frame_time = curr_frame_time
        cv2.putText(img, f'FPS: {int(fps)}', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        # 4. Display Video
        # Streamlit requires RGB, OpenCV uses BGR
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        video_placeholder.image(img_rgb, channels="RGB", use_column_width=True)

        # 5. Update Status Panel
        if violation_count > 0:
            status_placeholder.markdown(
                f"""
                <div style="background-color: #ff4b4b; padding: 20px; border-radius: 10px;">
                    <h2 style="color: white; margin:0;">⚠️ VIOLATION</h2>
                    <p style="color: white;">{violation_count} Unsafe Workers</p>
                </div>
                """, unsafe_allow_html=True
            )
        else:
            status_placeholder.markdown(
                f"""
                <div style="background-color: #0df2c9; padding: 20px; border-radius: 10px;">
                    <h2 style="color: black; margin:0;">✅ SAFE</h2>
                    <p style="color: black;">{safe_count} Compliant Workers</p>
                </div>
                """, unsafe_allow_html=True
            )

    cap.release()
else:
    st.info("⬅️ Toggle 'Active Webcam' in the sidebar to start the monitor.")
