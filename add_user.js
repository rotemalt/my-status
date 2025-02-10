document.getElementById("userForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const lastName = document.getElementById("lastName").value;
    const idNumber = document.getElementById("idNumber").value;

    // API endpoint to add user
    const apiEndpoint = "https://rotemalt.github.io/my-status-site/website/";

    fetch(apiEndpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            last_name: lastName,
            id_number: idNumber,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                document.getElementById("responseMessage").textContent = "User added successfully!";
            } else {
                document.getElementById("responseMessage").textContent = "Error adding user.";
            }
        })
        .catch((error) => {
            document.getElementById("responseMessage").textContent = "Error: " + error.message;
        });
});
