document.getElementById('prognosisForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent the form from submitting the traditional way

    // Get the value of the date input
    const dateInput = document.getElementById('dateInput').value;

    // Split the date value into year, month, and day
    const date = new Date(dateInput);
    const month = date.getMonth() + 1; // Months are 0-indexed, so add 1
    const day = date.getDate();

    // Create the query string parameters for month and day
    const queryParams = `?month=${month}&day=${day}`;

    // Fetch the prognosis from the server
    fetch(`/prognosis${queryParams}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // Parse JSON response
    })
    .then(data => {
        // Handle the response data
        document.getElementById('responseText').innerText = data.message;  // Display the message from the JSON response
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        document.getElementById('responseText').innerText = 'Error fetching data. Please try again.';
    });
});
