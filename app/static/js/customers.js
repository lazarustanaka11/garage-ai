async function loadCustomers() {

    const tbody = document.getElementById("customerTable");

    tbody.innerHTML = "";

    try {

        const customers = await api.get("/customers");

        customers.forEach(customer => {

            tbody.innerHTML += `

<tr>

<td>${customer.name}</td>

<td>${customer.email}</td>

<td>${customer.phone}</td>

<td>

<button
class="btn btn-danger btn-sm"
onclick="deleteCustomer('${customer.id}')">

Delete

</button>

</td>

</tr>

`;

        });

    } catch (err) {

        console.error(err);

        showAlert("Unable to load customers.", "danger");

    }

}


document
.getElementById("saveCustomer")
.addEventListener("click", async () => {

    try {

        await api.post("/customers", {

            name: document.getElementById("name").value,

            email: document.getElementById("email").value,

            phone: document.getElementById("phone").value,

        });
        showAlert("Customer created successfully!");

        bootstrap.Modal
            .getInstance(
                document.getElementById("customerModal")
            )
            .hide();

        loadCustomers();

    } catch (err) {

        showAlert(err.detail, "danger");

    }

});


async function deleteCustomer(id) {

    if (!confirm("Delete customer?")) {

        return;

    }

    await api.delete(`/customers/${id}`);
    showAlert("Customer deleted.");

    loadCustomers();

}


loadCustomers();
