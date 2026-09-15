import {useState, useEffect } from "react";
import {setUnauthorizedHandler } from "./api"
import {AuthContext} from "./AuthContext"

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [token, setToken] = useState<string | null>(() => localStorage.getItem("token"));

    const login = (newToken: string) => {
        localStorage.setItem("token", newToken);
        setToken(newToken);
    };

    const logout = () => {
        localStorage.removeItem("token");
        setToken(null);
        window.location.href = "/login";
    };

    useEffect(() => {
        setUnauthorizedHandler(logout);
    }, []);

    return (
        <AuthContext.Provider value={{ token, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};