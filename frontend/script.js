const SEARCH_ENDPOINT = "/api/search/combined";

const form = document.getElementById("searchForm");
const resultsEl = document.getElementById("results");

const salaryPanel = document.getElementById("salaryPanel");
const salaryContent = document.getElementById("salaryContent");

const jobCountEl = document.getElementById("jobCount"); 

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

function renderSalary({q, location, salary}) {
    if (!salary) {
        salaryContent.innerHTML = `<p>Ingen löninfo kunde hämtas.</p>`;
        return;
    }
    const mean = salary.mean ?? null;
    const median = salary.median ?? null;
    const percentiles = salary.percentiles ?? {};
    const year = salary.year ?? "";

    const values = [
        {label: "P10", value: percentiles.p10},
        {label: "P25", value: percentiles.p25},
        {label: "Median", value: median, highlight: true},
        {label: "P75", value: percentiles.p75},
        {label: "P90", value: percentiles.p90},
    ].filter(v => typeof v.value === "number");

    const maxValue = Math.max(...values.map(v => v.value));

    const bars = values.map(v => `
    <div class="salary-bar-item">
      <div class="salary-bar-label">${v.label}</div>
      <div class="salary-bar-track">
        <div
          class="salary-bar-fill ${v.highlight ? "median" : ""}"
          style="width: ${(v.value / maxValue) * 100}%"
        ></div>
      </div>
      <div class="salary-bar-value">
        ${v.value.toLocaleString()} kr
      </div>
    </div>
  `).join("");

    salaryContent.innerHTML = `
    <p><strong>Yrkeområde:</strong> ${q}</p>
    <p><strong>Ort:</strong> ${location}</p>
    <p><strong>Snittlön:</strong> ${mean.toLocaleString()} kr / mån</p>

    <div class="salary-bar-chart">
      ${bars}
    </div>

    <p class="salary-source">Källa: SCB (${year})</p>
  `;
}


function renderJobs(jobs) {
  const query = document.getElementById("q").value.trim();
    const location = document.getElementById("location").value.trim();

    if (jobCountEl) {
        if (jobs.length > 0) {
            jobCountEl.innerText = `Hittade ${jobs.length} lediga tjänster för "${query}" i ${location}`;
        } else {
            jobCountEl.innerText = "";
        }
    }
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
        const salary = salaryJob?.salary ?? null;

        renderSalary({q, location, salary});
        renderJobs(jobs);

    } catch (err) {
        console.error(err);
        setError("Kunde inte hämta data");
    }
});

