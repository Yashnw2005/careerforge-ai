const express = require("express");
const multer = require("multer");

const protect = require("../middleware/authMiddleware");

const {
  analyzeResumeForJob,
  getAnalysisHistory,
  getAnalysisById,
} = require("../controllers/analysisController");

const router = express.Router();

const upload = multer({
  storage: multer.memoryStorage(),

  limits: {
    fileSize: 5 * 1024 * 1024,
  },
});

// Create new analysis
router.post(
  "/",
  protect,
  upload.single("file"),
  analyzeResumeForJob
);

// Get logged-in user's analysis history
router.get(
  "/",
  protect,
  getAnalysisHistory
);

// Get one analysis belonging to logged-in user
router.get(
  "/:id",
  protect,
  getAnalysisById
);

module.exports = router;