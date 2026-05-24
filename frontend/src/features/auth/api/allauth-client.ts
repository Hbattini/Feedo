type SessionResponse = {
  viewer: {
    publicId: string;
    email: string;
  } | null;
};

const allauthBaseUrl = import.meta.env.VITE_ALLAUTH_BASE_URL ?? "http://localhost:8000/_allauth/";

export async function fetchSession(): Promise<SessionResponse> {
  const response = await fetch(`${allauthBaseUrl}browser/v1/auth/session`, {
    credentials: "include"
  });
  if (!response.ok) {
    return { viewer: null };
  }
  return { viewer: null };
}
