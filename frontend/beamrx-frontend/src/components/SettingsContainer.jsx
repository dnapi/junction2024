import React, { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import FileUploader from "./FileUploader";

function SettingsContainer() {
  const [formData, setFormData] = useState({
    tenderNumber: "",
    length: "",
    width: "",
    height: "",
    tolerance: "",
    strictMode: false,
  });

  const fileRef = useRef(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const sendFormData = () => {
    const file = fileRef.current?.files[0];

    if (!file) {
      alert("Please select a file");
      return;
    }

    const payload = new FormData();
    payload.append("ifc_file", file);
    payload.append("tenderNumber", formData.tenderNumber);
    payload.append("length", formData.length);
    payload.append("width", formData.width);
    payload.append("height", formData.height);
    payload.append("tolerance", formData.tolerance);
    payload.append("strictMode", formData.strictMode);

    fetch("http://localhost:8000/process_ifc", {
      method: "POST",
      body: payload,
    })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to fetch");
        return response.json();
      })
      .then((data) => {
        console.log("Response Data:", data);
        navigate("/results", { state: { data } });
      })
      .catch((error) => alert("Error sending data: " + error.message));
  };

  return (
    <div className="table-settings">
      <h1>Model view settings</h1>
      <input type="text" name="tenderNumber" placeholder="Enter tender number" value={formData.tenderNumber} onChange={handleChange} />
      <input type="text" name="length" placeholder="Enter length in mm" value={formData.length} onChange={handleChange} />
      <input type="text" name="width" placeholder="Enter width in mm" value={formData.width} onChange={handleChange} />
      <input type="text" name="height" placeholder="Enter height in mm" value={formData.height} onChange={handleChange} />
      <input type="text" name="tolerance" placeholder="Enter tolerance" value={formData.tolerance} onChange={handleChange} />
      <label>
        <input type="checkbox" name="strictMode" checked={formData.strictMode} onChange={handleChange} />
        Strict mode
      </label>
      <FileUploader fileRef={fileRef} />
      <button onClick={sendFormData}>Form table</button>
    </div>
  );
}

export default SettingsContainer;
