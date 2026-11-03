import { useCallback, useEffect, useState } from 'react';

const API_BASE_URL = 'http://localhost:8000/api/v1';

type Summary = {
  jobs_discovered: number;
  jobs_matching: number;
  applications_in_progress: number;
  accepted: number;
  pending_approval: number;
};

type Application = {
  id: string;
  company: string;
  role: string;
  source: string;
  status: string;
  status_message?: string;
  job_url?: string | null;
  match_score?: number;
};

type DashboardPayload = {
  summary: Summary;
  approval_queue: Application[];
};

type AutoApplySettings = {
  min_score: number;
  max_jobs: number;
  headless: boolean;
  sources: string;
};

const emptySummary: Summary = {
  jobs_discovered: 0,
  jobs_matching: 0,
  applications_in_progress: 0,
  accepted: 0,
  pending_approval: 0,
};

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? `Request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}

export default function App() {
  const [summary, setSummary] = useState<Summary>(emptySummary);
  const [queue, setQueue] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState(false);
  const [autoApplying, setAutoApplying] = useState(false);
  const [busyApplicationId, setBusyApplicationId] = useState<string | null>(null);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [autoApplySettings, setAutoApplySettings] = useState<AutoApplySettings>({
    min_score: 0.65,
    max_jobs: 10,
    headless: false,
    sources: '',
  });

  const loadDashboard = useCallback(async () => {
    const payload = await requestJson<DashboardPayload>('/dashboard/summary');
    setSummary(payload.summary);
    setQueue(payload.approval_queue);
  }, []);

  useEffect(() => {
    loadDashboard()
      .catch((loadError: unknown) => {
        setError(loadError instanceof Error ? loadError.message : 'Could not load dashboard.');
      })
      .finally(() => setLoading(false));
  }, [loadDashboard]);

  const startApplying = async () => {
    setStarting(true);
    setError('');
    setNotice('');
    try {
      const result = await requestJson<{
        message: string;
        jobs_evaluated: number;
        applications_created: number;
      }>('/applications/start', { method: 'POST' });
      setNotice(
        `${result.message} Checked ${result.jobs_evaluated} listings; prepared ${result.applications_created} application(s).`,
      );
      await loadDashboard();
    } catch (startError: unknown) {
      setError(startError instanceof Error ? startError.message : 'Could not start the application workflow.');
    } finally {
      setStarting(false);
    }
  };

  const approveApplication = async (applicationId: string) => {
    setBusyApplicationId(applicationId);
    setError('');
    try {
      await requestJson(`/applications/${applicationId}/approve`, { method: 'POST' });
      setNotice('Application approved. It is ready for the separate submission step.');
      await loadDashboard();
    } catch (approveError: unknown) {
      setError(approveError instanceof Error ? approveError.message : 'Could not approve this application.');
    } finally {
      setBusyApplicationId(null);
    }
  };

  const startAutoApply = async () => {
    setAutoApplying(true);
    setError('');
    setNotice('');
    setShowSettings(false);
    try {
      const params = new URLSearchParams({
        min_score: autoApplySettings.min_score.toString(),
        max_jobs: autoApplySettings.max_jobs.toString(),
        headless: autoApplySettings.headless.toString(),
      });
      if (autoApplySettings.sources) {
        params.append('sources', autoApplySettings.sources);
      }

      const result = await requestJson<{
        status: string;
        message: string;
        jobs_evaluated: number;
        jobs_matched: number;
        applications_submitted: number;
        applications: Array<{
          status: string;
          job_title: string;
          company: string;
        }>;
      }>(`/applications/auto-apply?${params.toString()}`, { method: 'POST' });

      const successful = result.applications?.filter(a => a.status === 'submitted').length || 0;
      setNotice(
        `Auto-apply completed! Evaluated ${result.jobs_evaluated} jobs, matched ${result.jobs_matched}, successfully submitted ${successful} applications.`
      );
      await loadDashboard();
    } catch (autoError: unknown) {
      setError(autoError instanceof Error ? autoError.message : 'Auto-apply failed. Check backend logs for details.');
    } finally {
      setAutoApplying(false);
    }
  };

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">PERSONAL JOB SEARCH</p>
          <h1>Huntify</h1>
          <p className="subtitle">Find relevant roles and prepare applications from your base resume.</p>
        </div>
        <div className="header-actions">
          <button className="secondary-button" onClick={startApplying} disabled={starting || autoApplying}>
            {starting ? 'Preparing…' : 'Prepare Applications'}
          </button>
          <button
            className="action-button auto-apply-button"
            onClick={() => setShowSettings(!showSettings)}
            disabled={starting || autoApplying}
          >
            {autoApplying ? '🤖 Auto-applying…' : '🤖 Auto-Apply'}
          </button>
        </div>
      </header>

      {showSettings && (
        <section className="card settings-panel">
          <h3>Auto-Apply Settings</h3>
          <div className="settings-grid">
            <div className="setting-item">
              <label htmlFor="max-jobs">Maximum Jobs</label>
              <input
                id="max-jobs"
                type="number"
                min="1"
                max="50"
                value={autoApplySettings.max_jobs}
                onChange={(e) => setAutoApplySettings({ ...autoApplySettings, max_jobs: parseInt(e.target.value) || 10 })}
              />
            </div>
            <div className="setting-item">
              <label htmlFor="min-score">Minimum Match Score</label>
              <input
                id="min-score"
                type="number"
                min="0"
                max="1"
                step="0.05"
                value={autoApplySettings.min_score}
                onChange={(e) => setAutoApplySettings({ ...autoApplySettings, min_score: parseFloat(e.target.value) || 0.65 })}
              />
            </div>
            <div className="setting-item">
              <label htmlFor="sources">Job Sources (comma-separated)</label>
              <input
                id="sources"
                type="text"
                placeholder="LinkedIn,Naukri,Indeed or leave empty for all"
                value={autoApplySettings.sources}
                onChange={(e) => setAutoApplySettings({ ...autoApplySettings, sources: e.target.value })}
              />
            </div>
            <div className="setting-item checkbox-item">
              <label htmlFor="headless">
                <input
                  id="headless"
                  type="checkbox"
                  checked={autoApplySettings.headless}
                  onChange={(e) => setAutoApplySettings({ ...autoApplySettings, headless: e.target.checked })}
                />
                Run in headless mode (hidden browser)
              </label>
            </div>
          </div>
          <div className="settings-actions">
            <button className="secondary-button" onClick={() => setShowSettings(false)}>Cancel</button>
            <button className="action-button" onClick={startAutoApply} disabled={autoApplying}>
              {autoApplying ? 'Running…' : 'Start Auto-Apply'}
            </button>
          </div>
        </section>
      )}

      <p className="workflow-note">
        <strong>Prepare Applications:</strong> Discovers jobs, matches them to your resume, and prepares tailored applications for manual review.<br />
        <strong>Auto-Apply:</strong> Fully automated workflow that finds jobs, tailors resumes, and submits applications automatically using browser automation.
      </p>

      {error && <div className="notice error" role="alert">{error}</div>}
      {notice && <div className="notice success" role="status">{notice}</div>}

      <section className="summary-grid" aria-label="Application summary">
        <div className="card">
          <h2>Jobs discovered</h2>
          <p className="stat">{summary.jobs_discovered}</p>
        </div>
        <div className="card">
          <h2>Applications prepared</h2>
          <p className="stat">{summary.jobs_matching}</p>
        </div>
        <div className="card">
          <h2>In progress</h2>
          <p className="stat">{summary.applications_in_progress}</p>
        </div>
        <div className="card">
          <h2>Approved</h2>
          <p className="stat">{summary.accepted}</p>
        </div>
        <div className="card">
          <h2>Awaiting approval</h2>
          <p className="stat">{summary.pending_approval}</p>
        </div>
      </section>

      <section className="card queue" aria-labelledby="queue-title">
        <div className="section-heading">
          <div>
            <p className="eyebrow">REVIEW MATCHES</p>
            <h2 id="queue-title">Application queue</h2>
          </div>
          <button className="secondary-button" onClick={() => {
            setError('');
            loadDashboard().catch((loadError: unknown) => {
              setError(loadError instanceof Error ? loadError.message : 'Could not refresh the queue.');
            });
          }}>
            Refresh
          </button>
        </div>

        {loading ? (
          <p className="empty-state">Loading your application queue…</p>
        ) : queue.length === 0 ? (
          <div className="empty-state">
            <strong>No applications yet</strong>
            <p>Choose “Start applying” to run the backend job-matching workflow.</p>
          </div>
        ) : (
          <div className="queue-list">
            {queue.map((application) => (
              <article className="job-row" key={application.id}>
                <div className="job-details">
                  <strong>{application.role}</strong>
                  <span>{application.company} · {application.source}</span>
                  {application.status_message && <small>{application.status_message}</small>}
                </div>
                <div className="inline-actions">
                  {typeof application.match_score === 'number' && (
                    <span className="badge">{Math.round(application.match_score * 100)}% match</span>
                  )}
                  <span className={`badge status-${application.status}`}>{application.status.replace(/_/g, ' ')}</span>
                  {application.job_url && (
                    <a className="secondary-button" href={application.job_url} target="_blank" rel="noreferrer">
                      View job
                    </a>
                  )}
                  {application.status === 'pending_review' && (
                    <button
                      className="secondary-button approve-button"
                      onClick={() => approveApplication(application.id)}
                      disabled={busyApplicationId === application.id}
                    >
                      {busyApplicationId === application.id ? 'Approving…' : 'Approve'}
                    </button>
                  )}
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
