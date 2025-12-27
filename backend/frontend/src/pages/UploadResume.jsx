import React, { useState } from "react";
import api from "../api";

const UploadResume = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [analysis, setAnalysis] = useState("");
  const [rewrittenResume, setRewrittenResume] = useState("");

  const handleAnalyze = async () => {
    if (!resumeFile) {
      alert("Upload your resume first!");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resumeFile);                    // EXACT NAME
    formData.append("job_description", jobDescription);       // EXACT NAME

    try {
      const response = await api.post("/analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setAnalysis(response.data.analysis);
    } catch (error) {
      console.error("Error:", error);
      alert("Analyze failed!");
    }
  };

  const handleRewrite = async () => {
    if (!resumeFile) {
      alert("Upload your resume first!");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resumeFile);                    // EXACT NAME

    try {
      const response = await api.post("/rewrite", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setRewrittenResume(response.data.rewritten_resume);
    } catch (error) {
      console.error("Error:", error);
      alert("Rewrite failed!");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>AI Resume Analyzer</h2>

      <input
        type="file"
        name="resume" 
        onChange={(e) => setResumeFile(e.target.files[0])}
      />

      <textarea
        placeholder="Paste Job Description"
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        style={{ width: "100%", height: "120px", marginTop: "10px" }}
      />

      <button onClick={handleAnalyze}>Analyze Resume</button>
      <button onClick={handleRewrite} style={{ marginLeft: "10px" }}>
        Rewrite Resume
      </button>

      {analysis && (
        <div style={{ marginTop: "20px" }}>
          <h3>Analysis</h3>
          <pre>{analysis}</pre>
        </div>
      )}

      {rewrittenResume && (
        <div style={{ marginTop: "20px" }}>
          <h3>Rewritten Resume</h3>
          <pre>{rewrittenResume}</pre>
        </div>
      )}
    </div>
  );
};

export default UploadResume;
