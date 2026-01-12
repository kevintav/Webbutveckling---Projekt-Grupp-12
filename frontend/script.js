
const SEARCH_ENDPOINT = "/api/search/combined";

const form = document.getElementById("searchForm");
const resultsEl = document.getElementById("results");

const salaryPanel = document.getElementById("salaryPanel");
const salaryContent = document.getElementById("salaryContent");

function setLoading() {
  resultsEl.innerHTML = `
    <div class="status-msg loading">
      <div class="spinner"></div>
      <p>Hämtar platsannonser…</p>
    </div>
  `;

  salaryPanel.classList.remove("hidden");
  salaryContent.innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <p>Hämtar lönestatistik…</p>
    </div>
  `;
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
      <p><strong>Snittlön för Yrke-område:</strong> ${belopp} kr</p>
    `;
  }

  function renderJobs(jobs) {
  if (!jobs.length) {
    resultsEl.innerHTML =
      `<div class="status-msg"><p>Inga platsannonser hittades.</p></div>`;
    return;
  }

  const cards = jobs.map(job => `
    <article class="job-card">
      <div class="job-title">${job.title ?? "Okänd titel"}</div>
      <div class="job-meta">
        ${job.employer ? `<span class="badge">${job.employer}</span>` : ""}
        ${job.location ? `<span>• ${job.location}</span>` : ""}
      </div>
      ${job.url ? `
        <div class="job-actions">
          <a href="${job.url}" target="_blank" rel="noopener">Öppna annons</a>
        </div>` : ""}
    </article>
  `).join("");

  resultsEl.innerHTML = `<div class="cards">${cards}</div>`;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const q = document.getElementById("q").value.trim();
  const location = document.getElementById("location").value.trim();

  if (!q || !location) return;

  setLoading();

  try {
    const url = `${SEARCH_ENDPOINT}?q=${encodeURIComponent(q)}&region=${encodeURIComponent(location)}`;
    const res = await fetch(url);

    if (!res.ok) {
      throw new Error(`Backend svarade med status ${res.status}`);
    }

    const data = await res.json();

    const jobs = Array.isArray(data) ? data : (data.jobs || []);
    const salaryJob = jobs.find(job => job.salary != null);

    const salary = salaryJob
      ? { value: salaryJob.salary, source: "SCB" }
      : null;

    renderSalary({ q, location, salary });
    renderJobs(jobs);

  } catch (err) {
    console.error(err);
    setError("Kunde inte hämta data");
  }
});

