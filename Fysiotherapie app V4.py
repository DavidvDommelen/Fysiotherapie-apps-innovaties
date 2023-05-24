import cv2
import mediapipe as mp
import math
import tkinter as tk

class PoseRecorder:
    def __init__(self, video_file):
        self.video_file = video_file
        self.cap = cv2.VideoCapture(0)
        self.fps = 30  # Set the desired FPS
        self.width = 1080  # Set the desired width
        self.height = 720  # Set the desired height
        self.out = None  # VideoWriter object
        self.recording = False  # Flag to indicate recording status
        self.mp_pose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.left_shoulder_up = False  # Flag to indicate if the left shoulder is up
        self.right_shoulder_up = False  # Flag to indicate if the right shoulder is up
        self.repetitions = 0  # Variable to store the number of repetitions
        self.update()

    def calculate_angle(self, a, b, c):
        # Calculate the angle between three points using the cosine rule
        radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
        angle = math.degrees(radians)
        angle = (angle + 180) % 180  # Ensure the angle is always positive
        return angle

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            flipped = cv2.flip(frame, flipCode=1)
            resized = cv2.resize(flipped, (self.width, self.height))
            rgb_img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            result = self.pose.process(rgb_img)
            self.mpDraw.draw_landmarks(resized, result.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

            # Restore the natural colors of the frame
            rgb_img = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

            # Get the points of the shoulders and hips
            left_shoulder = result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x, result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y
            right_shoulder = result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x, result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y
            left_elbow = result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW].x, result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_ELBOW].y
            right_elbow = result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW].x, result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_ELBOW].y
            left_hip = result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP].x, result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_HIP].y
            right_hip = result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP].x, result.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_HIP].y

            # Calculate the angles of the arms relative to the body
            left_shoulder_angle = self.calculate_angle(left_elbow, left_shoulder, left_hip)
            right_shoulder_angle = self.calculate_angle(right_elbow, right_shoulder, right_hip)

            # Determine repetitions based on the left shoulder angle
            if left_shoulder_angle > 90 and not self.left_shoulder_up:
                self.repetitions += 1
                self.left_shoulder_up = True
            elif left_shoulder_angle <= 90:
                self.left_shoulder_up = False

            # Draw angle and repetitions on the frame
            cv2.putText(rgb_img, f"Right Shoulder Angle: {int(left_shoulder_angle)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(rgb_img, f"Repetitions: {self.repetitions}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display recording status
            if self.recording:
                cv2.putText(rgb_img, "Recording...", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(rgb_img, "Not Recording", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (self.width, self.height))
            img = tk.PhotoImage(data=cv2.imencode('.png', img)[1].tobytes())
            self.canvas.img = img
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

            # Start recording if not already recording
            if self.recording:
                if self.out is None:
                    self.out = cv2.VideoWriter(self.video_file, cv2.VideoWriter_fourcc(*'XVID'), self.fps, (self.width, self.height))
                self.out.write(resized)
            elif self.out is not None:
                self.out.release()
                self.out = None

        self.root.after(int(1000 / self.fps), self.update)

    def start_recording(self):
        self.recording = True

    def stop_recording(self):
        self.recording = False

    def close(self):
        if self.out is not None:
            self.out.release()
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

if __name__ == "__main__":
    pose_recorder = PoseRecorder("pose_detection.mp4")
    pose_recorder.root.bind('s', lambda event: pose_recorder.start_recording())
    pose_recorder.root.bind('e', lambda event: pose_recorder.stop_recording())
    cv2.putText(rgb_img, "Press 's' to start recording", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(rgb_img, "Press 'e' to stop recording", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    pose_recorder.root.mainloop()


