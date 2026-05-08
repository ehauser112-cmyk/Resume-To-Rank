const state = {
    files: [],
    ranked: [],
};

const elements = {
    fileInput: document.querySelector("#resumeFiles"),
    dropzone: document.querySelector("#dropzone"),
    fileList: document.querySelector("#fileList"),
    uploadButton: document.querySelector("#uploadButton"),
    parseButton: document.querySelector("#parseButton"),
    rankButton: document.querySelector("#rankButton"),
    sortScoreButton: document.querySelector("#sortScoreButton"),
    sortNameButton: document.querySelector("#sortNameButton"),
    clearRankingsButton: document.querySelector("#clearRankingsButton"),
    exportButton: document.querySelector("#exportButton"),
    addSkillButton: document.querySelector("#addSkillButton"),
    clearSelectionButton: document.querySelector("#clearSelectionButton"),
    criteriaGrid: document.querySelector("#criteriaGrid"),
    customCriteria: document.querySelector("#customCriteria"),
    resultsBody: document.querySelector("#resultsBody"),
    resultsSummary: document.querySelector("#resultsSummary"),
    messageLog: document.querySelector("#messageLog"),
    statusPill: document.querySelector("#statusPill"),
};

function setStatus(message, type = "ok") {
    elements.statusPill.textContent = message;
    elements.statusPill.classList.toggle("error", type === "error");
}

function log(message, type = "ok") {
    elements.messageLog.textContent = message;
    setStatus(type === "error" ? "Needs attention" : "Ready", type);
}

function setBusy(isBusy) {
    [
        elements.uploadButton,
        elements.parseButton,
        elements.rankButton,
        elements.sortScoreButton,
        elements.sortNameButton,
        elements.clearRankingsButton,
        elements.exportButton,
    ].forEach((button) => {
        button.disabled = isBusy;
    });
    if (isBusy) {
        setStatus("Working");
    }
}

function updateFileList() {
    if (!state.files.length) {
        elements.fileList.textContent = "No files selected";
        return;
    }

    elements.fileList.textContent = state.files.map((file) => file.name).join(", ");
}

function setFiles(fileList) {
    state.files = Array.from(fileList);
    elements.fileInput.value = "";
    updateFileList();
}

async function requestJson(url, options = {}) {
    const response = await fetch(url, options);
    const payload = await response.json();

    if (!response.ok || payload.error) {
        throw new Error(payload.error || `Request failed with status ${response.status}`);
    }

    return payload;
}

function selectedCriteria() {
    return Array.from(elements.criteriaGrid.querySelectorAll("input:checked")).map((input) => input.value);
}

function normalizedSkill(value) {
    return value.trim().replace(/\s+/g, " ");
}

function skillExists(skill) {
    return Array.from(elements.criteriaGrid.querySelectorAll("input")).some((input) => input.value.toLowerCase() === skill.toLowerCase());
}

function addSkill() {
    const skill = normalizedSkill(elements.customCriteria.value);

    if (!skill) {
        log("Enter a skill before adding it.", "error");
        return;
    }

    if (skillExists(skill)) {
        const existing = Array.from(elements.criteriaGrid.querySelectorAll("input")).find((input) => input.value.toLowerCase() === skill.toLowerCase());
        existing.checked = true;
        elements.customCriteria.value = "";
        log(`${skill} is already in the list and is now selected.`);
        return;
    }

    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = skill.toLowerCase();
    checkbox.checked = true;
    label.append(checkbox, ` ${skill}`);
    elements.criteriaGrid.append(label);
    elements.customCriteria.value = "";
    log(`Added ${skill} to the skill list.`);
}

