from ultralytics import YOLO
import cv2

model = YOLO('best.pt') 


DISTANCE_M = 9.144
ax1 = 70
ay = 90
ax2 = 230

bx1 = 15
by = 125
bx2 = 225


class SpeedLine:
    def __init__(self, x1, x2, y):
        self.x1 = x1
        self.x2 = x2
        self.y = y

    def is_crossed(self, cx, prev_y, cur_y):

        if (self.x1 <= cx <= self.x2):
            if (prev_y < self.y <= cur_y) or (prev_y > self.y >= cur_y):
                return True
        return False



class Vehicle:
    def __init__(self, track_id):
        self.track_id = track_id
        self.prev_cy = None
        self.frame_a = None
        self.frame_b = None
        self.speed_kmh = None
        self.fps = None

    def update(self, cx, cy, now, line_a, line_b):
        if self.prev_cy is not None:
            if self.frame_a is None and line_a.is_crossed(cx, self.prev_cy, cy):
                self.frame_a = now

            if self.frame_b is None and line_b.is_crossed(cx, self.prev_cy, cy):
                self.frame_b = now

        self.prev_cy = cy

    def get_speed(self):
        if self.speed_kmh is not None:
            return self.speed_kmh
        if self.frame_a is not None and self.frame_b is not None:
            elapsed_frames = self.frame_b - self.frame_a
            if elapsed_frames > 0:
                t = elapsed_frames / self.fps
                self.speed_kmh = DISTANCE_M / t * 3.6
        return self.speed_kmh


class SpeedDetector:
    def __init__(self, model_path, video_path):
            self.model = YOLO(model_path)
            self.video_path = video_path
            self.cap = cv2.VideoCapture(video_path)

            self.fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            self.vehicles = {}
            self.line_a = SpeedLine(x1=ax1, x2=ax2, y=ay)
            self.line_b = SpeedLine(x1=bx1, x2=bx2, y=by)
    def run(self, output_path='output.mp4'):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))

        if not writer.isOpened():
            raise RuntimeError(f'Could not open video writer for {output_path} — check the path is valid.')

        frame_count = 0

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            results = self.model.track(frame, persist=True, tracker="bytetrack.yaml", conf=0.3)
            boxes = results[0].boxes

            if boxes.id is not None:
                for (x1, y1, x2, y2), track_id in zip(boxes.xyxy.int().tolist(), boxes.id.int().tolist()):
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                    if track_id not in self.vehicles:
                        self.vehicles[track_id] = Vehicle(track_id)

                    vehicle = self.vehicles[track_id]
                    vehicle.fps = self.fps
                    vehicle.update(cx, cy, frame_count, self.line_a, self.line_b)
                    speed = vehicle.get_speed()

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    label = f'ID {track_id}'
                    if speed is not None:
                        label += f' {speed:.1f} km/h'
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.line(frame, (self.line_a.x1, self.line_a.y), (self.line_a.x2, self.line_a.y), (255, 0, 0), 2)
            cv2.line(frame, (self.line_b.x1, self.line_b.y), (self.line_b.x2, self.line_b.y), (0, 0, 255), 2)

            writer.write(frame)
            frame_count += 1

        self.cap.release()
        writer.release()
        print('Processing Complete and Video Saved!')


detector = SpeedDetector(model_path='best.pt', video_path='Task_Video.mp4')
detector.run()