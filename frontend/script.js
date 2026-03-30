const SEARCH_ENDPOINT = "/api/search/combined";

const form = document.getElementById("searchForm");
const resultsEl = document.getElementById("results");

const salaryPanel = document.getElementById("salaryPanel");
const salaryContent = document.getElementById("salaryContent");

const jobCountEl = document.getElementById("jobCount"); 

const clearBtn = document.getElementById("clearBtn");

const STORAGE_KEY = "lastSearch";


const THEME_KEY = "theme";
const themeToggle = document.getElementById("themeToggle");










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

const sortSelect = document.getElementById("sortSelect");
const employmentFilter = document.getElementById("employmentFilter");
const minSalaryInput = document.getElementById("minSalary");

function applyFiltersAndSort(jobs) {
  let filtered = [...jobs];

  const empType = employmentFilter.value;

  if (empType) {
    filtered = filtered.filter(job => {
      const scope = job.scope_of_work;

      if (!scope) return empType === "Variable";

      const min = scope.min ?? 0;
      const max = scope.max ?? 0;

      if (min === 100 && max === 100) {
        return empType === "Full-time";
      }

      if (max < 100) {
        return empType === "Part-time";
      }

      if (min < 100 && max === 100) {
        return empType === "Part-time";
      }

      return empType === "Variable";

});
  }

  const minSalary = parseInt(minSalaryInput.value);
  if (!isNaN(minSalary)) {
    filtered = filtered.filter(job => job.salary?.median >= minSalary);
  }

  const sortKey = sortSelect.value;
  if (sortKey) {
    filtered.sort((a, b) => {
      if (sortKey === "salary") {
        return (b.salary?.median || 0) - (a.salary?.median || 0);
      }
      return (a[sortKey] || "").localeCompare(b[sortKey] || "");
    });
  }

  return filtered;
}

sortSelect.addEventListener("change", () => {
  const lastJobs = JSON.parse(localStorage.getItem("lastResults") || "[]");
  renderJobs(applyFiltersAndSort(lastJobs));
});

employmentFilter.addEventListener("change", () => {
  const lastJobs = JSON.parse(localStorage.getItem("lastResults") || "[]");
  renderJobs(applyFiltersAndSort(lastJobs));
});

minSalaryInput.addEventListener("input", () => {
  const lastJobs = JSON.parse(localStorage.getItem("lastResults") || "[]");
  renderJobs(applyFiltersAndSort(lastJobs));
});

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

    <div class="job-actions">
      ${job.url ? `<a href="${job.url}" target="_blank">Öppna annons</a>` : ""}
    <button class="fav-btn ${isFavorite(job) ? "active" : ""}" onclick="toggleFavoriteFromUrl('${job.url}')">${isFavorite(job) ? "❤️" : "🤍"} </button>    
    </div>
  </article>
