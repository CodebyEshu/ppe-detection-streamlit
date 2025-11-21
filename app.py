import cv2
import cvzone
import time
import os
from src.detector import Detector

def main():
    # Initialize Detector
    model_path = "models/best.pt"
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}. Please run setup_model.py first.")
        return

    detector = Detector(model_path)

    # Initialize Webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280) # Width
    cap.set(4, 720)  # Height

    prev_frame_time = 0
    new_frame_time = 0

    print("Starting PPE Monitor - Live...")

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from webcam.")
            break

        # Get detections
        detections = detector.detect(img)
        
        violation_detected = False

        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            color = det['color']
            class_name = det['class']
            conf = det['conf']

            # Draw Box
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 3)
            
            # Draw Label
            cvzone.putTextRect(img, f'{class_name} {conf}', 
                               (max(0, x1), max(35, y1)), 
                               scale=1, thickness=1, 
                               colorR=color, colorT=(255, 255, 255), offset=5)

            # Check for Violation (High Confidence No-Helmet)
            if 'no-hardhat' in class_name.lower() and conf > 0.6:
                violation_detected = True

        # FPS Counter
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time)
        prev_frame_time = new_frame_time
        cvzone.putTextRect(img, f'FPS: {int(fps)}', (20, 50), scale=2, thickness=2, colorR=(0, 0, 0))

        # Violation Alert
        if violation_detected:
            cvzone.putTextRect(img, "VIOLATION DETECTED", (400, 100), scale=3, thickness=3, colorR=(0, 0, 255))

        cv2.imshow("PPE Monitor - Live", img)

        # Exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
