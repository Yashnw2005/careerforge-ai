import api from "./api";

export interface SkillGap {
  skill: string;
  priority?: string;
  category?: string;
  reason?: string;
  prerequisites: string[];
  learning_topics: string[];
}

export interface CareerRecommendation {
  role: string;
  category?: string;
  match_percentage?: number;
  skill_match_percentage?: number;
  semantic_match_percentage?: number;
  matched_skills: string[];
  missing_skills: string[];
}

export interface Analysis {
  id: string;
  resumeFilename: string;
  jobDescription: string;
  requiredSkills: string[];
  resumeSkills: string[];

  overallMatchPercentage: number;
  textSimilarity: number;
  semanticSimilarity: number;
  skillMatchPercentage: number;

  matchedSkills: string[];
  missingSkills: string[];

  skillGapAnalysis: SkillGap[];
  careerRecommendations: CareerRecommendation[];

  createdAt: string;
}

interface AnalysisResponse {
  success: boolean;
  analysisId: string;
  analysis: Analysis;
}

interface AnalysisHistoryResponse {
  success: boolean;
  count: number;
  analyses: Array<{
    _id: string;
    resumeFilename: string;
    overallMatchPercentage: number;
    skillMatchPercentage: number;
    createdAt: string;
  }>;
}

interface SingleAnalysisResponse {
  success: boolean;
  analysis: Analysis;
}

export const analyzeResume = async (
  file: File,
  jobDescription: string,
  requiredSkills: string[]
): Promise<Analysis> => {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("jobDescription", jobDescription);
  formData.append(
    "requiredSkills",
    JSON.stringify(requiredSkills)
  );

  const response =
    await api.post<AnalysisResponse>(
      "/analysis",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

  return response.data.analysis;
};

export const getAnalysisHistory =
  async () => {
    const response =
      await api.get<AnalysisHistoryResponse>(
        "/analysis"
      );

    return response.data.analyses;
  };

export const getAnalysisById = async (
  id: string
): Promise<Analysis> => {
  const response =
    await api.get<SingleAnalysisResponse>(
      `/analysis/${id}`
    );

  return response.data.analysis;
};