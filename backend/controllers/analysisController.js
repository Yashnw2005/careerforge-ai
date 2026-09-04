const { analyzeResume } = require("../services/mlService");
const Analysis = require("../models/Analysis");

const analyzeResumeForJob = async (req, res) => {
  try {
    const {
      jobDescription,
      requiredSkills,
    } = req.body;

    // Validate job description
    if (!jobDescription || !jobDescription.trim()) {
      return res.status(400).json({
        success: false,
        message: "Job description is required",
      });
    }

    // Parse required skills
    let parsedRequiredSkills;

    if (Array.isArray(requiredSkills)) {
      parsedRequiredSkills = requiredSkills;
    } else if (typeof requiredSkills === "string") {
      const trimmedSkills = requiredSkills.trim();

      try {
        const parsed = JSON.parse(trimmedSkills);

        if (Array.isArray(parsed)) {
          parsedRequiredSkills = parsed;
        }
      } catch (error) {
        parsedRequiredSkills = trimmedSkills
          .replace(/^\[/, "")
          .replace(/\]$/, "")
          .split(",")
          .map((skill) =>
            skill
              .trim()
              .replace(/^["']|["']$/g, "")
              .toLowerCase()
          )
          .filter(Boolean);
      }
    }

    if (
      !Array.isArray(parsedRequiredSkills) ||
      parsedRequiredSkills.length === 0
    ) {
      return res.status(400).json({
        success: false,
        message: "Required skills are required",
      });
    }

    // Validate resume
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: "Resume PDF is required",
      });
    }

    if (req.file.mimetype !== "application/pdf") {
      return res.status(400).json({
        success: false,
        message: "Only PDF files are supported",
      });
    }

    // Send data to ML service
    const mlResponse = await analyzeResume(
      req.file.buffer,
      req.file.originalname,
      jobDescription,
      parsedRequiredSkills
    );

    if (
      !mlResponse ||
      mlResponse.success !== true
    ) {
      return res.status(502).json({
        success: false,
        message: "Invalid response from ML service",
      });
    }

    // Extract ML analysis
    const analysis = mlResponse;

    // Persist analysis in MongoDB
    const savedAnalysis = await Analysis.create({
      user: req.user._id,

      resumeFilename: analysis.filename,

      jobDescription,

      requiredSkills:
        analysis.job_required_skills,

      resumeSkills:
        analysis.resume_skills,

      overallMatchPercentage:
        analysis.overall_match_percentage,

      textSimilarity:
        analysis.text_similarity,

      semanticSimilarity:
        analysis.semantic_similarity,

      skillMatchPercentage:
        analysis.skill_match_percentage,

      matchedSkills:
        analysis.matched_skills,

      missingSkills:
        analysis.missing_skills,

      skillGapAnalysis:
        analysis.skill_gap_analysis,

      careerRecommendations:
        analysis.career_recommendations,
    });

    return res.status(201).json({
      success: true,

      analysisId: savedAnalysis._id,

      analysis: {
        id: savedAnalysis._id,
        resumeFilename:
          savedAnalysis.resumeFilename,
        jobDescription:
          savedAnalysis.jobDescription,
        requiredSkills:
          savedAnalysis.requiredSkills,
        resumeSkills:
          savedAnalysis.resumeSkills,
        overallMatchPercentage:
          savedAnalysis.overallMatchPercentage,
        textSimilarity:
          savedAnalysis.textSimilarity,
        semanticSimilarity:
          savedAnalysis.semanticSimilarity,
        skillMatchPercentage:
          savedAnalysis.skillMatchPercentage,
        matchedSkills:
          savedAnalysis.matchedSkills,
        missingSkills:
          savedAnalysis.missingSkills,
        skillGapAnalysis:
          savedAnalysis.skillGapAnalysis,
        careerRecommendations:
          savedAnalysis.careerRecommendations,
        createdAt:
          savedAnalysis.createdAt,
      },
    });
  } catch (error) {
    console.error(
      "Resume analysis error:",
      error.response?.data || error.message
    );

    return res.status(502).json({
      success: false,
      message: "ML service analysis failed",
    });
  }
};

const getAnalysisHistory = async (req, res) => {
  try {
    const analyses = await Analysis.find({
      user: req.user._id,
    })
      .sort({ createdAt: -1 })
      .select(
        "resumeFilename overallMatchPercentage skillMatchPercentage createdAt"
      );

    return res.status(200).json({
      success: true,
      count: analyses.length,
      analyses,
    });
  } catch (error) {
    console.error(
      "Analysis history error:",
      error.message
    );

    return res.status(500).json({
      success: false,
      message: "Failed to fetch analysis history",
    });
  }
};

const getAnalysisById = async (req, res) => {
  try {
    const analysis = await Analysis.findOne({
      _id: req.params.id,
      user: req.user._id,
    });

    if (!analysis) {
      return res.status(404).json({
        success: false,
        message: "Analysis not found",
      });
    }

    return res.status(200).json({
      success: true,
      analysis,
    });
  } catch (error) {
    console.error(
      "Analysis retrieval error:",
      error.message
    );

    return res.status(500).json({
      success: false,
      message: "Failed to fetch analysis",
    });
  }
};

module.exports = {
  analyzeResumeForJob,
  getAnalysisHistory,
  getAnalysisById,
};