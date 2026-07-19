const form = document.getElementById("login-form");

if (form) {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const username =
            document.getElementById("username").value;

        const password =
            document.getElementById("password").value;

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/api/auth/login",
                {
                    method: "POST",
                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded",
                    },
                    body: new URLSearchParams({
                        username,
                        password,
                    }),
                }
            );

            const data = await response.json();

            if (!response.ok) {
                alert(data.detail);
                return;
            }

            setToken(data.access_token);

            window.location.href = "/";

        } catch (err) {
            console.error(err);

            alert("Login failed.");
        }
    });
}
