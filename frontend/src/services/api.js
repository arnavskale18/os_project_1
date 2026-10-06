const API_BASE = 'http://localhost:8000';

async function fetchJson(endpoint, options = {}) {
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`API Error ${res.status}: ${err}`);
    }
    return await res.json();
  } catch (err) {
    console.error(`Fetch error on ${endpoint}:`, err);
    throw err;
  }
}

export const api = {
  createSimulation: (params) => fetchJson('/simulation/create', { method: 'POST', body: JSON.stringify(params) }),
  startSimulation: () => fetchJson('/simulation/start', { method: 'POST' }),
  pauseSimulation: () => fetchJson('/simulation/pause', { method: 'POST' }),
  resetSimulation: () => fetchJson('/simulation/reset', { method: 'POST' }),
  stepSimulation: () => fetchJson('/simulation/step', { method: 'POST' }),
  getState: () => fetchJson('/simulation/state'),
  evaluateRequest: (pid, request) => fetchJson('/request/evaluate', { method: 'POST', body: JSON.stringify({ pid, request }) }),
  runExperiment: (scenario, maxTicks = 50) => fetchJson('/experiment/run', { method: 'POST', body: JSON.stringify({ scenario, max_ticks: maxTicks }) }),
};
