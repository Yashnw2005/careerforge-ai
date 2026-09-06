import { useAuth } from "../context/AuthContext";

interface NavbarProps {
  onReset?: () => void;
}

const Navbar = ({ onReset }: NavbarProps) => {
  const { user, logout } = useAuth();

  return (
    <header className="dashboard-header">
      <div className="brand">
        <button
          type="button"
          className="brand-button"
          onClick={onReset}
          aria-label="Go to dashboard home"
        >
          <span className="brand-mark">C</span>

          <span className="brand-name">
            CareerForge
          </span>

          <span className="brand-badge">
            AI
          </span>
        </button>
      </div>

      <div className="user-area">
        <span className="user-name">
          {user?.name || "User"}
        </span>

        <button
          type="button"
          className="logout-button"
          onClick={logout}
        >
          Sign out
        </button>
      </div>
    </header>
  );
};

export default Navbar;