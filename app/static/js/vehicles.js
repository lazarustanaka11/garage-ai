async function loadCustomers() {
    const select = document.getElementById("customer_id");

    select.innerHTML = "";

    try {
        const customers = await api.get("/customers");

        customers.forEach(customer => {
            const option = document.createElement("option");

            option.value = customer.id;
            option.textContent = customer.name;

            select.appendChild(option);
        });

    } catch (err) {
        console.error(err);
        showAlert("Unable to load customers.", "danger");
    }
}

async function loadVehicles() {
    const tbody = document.getElementById("vehicleTable");

    tbody.innerHTML = "";

    try {
        const vehicles = await api.get("/vehicles");

        vehicles.forEach(vehicle => {
            tbody.innerHTML += `
                <tr>
                    <td>${vehicle.make}</td>
                    <td>${vehicle.model}</td>
                    <td>${vehicle.year}</td>
                    <td>${vehicle.license_plate}</td>
                    <td>
                        <button
                            class="btn btn-danger btn-sm"
                            onclick="deleteVehicle('${vehicle.id}')">
                            Delete
                        </button>
                    </td>
                </tr>
            `;
        });

    } catch (err) {
        console.error(err);
        showAlert("Unable to load vehicles.", "danger");
    }
}

document
    .getElementById("saveVehicle")
    .addEventListener("click", async () => {
        try {
            await api.post("/vehicles", {
                customer_id: document.getElementById("customer_id").value,
                make: document.getElementById("make").value,
                model: document.getElementById("model").value,
                year: Number(document.getElementById("year").value),
                vin: document.getElementById("vin").value,
                license_plate: document.getElementById("license_plate").value,
                mileage: Number(document.getElementById("mileage").value),
                color: document.getElementById("color").value
            });

            bootstrap.Modal
                .getInstance(document.getElementById("vehicleModal"))
                .hide();

            showAlert("Vehicle created successfully!");

            document.getElementById("make").value = "";
            document.getElementById("model").value = "";
            document.getElementById("year").value = "";
            document.getElementById("vin").value = "";
            document.getElementById("license_plate").value = "";
            document.getElementById("mileage").value = "";
            document.getElementById("color").value = "";

            await loadVehicles();

        } catch (err) {
            console.error(err);
            showAlert(err.detail || "Unable to create vehicle.", "danger");
        }
    });

async function deleteVehicle(id) {
    if (!confirm("Delete vehicle?")) {
        return;
    }

    try {
        await api.delete(`/vehicles/${id}`);

        showAlert("Vehicle deleted.");

        await loadVehicles();

    } catch (err) {
        console.error(err);
        showAlert(err.detail || "Unable to delete vehicle.", "danger");
    }
}

loadCustomers();
loadVehicles();