function renderRanked(ranked) {
    state.ranked = ranked;

    if (!ranked.length) {
        elements.resultsSummary.textContent = "No candidates ranked yet.";
        elements.resultsBody.innerHTML = '<tr><td colspan="4" class="empty-state">Upload, parse, and rank resumes to see candidates here.</td></tr>';
        return;
    }

    elements.resultsSummary.textContent = `${ranked.length} candidate${ranked.length === 1 ? "" : "s"} ranked.`;
    elements.resultsBody.innerHTML = ranked
        .map((candidate, index) => {
            const matches = candidate.matches && candidate.matches.length
                ? candidate.matches.map((match) => `<span class="match">${escapeHtml(match)}</span>`).join("")
                : '<span class="match">No selected match</span>';

            return `
                <tr>
                    <td>${index + 1}</td>
                    <td>${escapeHtml(candidate.filename)}</td>
                    <td><span class="score">${candidate.score}</span></td>
                    <td><div class="matches">${matches}</div></td>
                </tr>
            `;
        })
        .join("");
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

async function uploadFiles() {
    if (!state.files.length) {
        log("Choose at least one resume before uploading.", "error");
        return;
    }

    const formData = new FormData();
    state.files.forEach((file) => formData.append("files", file));

    setBusy(true);
    try {
        const result = await requestJson("/upload", {
            method: "POST",
            body: formData,
        });
        log(`Uploaded ${result.uploaded.length} file${result.uploaded.length === 1 ? "" : "s"}. Rejected: ${result.rejected.length}.`);
    } catch (error) {
        log(error.message, "error");
    } finally {
        setBusy(false);
    }
}

async function parseResumes() {
    setBusy(true);
    try {
        const result = await requestJson("/parse", { method: "POST" });
        log(`Parsed ${result.count} resume${result.count === 1 ? "" : "s"}.`);
    } catch (error) {
        log(error.message, "error");
    } finally {
        setBusy(false);
    }
}

async function rankResumes() {
    const criteria = selectedCriteria();
    if (!criteria.length) {
        log("Select or enter at least one ranking criterion.", "error");
        return;
    }

    setBusy(true);
    try {
        const result = await requestJson("/rank", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ criteria }),
        });
        renderRanked(result.ranked);
        log(`Generated ranking with ${result.criteria.length} ${result.criteria.length === 1 ? "criterion" : "criteria"}.`);
    } catch (error) {
        log(error.message, "error");
    } finally {
        setBusy(false);
    }
}

async function sortRanked(key) {
    setBusy(true);
    try {
        const result = await requestJson("/sort", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ key }),
        });
        renderRanked(result.ranked);
        log(`Sorted candidates by ${result.sort_key}.`);
    } catch (error) {
        log(error.message, "error");
    } finally {
        setBusy(false);
    }
}

async function exportCsv() {
    setBusy(true);
    try {
        const result = await requestJson("/export", { method: "POST" });
        log(`Exported ${result.count} ranked candidate${result.count === 1 ? "" : "s"} to ${result.exported}.`);
    } catch (error) {
        log(error.message, "error");
    } finally {
        setBusy(false);
    }
}

async function clearRankings() {
    setBusy(true);
    try {
        const result = await requestJson("/rank/clear", { method: "POST" });
        renderRanked(result.ranked);
        log("Ranking data cleared.");
    } catch (error) {
        log(error.message, "error");
    } finally {
        setBusy(false);
    }
}

elements.fileInput.addEventListener("change", (event) => setFiles(event.target.files));

["dragenter", "dragover"].forEach((eventName) => {
    elements.dropzone.addEventListener(eventName, (event) => {
        event.preventDefault();
        elements.dropzone.classList.add("is-dragging");
    });
});

["dragleave", "drop"].forEach((eventName) => {
    elements.dropzone.addEventListener(eventName, (event) => {
        event.preventDefault();
        elements.dropzone.classList.remove("is-dragging");
    });
});

elements.dropzone.addEventListener("drop", (event) => {
    setFiles(event.dataTransfer.files);
});

elements.clearSelectionButton.addEventListener("click", () => {
    state.files = [];
    updateFileList();
    log("File selection cleared.");
});

elements.uploadButton.addEventListener("click", uploadFiles);
elements.parseButton.addEventListener("click", parseResumes);
elements.rankButton.addEventListener("click", rankResumes);
elements.sortScoreButton.addEventListener("click", () => sortRanked("score"));
elements.sortNameButton.addEventListener("click", () => sortRanked("filename"));
elements.clearRankingsButton.addEventListener("click", clearRankings);
elements.exportButton.addEventListener("click", exportCsv);
elements.addSkillButton.addEventListener("click", addSkill);
elements.customCriteria.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        event.preventDefault();
        addSkill();
    }
});

updateFileList();
