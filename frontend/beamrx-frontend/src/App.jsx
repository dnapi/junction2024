import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SettingsContainer from "./components/SettingsContainer";
import ResultsTable from "./components/ResultsTable";
import beamrxLogo from "/images/beamrx.png";
import peikkoLogo from "/images/peikko.png";
import "./styles.css";

function App() {
  return (
    <Router>
      <div className="App">
        <div className="background-div"></div>
        <img src={beamrxLogo} alt="BeamrX Logo" className="beamrx-logo" />
        <img src={peikkoLogo} alt="Peikko Logo" className="peikko-logo" />
        <Routes>
          <Route path="/" element={<SettingsContainer />} />
          <Route path="/results" element={<ResultsTable />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
