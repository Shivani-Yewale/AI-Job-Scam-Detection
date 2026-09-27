import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    title: "",
    company_profile: "",
    description: "",
    requirements: "",
    benefits: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [selectedHistory, setSelectedHistory] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const fetchHistory = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/history");
      const data = await response.json();
      setHistory(data);
    } catch (error) {
      console.error("Error loading history:", error);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error("Prediction failed");
      }

      setResult(data);
      fetchHistory();
    } catch (error) {
      console.error(error);

      alert(
        "Could not connect to the backend. Make sure FastAPI is running on http://127.0.0.1:8000"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFormData({
      title: "",
      company_profile: "",
      description: "",
      requirements: "",
      benefits: "",
    });

    setResult(null);
  };

  const loadFakeExample = () => {
    setFormData({
      title: "Data Entry Operator",
      company_profile: "Unknown company",
      description: "Work from home and earn high income immediately.",
      requirements: "No experience required. No interview needed.",
      benefits: "Earn $5000 every week after paying registration fee.",
    });

    setResult(null);
  };

  const loadLegitimateExample = () => {
    setFormData({
      title: "Software Developer",
      company_profile:
        "ABC Technologies is a software development company providing web and cloud solutions.",
      description:
        "We are looking for a Software Developer to work with our engineering team on web applications and backend services.",
      requirements:
        "Bachelor's degree in Computer Science or related field. Knowledge of Python, SQL, Git, and basic web development.",
      benefits:
        "Competitive salary, health insurance, paid leave, training opportunities, and flexible working hours.",
    });

    setResult(null);
  };

  const getResultClass = () => {
    if (!result) return "result-card";

    if (result.risk_level === "High") {
      return "result-card result-high";
    }

    if (result.risk_level === "Medium") {
      return "result-card result-medium";
    }

    return "result-card result-low";
  };

  const getBadgeClass = () => {
    if (!result) return "risk-badge";

    if (result.risk_level === "High") {
      return "risk-badge badge-high";
    }

    if (result.risk_level === "Medium") {
      return "risk-badge badge-medium";
    }

    return "risk-badge badge-low";
  };

  const getProgressClass = () => {
    if (!result) return "progress-bar";

    if (result.risk_level === "High") {
      return "progress-bar bar-high";
    }

    if (result.risk_level === "Medium") {
      return "progress-bar bar-medium";
    }

    return "progress-bar bar-low";
  };

  const getHistoryRiskClass = (riskLevel) => {
    if (riskLevel === "High") {
      return "history-risk history-high";
    }

    if (riskLevel === "Medium") {
      return "history-risk history-medium";
    }

    return "history-risk history-low";
  };

  return (
    <div className="container">
      <header className="page-header">
        <div className="header-icon">🛡️</div>

        <h1>AI Job Scam Detection</h1>

        <p className="subtitle">
          Analyze job postings using Machine Learning and identify suspicious
          recruitment offers.
        </p>
      </header>

      <form onSubmit={handleSubmit}>
        <h2 className="form-title">Enter Job Details</h2>

        <div className="sample-buttons">
          <button
            type="button"
            className="sample-fake"
            onClick={loadFakeExample}
          >
            Load Fake Job Example
          </button>

          <button
            type="button"
            className="sample-legit"
            onClick={loadLegitimateExample}
          >
            Load Legitimate Job Example
          </button>
        </div>

        <label htmlFor="title">Job Title</label>

        <input
          id="title"
          type="text"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="Example: Data Entry Operator"
          required
        />

        <label htmlFor="company_profile">Company Profile</label>

        <textarea
          id="company_profile"
          name="company_profile"
          value={formData.company_profile}
          onChange={handleChange}
          placeholder="Enter information about the company"
          required
        />

        <label htmlFor="description">Job Description</label>

        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="Enter the complete job description"
          required
        />

        <label htmlFor="requirements">Requirements</label>

        <textarea
          id="requirements"
          name="requirements"
          value={formData.requirements}
          onChange={handleChange}
          placeholder="Enter job requirements"
          required
        />

        <label htmlFor="benefits">Benefits</label>

        <textarea
          id="benefits"
          name="benefits"
          value={formData.benefits}
          onChange={handleChange}
          placeholder="Enter salary, benefits or other offers"
          required
        />

        <div className="button-group">
          <button
            className="analyze-button"
            type="submit"
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze Job"}
          </button>

          <button
            className="clear-button"
            type="button"
            onClick={handleClear}
          >
            Clear
          </button>
        </div>
      </form>

      {result && (
        <div className={getResultClass()}>
          <div className="result-header">
            <h2>Analysis Result</h2>

            <span className={getBadgeClass()}>
              {result.risk_level} Risk
            </span>
          </div>

          <p className="result-main">{result.result}</p>

          <div className="probability-grid">
            <div className="probability-box">
              <span>Fraud Probability</span>
              <strong>{result.fraud_probability}%</strong>
            </div>

            <div className="probability-box">
              <span>Legitimate Probability</span>
              <strong>{result.legitimate_probability}%</strong>
            </div>
          </div>

          <p className="progress-label">Fraud Risk</p>

          <div className="progress-container">
            <div
              className={getProgressClass()}
              style={{
                width: result.fraud_probability + "%",
              }}
            ></div>
          </div>

          <div className="reason-section">
            <h3>Why was this result given?</h3>

            <ul>
              {result.reasons.map((reason, index) => (
                <li key={index}>{reason}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
      
      <div className="stats-section">
        <div className="stat-card">
          <span className="stat-icon">📊</span>
          <div>
            <p>Total Predictions</p>
            <h3>{history.length}</h3>
          </div>
        </div>

        <div className="stat-card stat-high">
          <span className="stat-icon">🚨</span>
          <div>
            <p>High Risk</p>
            <h3>
              {history.filter(
                (item) => item.risk_level === "High"
              ).length}
            </h3>
          </div>
        </div>

        <div className="stat-card stat-medium">
          <span className="stat-icon">⚠️</span>
          <div>
            <p>Medium Risk</p>
            <h3>
              {history.filter(
                (item) => item.risk_level === "Medium"
              ).length}
            </h3>
          </div>
        </div>

        <div className="stat-card stat-low">
          <span className="stat-icon">✅</span>
          <div>
            <p>Low Risk</p>
            <h3>
              {history.filter(
                (item) => item.risk_level === "Low"
              ).length}
            </h3>
          </div>
        </div>
      </div>


      <div className="history-section">
        <div className="history-header">
          <h2>📋 Prediction History</h2>

          <button
            type="button"
            className="refresh-history-button"
            onClick={fetchHistory}
          >
            🔄 Refresh
          </button>
        </div>

        {history.length === 0 ? (
          <p className="no-history">
            No prediction history available.
          </p>
        ) : (
          <div className="history-list">
            {history.map((item, index) => (
              <div className="history-card" key={index}>
                <div className="history-card-header">
                  <h3>{item.title || "Untitled Job"}</h3>

                  <span
                    className={getHistoryRiskClass(item.risk_level)}
                  >
                    {item.risk_level} Risk
                  </span>
                </div>

                <p className="history-result">
                  {item.result}
                </p>

                <div className="history-details">
                  <span>
                    🚨 Fraud:{" "}
                    <strong>
                      {item.fraud_probability}%
                    </strong>
                  </span>

                  <span>
                    ✅ Legitimate:{" "}
                    <strong>
                      {item.legitimate_probability}%
                    </strong>
                  </span>

                  <span>
                    Time: {item.timestamp || "Unknown time"}
                  </span>
                </div>

                <button
                  type="button"
                  className="view-details-button"
                  onClick={() => {
                    if (selectedHistory === index) {
                      setSelectedHistory(null);
                    } else {
                      setSelectedHistory(index);
                    }
                  }}
                >
                  {selectedHistory === index
                    ? "Hide Details"
                    : "View Details"}
                </button>

                {selectedHistory === index && (
                  <div className="history-reasons">
                    <h4>Why was this result given?</h4>

                    {item.reasons && item.reasons.length > 0 ? (
                      <ul>
                        {item.reasons.map((reason, reasonIndex) => (
                          <li key={reasonIndex}>
                            {reason}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p>No reasons available.</p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <footer>
        <p>AI-Based Job Scam Detection & Risk Analysis System</p>
      </footer>
    </div>
  );
}

export default App;