`).join("");

    resultsEl.innerHTML = `<div class="cards">${cards}</div>`;
}

const FAVORITES_KEY = "favoritesContainer";

function getFavorites() {
    return JSON.parse(localStorage.getItem(FAVORITES_KEY)) || [];
}

function saveFavorites(favs) {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favs));
}

function toggleFavorite(job) {
    let favs = getFavorites();

    const exists = favs.find(f => f.url === job.url);

    if (exists) {
        favs = favs.filter(f => f.url !== job.url);
    } else {
        favs.push(job);
    }

    saveFavorites(favs);

    renderFavorites();

    const lastJobs = JSON.parse(localStorage.getItem("lastResults") || "[]");
    renderJobs(lastJobs);
}

const toggleBtn = document.getElementById("toggleFavoritesBtn");
const favContainer = document.getElementById("favoritesContainer");

toggleBtn.addEventListener("click", () => {
    favContainer.classList.toggle("hidden");
    toggleBtn.textContent = favContainer.classList.contains("hidden") ? "Visa favoriter" : "Dölj favoriter";
});


function renderFavorites() {
    const favs = getFavorites();
    const container = document.getElementById("favoritesContainer");

    if (!favs.length) {
        container.innerHTML = "<p>Inga favoriter ännu.</p>";
        return;
    }

      const cards = favs.map(job => `
          <article class="job-card">
              <div class="job-title">${job.title ?? "Okänd titel"}</div>

              <div class="job-meta">
                  ${job.employer ? `<span class="badge">${job.employer}</span>` : ""}
                  ${job.location ? `<span>• ${job.location}</span>` : ""}
              </div>

              <div class="job-actions">
                  ${job.url ? `<a href="${job.url}" target="_blank">Öppna annons</a>` : ""}
                  <button onclick='toggleFavoriteFromUrl("${job.url}")'>❌ Ta bort </button>
              </div>
          </article>
      `).join("");

    container.innerHTML = cards;
}

function isFavorite(job) {
    const favs = getFavorites();
    return favs.some(f => f.url === job.url);
}


function toggleFavoriteFromUrl(url) {
    const lastJobs = JSON.parse(localStorage.getItem("lastResults") || "[]");
    const job = lastJobs.find(j => j.url === url);

    if (job) {
        toggleFavorite(job);
    }
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const q = document.getElementById("q").value.trim();
    const location = document.getElementById("location").value.trim();

    if (!q || !location) return;

    localStorage.setItem(STORAGE_KEY, JSON.stringify({ q, location }));

    setLoading();

    try {
        const url = `${SEARCH_ENDPOINT}?q=${encodeURIComponent(q)}&region=${encodeURIComponent(location)}`;
        const res = await fetch(url);

        if (!res.ok) {
            throw new Error(`Backend svarade med status ${res.status}`);
        }

        const data = await res.json();

        const jobs = Array.isArray(data) ? data : (data.jobs || []);
        localStorage.setItem("lastResults", JSON.stringify(jobs));
        const salaryJob = jobs.find(job => job.salary != null);
        const salary = salaryJob?.salary ?? null;

        renderSalary({q, location, salary});
        const lastJobs = JSON.parse(localStorage.getItem("lastResults") || "[]");
        const filteredJobs = applyFiltersAndSort(lastJobs);
        renderJobs(filteredJobs);

        const updatedEl = document.getElementById("lastUpdated");
  if (updatedEl) {
    updatedEl.textContent =
      "Senast uppdaterad: " + new Date().toLocaleString("sv-SE");
    updatedEl.classList.remove("hidden");
  }
    } catch (err) {
        console.error(err);
        setError("Kunde inte hämta data");
    }
});

clearBtn.addEventListener("click", () => {
    localStorage.removeItem(STORAGE_KEY);
    document.getElementById("q").value = "";
  document.getElementById("location").value = "";

  resultsEl.innerHTML = `
      <div class="status-msg">
        <p>Skriv in ett yrke och en ort i sökfälten ovan</p>
      </div>
  `;

  if (typeof jobCountEl !== 'undefined' && jobCountEl) {
      jobCountEl.innerText = "";
  }
  salaryPanel.classList.add("hidden");
});

function openJob(url) {
    if (!url) return;
    window.open(url, "_blank", "noopener");
}





window.addEventListener("load", () => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return;

    try {
        const { q, location } = JSON.parse(saved);

        document.getElementById("q").value = q;
        document.getElementById("location").value = location;

        // Kör sökningen automatiskt
        form.dispatchEvent(new Event("submit"));
    } catch (e) {
        console.error("Kunde inte läsa sparad sökning");
    }
});


// Load saved theme
window.addEventListener("load", () => {
    const savedTheme = localStorage.getItem(THEME_KEY);

    if (savedTheme === "dark") {
        document.body.classList.add("dark");
        themeToggle.textContent = "☀️";
    }
});


themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");

    const isDark = document.body.classList.contains("dark");

    if (isDark) {
        localStorage.setItem(THEME_KEY, "dark");
        themeToggle.textContent = "☀️";
    } else {
        localStorage.setItem(THEME_KEY, "light");
        themeToggle.textContent = "🌙";
    }
});

window.addEventListener("load", () => {
    renderFavorites();
});


