const inputUsernameDiv = document.getElementsByClassName("input-username")[0];

let inputField = document.createElement("input");
inputField.setAttribute("type", "text");
inputField.setAttribute("placeholder", "Enter username");

// Create confirm button
let confirmButton = document.createElement("button");
confirmButton.textContent = "Confirm";

// Append input and button to the div
inputUsernameDiv.appendChild(inputField);
inputUsernameDiv.appendChild(confirmButton);

confirmButton.addEventListener("click", function() {
    // Get the value of the input
    const username = inputField.value;

    // Call GitHub API to add user to team
    const accessToken = "ghp_ipeseit"; // Replace with your GitHub personal access token
    const orgName = "IPESE"; // Replace with your organization name
    const teamId = "college-students"; // Replace with the ID of the team you want to add the user to

    fetch(`https://api.github.com/orgs/${orgName}/teams/${teamId}/memberships/${username}`, {
        method: "PUT",
        headers: {
            "Authorization": `token ${accessToken}`,
            "Accept": "application/vnd.github.v3+json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to add user to team.");
        }
        console.log("User added to team successfully.");
    })
    .catch(error => {
        console.error(error.message);
    });
});