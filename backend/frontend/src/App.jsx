import React from "react";
import UploadResume from "./components/UploadResume";
import Home from "./components/Home";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<UploadResume />} />
      </Routes>
    </Router>
  );
}

export default App;
