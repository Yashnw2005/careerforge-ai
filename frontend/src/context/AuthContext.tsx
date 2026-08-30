import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import api from "../services/api";
import type {
  User,
  LoginCredentials,
  RegisterData,
} from "../types/auth";

interface AuthContextType {
  user: User | null;
  token: string | null;
  loading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export const AuthProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("careerforge_token")
  );
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedToken = localStorage.getItem("careerforge_token");

    if (!storedToken) {
      setLoading(false);
      return;
    }

    const fetchCurrentUser = async () => {
      try {
        const response = await api.get("/users/me");

        setUser(response.data.user);
      } catch (error) {
        console.error("Session validation failed:", error);

        localStorage.removeItem("careerforge_token");
        setToken(null);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    fetchCurrentUser();
  }, []);

  const login = async (credentials: LoginCredentials) => {
    const response = await api.post("/auth/login", credentials);

    const { token: newToken, user: loggedInUser } =
      response.data;

    localStorage.setItem("careerforge_token", newToken);

    setToken(newToken);
    setUser(loggedInUser);
  };

  const register = async (data: RegisterData) => {
    const response = await api.post("/auth/register", data);

    const { token: newToken, user: registeredUser } =
      response.data;

    localStorage.setItem("careerforge_token", newToken);

    setToken(newToken);
    setUser(registeredUser);
  };

  const logout = () => {
    localStorage.removeItem("careerforge_token");

    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider"
    );
  }

  return context;
};