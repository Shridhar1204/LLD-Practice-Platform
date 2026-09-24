const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
export async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API}${path}`, { ...options, headers: { 'Content-Type':'application/json', ...(options?.headers || {}) } });
  if (!res.ok) throw new Error((await res.json().catch(()=>({detail:'Request failed'}))).detail || 'Request failed');
  return res.json();
}
export type Problem = { id:string; title:string; difficulty:string; time:string; tags:string[]; description:string; requirements:string[]; evaluation_focus:string[] };
export type Attempt = { id:string; problem_id:string; status:string; created_at:string; submission:any; evaluation:any };
