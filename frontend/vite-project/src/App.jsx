import { useState } from "react";

function App() {
  const [jd, setJd] = useState("");      // Job Description
  const [file, setFile] = useState(null); // Resume file
  const [result, setResult] = useState(""); // Result to display

  return (
    <div>
      <h1>ATS Resume Screener</h1>
      <textarea
        placeholder="Enter Job Description"
        value={jd}
        onChange={(e) => setJd(e.target.value)}
      />
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <div>
        <button>Tell me about the resume</button>
        <button>Percentage Match</button>
      </div>
      <div>
        <h2>Result:</h2>
        <pre>{result}</pre>
      </div>
    </div>
  );
}

export default App;
