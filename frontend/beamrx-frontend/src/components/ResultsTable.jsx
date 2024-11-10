import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

function ResultsTable() {
  const location = useLocation();
  const navigate = useNavigate();
  const data = location.state?.data || {};

  const handleBack = () => {
    navigate("/"); // Navigates to the main page at "/"
  };

  return (
    <div className="results-container">
      <h1>Results Table</h1>
      <table className="results-table">
        <thead>
          <tr>
            <th>Type</th>
            <th>Coordinates</th>
            <th>Distance</th>
            <th>Entities</th>
            <th>Clash Type</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(data).map(([type, records], index) => (
            records.map((record, idx) => (
              <tr key={`${index}-${idx}`}>
                <td>{type}</td>
                <td>{record.coords ? record.coords.join(", ") : "N/A"}</td>
                <td>{record.distance || "N/A"}</td>
                <td>
                  {record.entities
                    ? record.entities.map((entity, i) => (
                        <span key={i}>{JSON.stringify(entity)}, </span>
                      ))
                    : "N/A"}
                </td>
                <td>
                  {record.clash_type
                    ? record.clash_type.join(", ")
                    : "N/A"}
                </td>
              </tr>
            ))
          ))}
        </tbody>
      </table>
      <button className="back-button" onClick={handleBack}>Back</button>
    </div>
  );
}

export default ResultsTable;
