import { useEffect, useRef } from "react";
import { FaceMesh } from "@mediapipe/face_mesh";
import { Camera } from "@mediapipe/camera_utils";

function FaceAnalyzer() {
  const videoRef = useRef(null);

  useEffect(() => {
    if (!videoRef.current) return;

    const videoElement = videoRef.current;

    const faceMesh = new FaceMesh({
      locateFile: (file) =>
        `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`,
    });

    faceMesh.setOptions({
      maxNumFaces: 1,
      refineLandmarks: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    faceMesh.onResults((results) => {
      if (results.multiFaceLandmarks?.length > 0) {
        console.log("얼굴 좌표:", results.multiFaceLandmarks[0]);
      }
    });

    const camera = new Camera(videoElement, {
      onFrame: async () => {
        await faceMesh.send({ image: videoElement });
      },
      width: 640,
      height: 480,
    });

    camera.start();

    return () => {
      if (videoElement.srcObject) {
        videoElement.srcObject.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  return (
    <div>
      <h2>얼굴 분석 중...</h2>
      <video ref={videoRef} autoPlay playsInline muted style={{ width: "300px" }} />
    </div>
  );
}

export default FaceAnalyzer;