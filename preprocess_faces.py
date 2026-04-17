import os
import cv2
import mediapipe as mp

INPUT_DIR = "dataset"
OUTPUT_DIR = "processed_dataset"
TARGET_SIZE = (224, 224)
MARGIN_RATIO = 0.25

mp_face_detection = mp.solutions.face_detection


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def crop_face(image, bbox, margin_ratio=0.25):
    h, w = image.shape[:2]

    x = int(bbox.xmin * w)
    y = int(bbox.ymin * h)
    bw = int(bbox.width * w)
    bh = int(bbox.height * h)

    mx = int(bw * margin_ratio)
    my = int(bh * margin_ratio)

    x1 = max(0, x - mx)
    y1 = max(0, y - my)
    x2 = min(w, x + bw + mx)
    y2 = min(h, y + bh + my)

    return image[y1:y2, x1:x2]


def process_image(face_detector, input_path, output_path):
    image = cv2.imread(input_path)

    if image is None:
        print(f"[실패] 이미지 읽기 실패: {input_path}")
        return

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_detector.process(image_rgb)

    if not results.detections:
        print(f"[건너뜀] 얼굴 없음: {input_path}")
        return

    detection = results.detections[0]
    bbox = detection.location_data.relative_bounding_box

    face_crop = crop_face(image, bbox, MARGIN_RATIO)

    if face_crop.size == 0:
        print(f"[실패] 얼굴 crop 비어 있음: {input_path}")
        return

    face_crop = cv2.resize(face_crop, TARGET_SIZE)

    ensure_dir(os.path.dirname(output_path))
    cv2.imwrite(output_path, face_crop)
    print(f"[완료] {output_path}")


def main():
    ensure_dir(OUTPUT_DIR)

    with mp_face_detection.FaceDetection(
        model_selection=1,
        min_detection_confidence=0.5
    ) as face_detector:

        for class_name in os.listdir(INPUT_DIR):
            class_input_path = os.path.join(INPUT_DIR, class_name)
            class_output_path = os.path.join(OUTPUT_DIR, class_name)

            if not os.path.isdir(class_input_path):
                continue

            ensure_dir(class_output_path)

            for filename in os.listdir(class_input_path):
                ext = os.path.splitext(filename)[1].lower()
                if ext not in [".jpg", ".jpeg", ".png", ".bmp"]:
                    continue

                input_path = os.path.join(class_input_path, filename)
                output_path = os.path.join(class_output_path, filename)

                process_image(face_detector, input_path, output_path)


if __name__ == "__main__":
    main()