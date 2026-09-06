import { useState } from "react";
import type { CSSProperties } from "react";
import type { Analysis } from "../../services/analysisApi";

interface AnalysisResultsProps {
  analysis: Analysis;
  onReset: () => void;
}

const AnalysisResults = ({
  analysis,
  onReset,
}: AnalysisResultsProps) => {
  const [expandedGap, setExpandedGap] =
    useState<string | null>(null);

  const matchedCount = analysis.matchedSkills.length;
  const requiredCount = analysis.requiredSkills.length;

  const matchScore = analysis.overallMatchPercentage;

  const getScoreLabel = (score: number) => {
    if (score >= 80) return "Excellent fit";
    if (score >= 65) return "Strong foundation";
    if (score >= 50) return "Promising foundation";
    return "Early-stage fit";
  };

  const getScoreMessage = (score: number) => {
    if (score >= 80) {
      return "Your experience aligns strongly with the requirements of this role.";
    }

    if (score >= 65) {
      return "You have a strong foundation for this role, with a few areas worth strengthening.";
    }

    if (score >= 50) {
      return "You have a promising foundation, with some important skills to develop.";
    }

    return "This role has several gaps relative to your current profile, but the results highlight where to focus next.";
  };

  return (
    <section className="analysis-results">
      {/* Results header */}

      <div className="results-header">
        <div>
          <span className="eyebrow">
            ANALYSIS COMPLETE
          </span>

          <h2>Your role fit</h2>

          <p>
            Based on your resume and the requirements
            provided for this position.
          </p>
        </div>

        <button
          type="button"
          className="secondary-button"
          onClick={onReset}
        >
          Analyze another role
        </button>
      </div>

      {/* Match overview */}

      <section className="match-overview">
        <div className="score-panel">
          <div
            className="score-ring"
            style={
              {
                "--score": matchScore,
              } as CSSProperties
            }
          >
            <span>{matchScore}%</span>
          </div>

          <div className="score-copy">
            <span className="score-label">
              {getScoreLabel(matchScore)}
            </span>

            <p>
              {getScoreMessage(matchScore)}
            </p>
          </div>
        </div>

        <div className="score-breakdown">
          <div className="score-stat">
            <span>Skill fit</span>

            <strong>
              {analysis.skillMatchPercentage}%
            </strong>
          </div>

          <div className="score-stat">
            <span>Semantic fit</span>

            <strong>
              {analysis.semanticSimilarity
                ? `${(
                    analysis.semanticSimilarity * 100
                  ).toFixed(1)}%`
                : "—"}
            </strong>
          </div>

          <div className="score-stat">
            <span>Text similarity</span>

            <strong>
              {analysis.textSimilarity
                ? `${(
                    analysis.textSimilarity * 100
                  ).toFixed(1)}%`
                : "—"}
            </strong>
          </div>
        </div>
      </section>

      {/* Skill coverage */}

      <section className="results-section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">
              SKILL COVERAGE
            </span>

            <h2>
              {matchedCount} of {requiredCount} required
              skills matched
            </h2>

            <p>
              A direct comparison between your detected
              skills and the requirements for this role.
            </p>
          </div>
        </div>

        <div className="skill-coverage">
          <div className="coverage-summary">
            <div className="coverage-score">
              <strong>
                {analysis.skillMatchPercentage}%
              </strong>

              <span>skill fit</span>
            </div>

            <div className="coverage-track">
              <div
                className="coverage-track-fill"
                style={{
                  width: `${Math.min(
                    analysis.skillMatchPercentage,
                    100
                  )}%`,
                }}
              />
            </div>
          </div>

          <div className="skill-list">
            {analysis.requiredSkills.map((skill) => {
              const isMatched =
                analysis.matchedSkills.some(
                  (matchedSkill) =>
                    matchedSkill.toLowerCase() ===
                    skill.toLowerCase()
                );

              return (
                <div
                  className={`skill-row ${
                    isMatched ? "matched" : "missing"
                  }`}
                  key={skill}
                >
                  <div className="skill-row-main">
                    <span className="skill-status">
                      {isMatched ? "✓" : "＋"}
                    </span>

                    <span>{skill}</span>
                  </div>

                  <span className="skill-row-status">
                    {isMatched ? "Matched" : "Missing"}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Development priorities */}

      {analysis.skillGapAnalysis.length > 0 && (
        <section className="results-section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">
                DEVELOPMENT PRIORITIES
              </span>

              <h2>Where to focus next</h2>

              <p>
                These areas were identified from the
                skills missing from your target role.
              </p>
            </div>
          </div>

          <div className="skill-gap-grid">
            {analysis.skillGapAnalysis.map(
              (gap, index) => {
                const isExpanded =
                  expandedGap === gap.skill;

                return (
                  <article
                    className={`skill-gap-card ${
                      isExpanded ? "expanded" : ""
                    }`}
                    key={gap.skill}
                  >
                    <button
                      type="button"
                      className="skill-gap-trigger"
                      onClick={() =>
                        setExpandedGap(
                          isExpanded
                            ? null
                            : gap.skill
                        )
                      }
                      aria-expanded={isExpanded}
                    >
                      <div className="gap-number">
                        {String(index + 1).padStart(
                          2,
                          "0"
                        )}
                      </div>

                      <div className="gap-content">
                        <div className="gap-title-row">
                          <h3>{gap.skill}</h3>

                          {gap.priority && (
                            <span
                              className={`priority-badge ${gap.priority.toLowerCase()}`}
                            >
                              {gap.priority}
                            </span>
                          )}
                        </div>

                        {gap.reason && (
                          <p>{gap.reason}</p>
                        )}
                      </div>

                      <span className="gap-chevron">
                        {isExpanded ? "−" : "+"}
                      </span>
                    </button>

                    {isExpanded && (
                      <div className="gap-details">
                        {gap.prerequisites.length >
                          0 && (
                          <div className="gap-detail-group">
                            <span className="gap-detail-label">
                              PREREQUISITES
                            </span>

                            <div className="learning-topics">
                              {gap.prerequisites.map(
                                (item) => (
                                  <span key={item}>
                                    {item}
                                  </span>
                                )
                              )}
                            </div>
                          </div>
                        )}

                        {gap.learning_topics.length >
                          0 && (
                          <div className="gap-detail-group">
                            <span className="gap-detail-label">
                              WHAT TO LEARN
                            </span>

                            <div className="learning-topics">
                              {gap.learning_topics.map(
                                (topic) => (
                                  <span key={topic}>
                                    {topic}
                                  </span>
                                )
                              )}
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </article>
                );
              }
            )}
          </div>
        </section>
      )}

      {/* Career recommendations */}

      {analysis.careerRecommendations.length > 0 && (
        <section className="results-section">
          <div className="section-heading">
            <div>
              <span className="eyebrow">
                CAREER DIRECTIONS
              </span>

              <h2>Roles that fit your profile</h2>

              <p>
                These recommendations are based on the
                skills detected in your resume.
              </p>
            </div>
          </div>

          <div className="career-list">
            {analysis.careerRecommendations.map(
              (recommendation, index) => {
                const score =
                  recommendation.match_percentage ??
                  0;

                return (
                  <article
                    className={`career-row ${
                      index === 0
                        ? "top-career"
                        : ""
                    }`}
                    key={recommendation.role}
                  >
                    <div className="career-rank">
                      {String(index + 1).padStart(
                        2,
                        "0"
                      )}
                    </div>

                    <div className="career-info">
                      <div className="career-title-row">
                        <h3>
                          {recommendation.role}
                        </h3>

                        {index === 0 && (
                          <span className="best-fit-badge">
                            Best fit
                          </span>
                        )}
                      </div>

                      <div className="career-bar">
                        <div
                          className="career-bar-fill"
                          style={{
                            width: `${Math.min(
                              score,
                              100
                            )}%`,
                          }}
                        />
                      </div>
                    </div>

                    <div className="career-score-block">
                      <strong className="career-score">
                        {score}%
                      </strong>

                      <span>match</span>
                    </div>
                  </article>
                );
              }
            )}
          </div>
        </section>
      )}

      {/* Detected skills */}

      <section className="results-section">
        <div className="section-heading">
          <div>
            <span className="eyebrow">
              YOUR PROFILE
            </span>

            <h2>Detected skills</h2>

            <p>
              Skills identified from your resume.
            </p>
          </div>
        </div>

        {analysis.resumeSkills.length > 0 ? (
          <div className="detected-skills">
            {analysis.resumeSkills.map((skill) => (
              <span key={skill}>{skill}</span>
            ))}
          </div>
        ) : (
          <p className="empty-state">
            No supported skills were detected in
            the uploaded resume.
          </p>
        )}
      </section>
    </section>
  );
};

export default AnalysisResults;