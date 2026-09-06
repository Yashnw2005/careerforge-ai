import {
  useRef,
  useState,
  type ChangeEvent,
  type FormEvent,
} from "react";

interface AnalysisFormProps {
  loading: boolean;
  error: string;
  onSubmit: (
    file: File,
    jobDescription: string,
    requiredSkills: string[]
  ) => Promise<void>;
}

const AnalysisForm = ({
  loading,
  error,
  onSubmit,
}: AnalysisFormProps) => {
  const fileInputRef =
    useRef<HTMLInputElement>(null);

  const [resumeFile, setResumeFile] =
    useState<File | null>(null);

  const [jobDescription, setJobDescription] =
    useState("");

  const [requiredSkills, setRequiredSkills] =
    useState("");

  const [dragging, setDragging] =
    useState(false);

  const validateFile = (
    file: File
  ): boolean => {
    if (file.type !== "application/pdf") {
      return false;
    }

    if (file.size > 5 * 1024 * 1024) {
      return false;
    }

    return true;
  };

  const selectFile = (file?: File) => {
    if (!file) {
      return;
    }

    if (!validateFile(file)) {
      return;
    }

    setResumeFile(file);
  };

  const handleFileChange = (
    event: ChangeEvent<HTMLInputElement>
  ) => {
    selectFile(event.target.files?.[0]);
  };

  const handleDrop = (
    event: React.DragEvent<HTMLDivElement>
  ) => {
    event.preventDefault();
    setDragging(false);

    selectFile(event.dataTransfer.files?.[0]);
  };

  const handleSubmit = async (
    event: FormEvent<HTMLFormElement>
  ) => {
    event.preventDefault();

    if (!resumeFile) {
      return;
    }

    const skills = requiredSkills
      .split(",")
      .map((skill) => skill.trim())
      .filter(Boolean);

    if (!jobDescription.trim() || skills.length === 0) {
      return;
    }

    await onSubmit(
      resumeFile,
      jobDescription.trim(),
      skills
    );
  };

  const removeFile = () => {
    setResumeFile(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const canSubmit =
    !loading &&
    resumeFile !== null &&
    jobDescription.trim().length > 0 &&
    requiredSkills
      .split(",")
      .map((skill) => skill.trim())
      .filter(Boolean).length > 0;

  return (
    <section className="analysis-card">
      <div className="analysis-card-header">
        <div>
          <span className="eyebrow">
            ROLE FIT ANALYSIS
          </span>

          <h2>
            Understand your fit for the role.
          </h2>

          <p>
            Compare your experience with a target
            position and see exactly where you stand.
          </p>
        </div>
      </div>

      <form
        className="analysis-form"
        onSubmit={handleSubmit}
      >
        <div className="field">
          <label htmlFor="resume">
            Your resume
          </label>

          <div
            className={`resume-dropzone ${
              dragging ? "dragging" : ""
            } ${
              resumeFile ? "has-file" : ""
            }`}
            onDragOver={(event) => {
              event.preventDefault();
              setDragging(true);
            }}
            onDragLeave={() =>
              setDragging(false)
            }
            onDrop={handleDrop}
            onClick={() =>
              fileInputRef.current?.click()
            }
            role="button"
            tabIndex={0}
            onKeyDown={(event) => {
              if (
                event.key === "Enter" ||
                event.key === " "
              ) {
                fileInputRef.current?.click();
              }
            }}
          >
            <input
              ref={fileInputRef}
              id="resume"
              type="file"
              accept=".pdf,application/pdf"
              onChange={handleFileChange}
              hidden
            />

            {!resumeFile ? (
              <>
                <div className="upload-icon">
                  ↑
                </div>

                <div>
                  <strong>
                    Drop your resume here
                  </strong>

                  <p>
                    or click to choose a PDF
                  </p>
                </div>
              </>
            ) : (
              <>
                <div className="file-icon">
                  PDF
                </div>

                <div className="selected-file">
                  <strong>
                    {resumeFile.name}
                  </strong>

                  <span>
                    {(resumeFile.size / 1024 / 1024).toFixed(
                      2
                    )}{" "}
                    MB
                  </span>
                </div>

                <button
                  type="button"
                  className="remove-file"
                  onClick={(event) => {
                    event.stopPropagation();
                    removeFile();
                  }}
                >
                  Remove
                </button>
              </>
            )}
          </div>

          <span className="field-help">
            PDF only · Maximum 5 MB
          </span>
        </div>

        <div className="field">
          <label htmlFor="jobDescription">
            Target job description
          </label>

          <textarea
            id="jobDescription"
            value={jobDescription}
            onChange={(event) =>
              setJobDescription(
                event.target.value
              )
            }
            placeholder="Paste the job description you're targeting..."
            rows={8}
          />
        </div>

        <div className="field">
          <label htmlFor="requiredSkills">
            Required skills
          </label>

          <input
            id="requiredSkills"
            type="text"
            value={requiredSkills}
            onChange={(event) =>
              setRequiredSkills(
                event.target.value
              )
            }
            placeholder="Python, FastAPI, SQL, Docker, Git"
          />

          <span className="field-help">
            Separate skills with commas.
          </span>
        </div>

        {error && (
          <div
            className="error-message"
            role="alert"
          >
            {error}
          </div>
        )}

        <div className="analysis-submit-row">
          <div className="analysis-note">
            <span>✦</span>
            Analysis combines skills and semantic
            similarity.
          </div>

          <button
            type="submit"
            className="primary-button"
            disabled={!canSubmit}
          >
            {loading
              ? "Analyzing..."
              : "Analyze fit →"}
          </button>
        </div>
      </form>
    </section>
  );
};

export default AnalysisForm;