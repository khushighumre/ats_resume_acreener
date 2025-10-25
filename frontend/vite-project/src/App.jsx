import { useState } from "react";

function App() {
  const [jd, setJd] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [error, setError] = useState("");

  const handleResumeInfo = async () => {
    if (!file) {
      setError("Please upload a resume file");
      return;
    }
    setError("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/resume-info", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      if (data.error) {
        setError(data.error);
        setResult("");
      } else {
        // Format the structured data nicely
        const formatted = `Name: ${data.Name}
Email: ${data.Email}
Phone: ${data.Phone}

Skills: ${data.Skills.join(", ") || "None found"}

Education:\n${data.Education.join("\n") || "None found"}

Projects:\n${data.Projects.join("\n") || "None found"}

Experience:\n${data.Experience.join("\n") || "None found"}`;
        setResult(formatted);
      }
    } catch (err) {
      console.error(err);
      setError("Error fetching resume info");
      setResult("");
    }
  };

  const handlePercentageMatch = async () => {
    if (!file) {
      setError("Please upload a resume file");
      return;
    }
    if (!jd) {
      setError("Please enter a Job Description");
      return;
    }
    setError("");

    const formData = new FormData();
    formData.append("file", file);
    formData.append("jd", jd);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/percentage-match",
        {
          method: "POST",
          body: formData,
        }
      );
      const data = await response.json();
      if (data.error) {
        setError(data.error);
        setResult("");
      } else {
        setResult(`Match Percentage: ${data.percentage_match}%`);
      }
    } catch (err) {
      console.error(err);
      setError("Error fetching percentage match");
      setResult("");
    }
  };

  return (
    <div
  style={{  
    minHeight: "100vh",
    width: "100vw",
    backgroundColor: "#f0f2f5",
    fontFamily: "Arial, sans-serif",
    padding: "40px 50px", // spacing from edges
    boxSizing: "border-box",
  }}
>
  <div
    style={{
      width: "100%",
      maxWidth: "1200px", // allow wider card on desktop
      margin: "0 auto", // center horizontally
      backgroundColor: "#fff",
      padding: "40px",
      borderRadius: "12px",
      boxShadow: "0 6px 18px rgba(0,0,0,0.1)",
    }}
  >
    <h1 style={{ textAlign: "center", color: "#333", marginBottom: "40px" }}>
      ATS Resume Screener
    </h1>

    {/* Job Description */}
    <div style={{ marginBottom: "25px" }}>
      <label style={{ fontWeight: "bold", color: "#555" }}>Job Description:</label>
      <textarea
        placeholder="Enter Job Description"
        value={jd}
        onChange={(e) => setJd(e.target.value)}
        style={{
          width: "100%",
          minHeight: "140px",
          padding: "15px",
          marginTop: "8px",
          borderRadius: "6px",
          border: "1px solid #ccc",
          outline: "none",
          fontSize: "14px",
          transition: "border-color 0.3s",
        }}
        onFocus={(e) => (e.target.style.borderColor = "#4a90e2")}
        onBlur={(e) => (e.target.style.borderColor = "#ccc")}
      />
    </div>

    {/* Resume Upload */}
    <div style={{ marginBottom: "30px" }}>
      <label style={{ fontWeight: "bold", color: "#555" }}>Upload Resume (PDF/DOCX):</label>
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        style={{
          display: "block",
          marginTop: "8px",
          fontSize: "14px",
          padding: "6px",
        }}
      />
    </div>

    {/* Buttons */}
    <div style={{ display: "flex", justifyContent: "center", gap: "20px", marginBottom: "30px" }}>
      <button
        onClick={handleResumeInfo}
        style={{
          padding: "12px 25px",
          backgroundColor: "#4a90e2",
          color: "#fff",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          fontWeight: "bold",
          fontSize: "14px",
          transition: "background-color 0.3s",
        }}
        onMouseEnter={(e) => (e.target.style.backgroundColor = "#357ABD")}
        onMouseLeave={(e) => (e.target.style.backgroundColor = "#4a90e2")}
      >
        Tell me about the resume
      </button>
      <button
        onClick={handlePercentageMatch}
        style={{
          padding: "12px 25px",
          backgroundColor: "#27ae60",
          color: "#fff",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
          fontWeight: "bold",
          fontSize: "14px",
          transition: "background-color 0.3s",
        }}
        onMouseEnter={(e) => (e.target.style.backgroundColor = "#1e8449")}
        onMouseLeave={(e) => (e.target.style.backgroundColor = "#27ae60")}
      >
        Percentage Match
      </button>
    </div>

    {/* Error */}
    {error && (
      <div style={{ color: "red", marginBottom: "25px", fontWeight: "bold", textAlign: "center" }}>
        {error}
      </div>
    )}

    {/* Result */}
    {result && (
      <div
        style={{
          padding: "25px",
          border: "1px solid #ddd",
          borderRadius: "10px",
          backgroundColor: "#f9f9f9",
          maxHeight: "400px",
          overflowY: "auto",
          whiteSpace: "pre-wrap",
          color: "#333",
        }}
      >
        {result}
      </div>
    )}
  </div>
</div>
  );
}

export default App;
