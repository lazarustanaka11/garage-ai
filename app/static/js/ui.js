function showAlert(message, type = "success") {

    const container = document.getElementById("alert-container");

    container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show">

            ${message}

            <button
                type="button"
                class="btn-close"
                data-bs-dismiss="alert">
            </button>

        </div>
    `;

    setTimeout(() => {

        container.innerHTML = "";

    }, 4000);

}
