
import { useEffect, useState } from "react";
import "./App.css";

// Az adatbázisból érkező álláshirdetés típusa
type Job = {
  id: number;
  title: string;
  company: string;
  location: string;
  description: string | null;
  salary_min: number | null;
  salary_max: number | null;
  salary_currency: string;
  employment_type: string | null;
  work_schedule: string | null;
  remote_type: string | null;
  source: string;
  source_url: string;
  published_at: string | null;
  collected_at: string;
  is_active: boolean;
};

function App() {
  const [apiStatus, setApiStatus] = useState("Kapcsolódás...");
  const [error, setError] = useState("");

  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [jobsError, setJobsError] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/health")
      .then((response) => {
        if (!response.ok) {
          throw new Error("A backend hibás választ adott.");
        }
        return response.json();
      })
      .then((data) => {
        setApiStatus(data.status);
      })
      .catch(() => {
        setError("Nem sikerült elérni a backendet.");
      });

    fetch("http://127.0.0.1:8000/jobs")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Nem sikerült lekérni az állásokat.");
        }
        return response.json();
      })
      .then((data: Job[]) => {
        setJobs(data);
      })
      .catch(() => {
        setJobsError("Az állások betöltése nem sikerült.");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  function formatSalary(job: Job) {
    if (job.salary_min === null && job.salary_max === null) {
      return "Nincs megadva";
    }

    const format = (amount: number) =>
      new Intl.NumberFormat("hu-HU").format(amount);

    if (job.salary_min !== null && job.salary_max !== null) {
      return `${format(job.salary_min)} – ${format(job.salary_max)} ${job.salary_currency}`;
    }

    if (job.salary_min !== null) {
      return `${format(job.salary_min)} ${job.salary_currency}-tól`;
    }

    return `${format(job.salary_max!)} ${job.salary_currency}-ig`;
  }

  return (
    <main>
      <header>
        <h1>JobFinder</h1>
        <p>Álláskereső alkalmazás</p>
      </header>

      <section>
        <h2>Backend kapcsolat</h2>

        {error ? (
          <p>{error}</p>
        ) : (
          <p>API állapot: {apiStatus}</p>
        )}
      </section>

      <section>
        <h2>Álláshirdetések</h2>

        {loading && <p>Állások betöltése...</p>}

        {jobsError && <p>{jobsError}</p>}

        {!loading && !jobsError && jobs.length === 0 && (
          <p>Jelenleg nincs megjeleníthető álláshirdetés.</p>
        )}

        <div className="job-list">
          {jobs.map((job) => (
            <article className="job-card" key={job.id}>
              <h3>{job.title}</h3>

              <p><strong>Cég:</strong> {job.company}</p>
              <p><strong>Helyszín:</strong> {job.location}</p>
              <p><strong>Fizetés:</strong> {formatSalary(job)}</p>
              <p>
                <strong>Foglalkoztatás:</strong>{" "}
                {job.employment_type ?? "Nincs megadva"}
              </p>
              <p>
                <strong>Munkarend:</strong>{" "}
                {job.work_schedule ?? "Nincs megadva"}
              </p>
              <p>
                <strong>Munkavégzés:</strong>{" "}
                {job.remote_type ?? "Nincs megadva"}
              </p>
              <p><strong>Forrás:</strong> {job.source}</p>

              {job.description && (
                <p className="job-description">{job.description}</p>
              )}

              <a
                href={job.source_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                Eredeti hirdetés megnyitása
              </a>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

export default App;
