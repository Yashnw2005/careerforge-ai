const axios = require("axios");
const FormData = require("form-data");

const ML_SERVICE_URL =
  process.env.ML_SERVICE_URL || "http://127.0.0.1:8000";

/**
 * Send a resume PDF and job information
 * to the Python FastAPI ML service.
 */
const analyzeResume = async (
  fileBuffer,
  filename,
  jobDescription,
  requiredSkills
) => {
  const formData = new FormData();

  formData.append(
    "file",
    fileBuffer,
    {
      filename,
      contentType: "application/pdf",
    }
  );

  formData.append(
    "job_description",
    jobDescription
  );

  formData.append(
    "required_skills",
    requiredSkills.join(",")
  );

  const response = await axios.post(
    `${ML_SERVICE_URL}/api/analyze-resume-job`,
    formData,
    {
      headers: {
        ...formData.getHeaders(),
      },
      maxContentLength: 10 * 1024 * 1024,
      maxBodyLength: 10 * 1024 * 1024,
      timeout: 120000,
    }
  );

  return response.data;
};

module.exports = {
  analyzeResume,
};