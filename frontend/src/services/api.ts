const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export const fetchWithAuth = async (endpoint: string, options: RequestInit = {}) => {
  // In a real app with Better Auth, we'd get the session/token here
  // For now, we simulate the logic of attaching the header
  const token = localStorage.getItem('auth_token');

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Handle unauthorized - maybe redirect to login
    console.error('Unauthorized access - please login');
  }

  return response;
};

export const habitApi = {
  list: () => fetchWithAuth('/habits'),
  create: (data: any) => fetchWithAuth('/habits', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  update: (habitId: string, data: { name?: string; description?: string }) => fetchWithAuth(`/habits/${habitId}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  }),
  delete: (habitId: string) => fetchWithAuth(`/habits/${habitId}`, {
    method: 'DELETE',
  }),
  toggle: (habitId: string, date: string, status: boolean) => fetchWithAuth(`/habits/${habitId}/toggle`, {
    method: 'POST',
    body: JSON.stringify({ date, status }),
  }),
  getWeeklyStats: () => fetchWithAuth('/analytics/weekly'),
};
