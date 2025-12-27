import React from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div style={{ padding: "40px", textAlign: "center" }}>
      <h1>AI Resume Analyzer</h1>
      <p>Upload your resume and get instant AI feedback</p>

      <button
        onClick={() => navigate("/upload")}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          fontSize: "18px",
          cursor: "pointer"
        }}
      >
        Upload Resume
      </button>
    </div>
  );
}
