const form = document.getElementById("searchForm");
const resultsDiv = document.getElementById("results");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const q = document.getElementById("query").value;
    const municipality = document.getElementById("municipality").value;
    const year = document.getElementById("year").value;

    resultsDiv.innerHTML = "Laddar...";

    const response = await fetch(
        `http://127.0.0.1:8000/search/combined?q=${q}&municipality=${municipality}&year=${year}`
    );

    const data = await response.json();

    resultsDiv.innerHTML = "";

    data.forEach(job => {
        const div = document.createElement("div");
        div.className = "job";

        div.innerHTML = `
            <h3>${job.title}</h3>
            <p><strong>Företag:</strong> ${job.employer}</p>
            <p><strong>Plats:</strong> ${job.location}</p>
            <p><strong>Arbetstid:</strong> ${job.workload}</p>
            <p><strong>Lön:</strong> ${job.salary ? job.salary + " kr" : "Ej tillgänglig"}</p>
            <a href="${job.url}" target="_blank">Visa annons</a>
        `;

        resultsDiv.appendChild(div);
    });
});