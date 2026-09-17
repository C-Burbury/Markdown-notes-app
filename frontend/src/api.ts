const baseURL = import.meta.env.VITE_API_BASE_URL;

export class ApiError extends Error {
    status: number;
    detail: string;

    constructor(status: number, detail: string) {
        super(detail);
        this.status = status;
        this.detail = detail;
    }
}

let unauthorizedHandler: (() => void) | null = null;
export function setUnauthorizedHandler(fn: () => void) {
  unauthorizedHandler = fn;
}

export async function apiFetch<T>(path: string, opts?: RequestInit){
    const authKey = localStorage.getItem('token')
    const fullURL = baseURL + path;

        const response = await fetch(fullURL, {...opts, headers: {'Content-Type': 'application/json', ...(authKey ? { Authorization: `Bearer ${authKey}` } : {})}})
        if (!response.ok) {
            const raw = await response.text();
            let detail: string;
            try {
                detail = JSON.parse(raw).detail ?? raw;
            } catch {
                detail = raw;
            }
            if (response.status === 401) {
                unauthorizedHandler?.();
                }
            throw new ApiError(response.status, detail);
        }

        const result = await response.json();
        return result as T;
}