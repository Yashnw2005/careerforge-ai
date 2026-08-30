import { useAuth } from "../context/AuthContext";

const Dashboard = () => {
  const { user, logout } = useAuth();

  return (
    <div>
      <header>
        <h1>CareerForge AI</h1>

        <div>
          <span>
            Welcome, {user?.name || "User"}
          </span>

          <button onClick={logout}>
            Logout
          </button>
        </div>
      </header>

      <main>
        <h2>Your Career Dashboard</h2>

        <p>
          Welcome to CareerForge AI. Your personalized
          career journey starts here.
        </p>

        <div>
          <h3>Career Profile</h3>
          <p>Complete your profile to get started.</p>
        </div>

        <div>
          <h3>AI Career Analysis</h3>
          <p>
            Analyze your skills and discover suitable
            career paths.
          </p>
        </div>

        <div>
          <h3>Learning Roadmap</h3>
          <p>
            Generate a personalized learning roadmap.
          </p>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
