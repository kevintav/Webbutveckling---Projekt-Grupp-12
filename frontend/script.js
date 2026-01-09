
const API_BASE = "http://127.0.0.1:8000";
const SEARCH_ENDPOINT = "/api/search";

const form = document.getElementById("searchForm");
const resultsEl = document.getElementById("results");

const salaryPanel = document.getElementById("salaryPanel");
const salaryContent = document.getElementById("salaryContent");

function setLoading() {
  resultsEl.innerHTML = `
    <div class="status-msg"><p>Hämtar platsannonser…</p></div>
  `;
  salaryPanel.classList.remove("hidden");
  salaryContent.innerHTML = `<p>Hämtar lönestatistik…</p>`;
}

function setError(message) {
  resultsEl.innerHTML = `
    <div class="status-msg"><p>${message}</p></div>
  `;
  salaryContent.innerHTML = `<p>Ingen löninfo kunde hämtas.</p>`;
}

function renderSalary({ q, location, salary }) {
    const belopp = salary?.value || "Saknas";
    
    salaryContent.innerHTML = `
      <p><strong>Yrke:</strong> ${q}</p>
      <p><strong>Ort:</strong> ${location}</p>
      <p><strong>Snittlön:</strong> ${belopp} kr</p>
    `;
  }

  function renderJobs(jobs) {
    if (!Array.isArray(jobs) || jobs.length === 0) {
      resultsEl.innerHTML = `
        <div class="status-msg"><p>Inga platsannonser hittades.</p></div>
      `;
      return;
    }
  
    const cards = jobs.map(job => {
      const title = job.title || job.yrkestitel || "Okänd titel";
      const employer = job.employer || job.arbetsgivare || "";
      const location = job.location || job.ort || "";
      const published = job.published || job.publicerad || "";
      const url = job.url || job.annons_url || job.link || "";
  
      return `
        <article class="job-card">
          <div class="job-title">${title}</div> 
  
          <div class="job-meta">
            ${employer ? `<span class="badge">${employer}</span>` : ""}
            ${location ? ` <span>• ${location}</span>` : ""}
            ${published ? ` <span>• ${published}</span>` : ""}
          </div>
  
          ${url ? `<div class="job-actions"><a href="${url}" target="_blank" rel="noopener">Öppna annons</a></div>` : ""}
        </article>
      `;
    }).join("");
  
    resultsEl.innerHTML = `<div class="cards">${cards}</div>`;
  }

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const q = document.getElementById("q").value.trim();
  const location = document.getElementById("location").value.trim();

  if (!q || !location) return;

  setLoading();

  try {
    const url = `${API_BASE}/api/search?q=${encodeURIComponent(q)}&municipality=${encodeURIComponent(location)}`;
    const res = await fetch(url);

    if (!res.ok) {
      throw new Error(`Backend svarade med status ${res.status}`);
    }

    const data = await res.json();

    const jobs = Array.isArray(data) ? data : (data.jobs || []);
    const salary = jobs.length > 0 ? { value: jobs[0].salary, source: "SCB" } : null;

    renderSalary({ q, location, salary });
    renderJobs(jobs);

  } catch (err) {
    console.error(err);
    setError("Kunde inte hämta data");
  }
});

