import { useEffect, useState } from "react";

import Navbar from "../components/Navbar";
import AnalysisForm from "../components/analysis/AnalysisForm";
import AnalysisResults from "../components/analysis/AnalysisResults";

import {
  analyzeResume,
  getAnalysisHistory,
  getAnalysisById,
  type Analysis,
} from "../services/analysisApi";

interface HistoryItem {
  _id: string;
  resumeFilename: string;
  overallMatchPercentage: number;
  skillMatchPercentage: number;
  createdAt: string;
}

const Dashboard = () => {
  const [analysis, setAnalysis] =
    useState<Analysis | null>(null);

  const [history, setHistory] =
    useState<HistoryItem[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [historyLoading, setHistoryLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const loadHistory = async () => {
    try {
      const data = await getAnalysisHistory();

      setHistory(data);
    } catch (error) {
      console.error(
        "Failed to load analysis history:",
        error
      );
    } finally {
      setHistoryLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleAnalysis = async (
    file: File,
    jobDescription: string,
    requiredSkills: string[]
  ) => {
    try {
      setLoading(true);
      setError("");

      const result = await analyzeResume(
        file,
        jobDescription,
        requiredSkills
      );

      setAnalysis(result);

      await loadHistory();
    } catch (error: any) {
      console.error(
        "Resume analysis failed:",
        error
      );

      setError(
        error?.response?.data?.message ||
          "Analysis failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleHistorySelect = async (
    id: string
  ) => {
    try {
      setLoading(true);
      setError("");

      const result = await getAnalysisById(id);

      setAnalysis(result);

      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    } catch (error: any) {
      console.error(
        "Failed to load analysis:",
        error
      );

      setError(
        error?.response?.data?.message ||
          "Failed to load this analysis."
      );
    } finally {
      setLoading(false);
    }
  };

  const resetAnalysis = () => {
    setAnalysis(null);
    setError("");
  };

  return (
    <div className="dashboard">
      <Navbar onReset={resetAnalysis} />

      <main className="dashboard-main">

        {/* Dashboard introduction */}

        <section className="dashboard-intro">
          <span className="eyebrow">
            CAREER INTELLIGENCE
          </span>

          <h1>
            Your career,
            <br />
            understood.
          </h1>

          <p>
            See how your experience translates to
            the opportunities you want—and what to
            work on next.
          </p>
        </section>

        {/* Analysis form */}

        {!analysis && (
          <AnalysisForm
            loading={loading}
            error={error}
            onSubmit={handleAnalysis}
          />
        )}

        {/* Analysis results */}

        {analysis && (
          <AnalysisResults
            analysis={analysis}
            onReset={resetAnalysis}
          />
        )}

        {/* Analysis history */}

        <section className="history-section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">
                YOUR ACTIVITY
              </span>

              <h2>Recent analyses</h2>
            </div>

            {!historyLoading && (
              <span className="history-count">
                {history.length}{" "}
                {history.length === 1
                  ? "analysis"
                  : "analyses"}
              </span>
            )}
          </div>

          {historyLoading ? (
            <div className="empty-state">
              Loading your analyses...
            </div>
          ) : history.length === 0 ? (
            <div className="empty-state">
              <strong>
                Your analysis history will appear
                here.
              </strong>

              <p>
                Run your first role-fit analysis to
                start building your career profile.
              </p>
            </div>
          ) : (
            <div className="history-list">
              {history.map((item) => (
                <button
                  type="button"
                  className="history-item"
                  key={item._id}
                  onClick={() =>
                    handleHistorySelect(item._id)
                  }
                  disabled={loading}
                >
                  <div>
                    <div className="history-filename">
                      {item.resumeFilename}
                    </div>

                    <div className="history-meta">
                      {new Date(
                        item.createdAt
                      ).toLocaleDateString(
                        undefined,
                        {
                          month: "short",
                          day: "numeric",
                          year: "numeric",
                        }
                      )}
                    </div>
                  </div>

                  <div className="history-metrics">
                    <span>
                      Skill fit{" "}
                      <strong>
                        {item.skillMatchPercentage}%
                      </strong>
                    </span>

                    <span className="history-score">
                      {item.overallMatchPercentage}%
                    </span>

                    <span className="history-action">
                      View analysis
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
};

export default Dashboard;