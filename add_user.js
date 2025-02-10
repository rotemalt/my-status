document.getElementById("userForm").addEventListener("submit", function (event) {
    event.preventDefault();

    const lastName = document.getElementById("lastName").value;
    const idNumber = document.getElementById("idNumber").value;

    // Ensure it matches FastAPI’s expected JSON keys
    const userData = {
        last_name: lastName,
        identification_number: idNumber, // Corrected key
    };

    // Corrected API endpoint
    const apiEndpoint = "https://my-status-p9ia.onrender.com/add_user"; // Change this if deployed

    fetch(apiEndpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.message) {
            document.getElementById("responseMessage").textContent = data.message;
        } else {
            document.getElementById("responseMessage").textContent = "Error adding user.";
        }
    })
    .catch((error) => {
        document.getElementById("responseMessage").textContent = "Error: " + error.message;
    });
});
