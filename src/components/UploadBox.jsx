import { useState } from "react";
import { useNavigate } from "react-router-dom";

function UploadBox() {
  const [image, setImage] = useState(null);
  const navigate = useNavigate();

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setImage(imageUrl);
    }
  };

  const goResult = () => {
    navigate("/result", { state: { image } });
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleUpload} />

      {image && (
        <div>
          <h3>미리보기</h3>
          <img src={image} alt="preview" width="200" />

          <br />
          <button onClick={goResult}>분석하기</button>
        </div>
      )}
    </div>
  );
}

export default UploadBox;