import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const ProtectedRoute = () => {
  const { user, loading } = useAuth();

  // Wait while we check whether a session exists
  if (loading) {
    return <div>Loading CareerForge AI...</div>;
  }

  // No authenticated user → send to login
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Authenticated → allow the requested page
  return <Outlet />;
};

export default ProtectedRoute;