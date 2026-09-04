const mongoose = require("mongoose");

const skillGapSchema = new mongoose.Schema(
  {
    skill: {
      type: String,
      required: true,
    },
    priority: {
      type: String,
    },
    category: {
      type: String,
    },
    reason: {
      type: String,
    },
    prerequisites: {
      type: [String],
      default: [],
    },
    learning_topics: {
      type: [String],
      default: [],
    },
  },
  { _id: false }
);

const careerRecommendationSchema = new mongoose.Schema(
  {
    role: {
      type: String,
      required: true,
    },
    category: {
      type: String,
    },
    match_percentage: {
      type: Number,
    },
    skill_match_percentage: {
      type: Number,
    },
    semantic_match_percentage: {
      type: Number,
    },
    matched_skills: {
      type: [String],
      default: [],
    },
    missing_skills: {
      type: [String],
      default: [],
    },
  },
  { _id: false }
);

const analysisSchema = new mongoose.Schema(
  {
    user: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "User",
      required: true,
      index: true,
    },

    resumeFilename: {
      type: String,
      required: true,
    },

    jobDescription: {
      type: String,
      required: true,
    },

    requiredSkills: {
      type: [String],
      default: [],
    },

    resumeSkills: {
      type: [String],
      default: [],
    },

    overallMatchPercentage: {
      type: Number,
      required: true,
    },

    textSimilarity: {
      type: Number,
      required: true,
    },

    semanticSimilarity: {
      type: Number,
      required: true,
    },

    skillMatchPercentage: {
      type: Number,
      required: true,
    },

    matchedSkills: {
      type: [String],
      default: [],
    },

    missingSkills: {
      type: [String],
      default: [],
    },

    skillGapAnalysis: {
      type: [skillGapSchema],
      default: [],
    },

    careerRecommendations: {
      type: [careerRecommendationSchema],
      default: [],
    },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model(
  "Analysis",
  analysisSchema
);