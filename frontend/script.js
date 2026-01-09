function showHome() {
    showSection("home");
}

function showJobs() {
    showSection("jobs");
}

function showSalary() {
    showSection("salary");
}

function showSection(id) {
    document.querySelectorAll("main section").forEach(section => {
        section.hidden = true;
    });

    document.getElementById(id).hidden = false;
}
