import React from "react";
import FileUploader from "./FileUploader";

function TrainingContainer({ toggleView }) {
  return (
    <div className="table-training">
      <h1>Training model</h1>
      
      <h2>Upload IFC file</h2>
      <FileUploader label="Select IFC file" />

      <h2>Upload Excel file</h2>
      <FileUploader label="Select Excel file" />

      <button onClick={toggleView}>Back</button>
    </div>
  );
}

export default TrainingContainer;
