const form = document.getElementById("register-form");

if (form) {

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        const full_name =
            document.getElementById("full_name").value;

        const email =
            document.getElementById("email").value;

        const password =
            document.getElementById("password").value;

        try {

            const response = await fetch(
                "/api/auth/register",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":"application/json"
                    },
                    body: JSON.stringify({
                        full_name,
                        email,
                        password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok){

                alert(data.detail);

                return;

            }

            alert("Registration successful.");

            window.location.href="/login";

        }

        catch(err){

            console.error(err);

            alert("Registration failed.");

        }

    });

}
