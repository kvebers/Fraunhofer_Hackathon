document
  .getElementById("prognosisForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way
    const month = document.getElementById("monthSelect").value;
    const day = document.getElementById("daySelect").value;
    const hour = document.getElementById("hourSelect").value;

    // Create the query string parameters for month and day
    const queryParams = `?month=${month}&day=${day}&${hour}`;

    // Fetch the prognosis from the server
    fetch(`/prognosis${queryParams}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json(); // Parse JSON response
      })
      .then((data) => {
        // Handle the response data
        document.getElementById("responseText").innerText =
          data.mitte + data.ost + data.theresian; // Display the message from the JSON response
      })
      .catch((error) => {
        console.error("There was a problem with the fetch operation:", error);
        document.getElementById("responseText").innerText =
          "Error fetching data. Please try again.";
      });
  });
