let repairJobs = [];

async function loadVehicles() {
    const select = document.getElementById("vehicle_id");

    select.innerHTML = "";

    try {
        const vehicles = await api.get("/vehicles");

        vehicles.forEach(vehicle => {
            const option = document.createElement("option");

            option.value = vehicle.id;
            option.textContent =
                `${vehicle.year} ${vehicle.make} ${vehicle.model}`;

            select.appendChild(option);
        });

    } catch (err) {
        console.error(err);
        showAlert("Unable to load vehicles.", "danger");
    }
}

async function loadRepairJobs() {

    const tbody = document.getElementById("repairJobTable");

    tbody.innerHTML = "";

    try {

        repairJobs = await api.get("/repair-jobs");

        repairJobs.forEach(job => {

            let aiButton = "";

            if (job.ai_diagnosis) {

                aiButton = `
                    <button
                        class="btn btn-info btn-sm"
                        onclick="viewDiagnosis('${job.id}')">
                        View AI
                    </button>
                `;

            } else {

                aiButton = `
                    <button
                        id="ai-${job.id}"
                        class="btn btn-primary btn-sm"
                        onclick="generateDiagnosis('${job.id}')">
                        Diagnose
                    </button>
                `;

            }

            tbody.innerHTML += `
                <tr>

                    <td>
                        <a
                            href="/vehicles"
                            title="${job.vehicle_id}"
                            class="text-decoration-none">
                            ${job.vehicle_id.substring(0, 8)}...
                        </a>
                    </td>

                    <td>${job.title}</td>

                    <td>${job.status}</td>

                    <td>${job.mileage}</td>

                    <td>
                        ${aiButton}
                    </td>

                    <td>
                        <button
                            class="btn btn-danger btn-sm"
                            onclick="deleteRepairJob('${job.id}')">
                            Delete
                        </button>
                    </td>

                </tr>
            `;

        });

    } catch (err) {

        console.error(err);

        showAlert("Unable to load repair jobs.", "danger");

    }

}

document
.getElementById("saveRepairJob")
.addEventListener("click", async () => {

    try {

        await api.post("/repair-jobs", {

            vehicle_id:
                document.getElementById("vehicle_id").value,

            title:
                document.getElementById("title").value,

            description:
                document.getElementById("description").value,

            mileage:
                Number(document.getElementById("mileage").value)

        });

        bootstrap.Modal
            .getInstance(
                document.getElementById("repairJobModal")
            )
            .hide();

        showAlert("Repair job created.");

        document.getElementById("title").value = "";
        document.getElementById("description").value = "";
        document.getElementById("mileage").value = "";

        loadRepairJobs();

    } catch (err) {

        console.error(err);

        showAlert(
            err.detail || "Unable to create repair job.",
            "danger"
        );

    }

});

async function generateDiagnosis(id) {

    const button = document.getElementById(`ai-${id}`);

    button.disabled = true;
    button.innerText = "Generating...";

    try {

        const result = await api.post(`/ai/diagnose/${id}`, {});

        document.getElementById("diagnosisContent").textContent =
            result.diagnosis;

        new bootstrap.Modal(
            document.getElementById("diagnosisModal")
        ).show();

        showAlert("AI diagnosis generated.");

        await loadRepairJobs();

    } catch (err) {

        console.error(err);

        showAlert(
            err.detail || "AI diagnosis failed.",
            "danger"
        );

        button.disabled = false;
        button.innerText = "Diagnose";

    }

}

function viewDiagnosis(id) {

    const job = repairJobs.find(j => j.id === id);

    if (!job)
        return;

    document.getElementById("diagnosisContent").textContent =
        job.ai_diagnosis;

    new bootstrap.Modal(
        document.getElementById("diagnosisModal")
    ).show();

}

async function deleteRepairJob(id) {

    if (!confirm("Delete repair job?"))
        return;

    try {

        await api.delete(`/repair-jobs/${id}`);

        showAlert("Repair job deleted.");

        loadRepairJobs();

    } catch (err) {

        console.error(err);

        showAlert(
            err.detail || "Unable to delete repair job.",
            "danger"
        );

    }

}

loadVehicles();
loadRepairJobs();
