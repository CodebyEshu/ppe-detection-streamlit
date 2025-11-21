# Real‑Time PPE Detection (Streamlit)

🦺 **Detect hard‑hat violations from a webcam feed in real time** using a YOLOv8 model.

---

## ✨ Features
- Live webcam stream with bounding‑box annotations.
- FPS counter and violation alert overlay.
- Simple, single‑file Streamlit UI.
- Ready to deploy on **Streamlit Community Cloud** (free) directly from GitHub.

---

## 🚀 Quick start (local)
```bash
# Clone the repo (or copy the folder)
git clone <your‑repo‑url>
cd ppe_detection

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🌐 Deploy to Streamlit Community Cloud (live on GitHub)
1. Push this repository to GitHub.
2. Sign in to https://share.streamlit.io.
3. Click **New app**, select your repo, branch `main`, and the file `streamlit_app.py`.
4. Click **Deploy** – Streamlit will automatically install the dependencies from `requirements.txt` and give you a public URL.

Whenever you push new commits, the app will be redeployed automatically.

---

## 📂 Project structure
```
ppe_detection/
├─ src/                # Detector implementation (your existing code)
├─ models/best.pt      # Trained YOLO model (must be present)
├─ streamlit_app.py    # Streamlit entry point (added)
├─ requirements.txt    # Python dependencies
├─ README.md           # You are reading it!
└─ .streamlit/        # Streamlit theme configuration (optional)
```

---

## 🎨 Design notes
- Dark theme with vibrant accent colors for a premium look.
- Minimal UI – just the video feed and a title.
- Uses native OpenCV drawing for speed; Streamlit handles the display.

---

## 🛠️ Future enhancements (optional)
- Add a sidebar to select webcam device, confidence threshold, etc.
- Store violation timestamps in a CSV for audit logs.
- Deploy on GitHub Pages using WebAssembly (more complex).

---

*Happy coding!*
