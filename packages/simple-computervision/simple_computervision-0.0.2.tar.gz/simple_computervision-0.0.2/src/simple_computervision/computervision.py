from ultralytics import YOLO
import cv2
import os
from simple_computervision.logger import logger


def track_detect_video(
    video_filename: str,
    model_name: str = "yolov8n.pt",
    out_filename: str = "out_track.mp4",
    out_dir_name: str = "out_track",
    model_dir_name: str = "models",
    skip_frames: int = 1,
    method_type: str = "track",
):

    if not os.path.exists(video_filename):
        raise FileNotFoundError(f"Could not find video {video_filename}")

    cap = cv2.VideoCapture(video_filename)

    if not cap.isOpened():
        raise Exception("Could not open video")

    w, h, fps, fc = [
        int(i)
        for i in [
            cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
            cap.get(cv2.CAP_PROP_FPS),
            cap.get(cv2.CAP_PROP_FRAME_COUNT),
        ]
    ]

    [os.makedirs(d, exist_ok=True) for d in [model_dir_name, out_dir_name]]  # type: ignore

    video_file_path = os.path.join(out_dir_name, out_filename)
    model_path = os.path.join(model_dir_name, model_name)

    writer = cv2.VideoWriter(video_file_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))  # type: ignore

    model = YOLO(model_path)
    counter = 0
    while True:
        ret, frame = cap.read()

        if not ret:
            logger.info("Video ended")
            break

        if (counter % skip_frames) == 0:

            if method_type == "track":
                result = model.track(frame, persist=True, verbose=False)[0]
                ids = result.boxes.id.cpu().int().numpy()
            elif method_type == "detect":
                result = model.predict(frame, verbose=False)
                ids = None
            else:
                raise ValueError(f"Invalid method type: {method_type}")

            classes = result.boxes.cls.cpu().int().numpy()
            boxes = result.boxes.xyxy.cpu().int().numpy()

            for c, id_, box in zip(classes, ids, boxes):
                x1, y1, x2, y2 = box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                put_str = f"# {id_} {c}" if method_type == "track" else f"# {c}"
                cv2.putText(
                    frame,
                    put_str,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    1,
                )

        writer.write(frame)

        counter += 1

        if (counter % 100) == 0:
            logger.info(f"Processed {counter}/{fc} frames")

    writer.release()
    cap.release()
