import { useLocation } from "react-router-dom";
import FaceAnalyzer from "../components/FaceAnalyzer";

function Result() {
  const location = useLocation();
  const image = location.state?.image;

  return (
    <div>
      <h1>분석 결과 💇‍♂️</h1>

      {image && <img src={image} width="200" />}

      <FaceAnalyzer />
    </div>
  );
}

export default Result;