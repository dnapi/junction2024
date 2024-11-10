import React from "react";

function FileUploader({ label = "Select file", fileRef }) {
  return (
    <div>
      <label>{label}</label>
      <input type="file" ref={fileRef} />
    </div>
  );
}

export default FileUploader;
