// Fetch available vehicles and display them on the vehicles page
function fetchVehicles() {
  fetch("/api/vehicles")
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById("vehicles-container");
      container.innerHTML = "";
      data.forEach(vehicle => {
        const vehicleDiv = document.createElement("div");
        vehicleDiv.className = "vehicle-card";
        vehicleDiv.innerHTML = `
          <img src="${vehicle.photo_url}" alt="${vehicle.brand} ${vehicle.model}" class="vehicle-photo"/>
          <h3>${vehicle.brand} ${vehicle.model}</h3>
          <p>Price per day: $${vehicle.price_per_day}</p>
          <button onclick="bookVehicle(${vehicle.id})">Book Now</button>
        `;
        container.appendChild(vehicleDiv);
      });
    })
    .catch(error => console.error("Error fetching vehicles:", error));
}

// Redirect to booking page with vehicle_id parameter
function bookVehicle(vehicleId) {
  window.location.href = "/booking?vehicle_id=" + vehicleId;
}

// Handle Registration Form Submission
if (document.getElementById("registration-form")) {
  document.getElementById("registration-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const name = document.getElementById("reg_name").value;
    const email = document.getElementById("reg_email").value;
    const phone = document.getElementById("reg_phone").value;
    const password = document.getElementById("reg_password").value;
    const regData = { name, email, phone, password };

    fetch("/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(regData)
    })
      .then(response => response.json())
      .then(data => {
        const regResultDiv = document.getElementById("reg-result");
        if (data.error) {
          regResultDiv.textContent = "Error: " + data.error;
        } else {
          regResultDiv.textContent = data.message;
        }
      })
      .catch(error => console.error("Error during registration:", error));
  });
}

// Handle Login Form Submission
if (document.getElementById("login-form")) {
  document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const email = document.getElementById("login_email").value;
    const password = document.getElementById("login_password").value;
    const loginData = { email, password };

    fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(loginData)
    })
      .then(response => response.json())
      .then(data => {
        const loginResultDiv = document.getElementById("login-result");
        if (data.error) {
          loginResultDiv.textContent = "Error: " + data.error;
        } else {
          loginResultDiv.textContent = data.message;
          // Redirect to home after login
          window.location.href = "/";
        }
      })
      .catch(error => console.error("Error during login:", error));
  });
}

// Handle Booking Form Submission
if (document.getElementById("booking-form")) {
  document.getElementById("booking-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const vehicle_id = document.getElementById("vehicle_id").value;
    const rent_date = document.getElementById("rent_date").value;
    const return_date = document.getElementById("return_date").value;
    const bookingData = { vehicle_id, rent_date, return_date };

    fetch("/api/bookings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(bookingData)
    })
      .then(response => response.json())
      .then(data => {
        const resultDiv = document.getElementById("booking-result");
        if (data.error) {
          resultDiv.textContent = "Error: " + data.error;
        } else {
          resultDiv.textContent = "Booking successful! Total Price: $" + data.total_price;
        }
      })
      .catch(error => console.error("Error creating booking:", error));
  });
}

// Fetch and display logged-in user's bookings
function fetchMyBookings() {
  fetch("/api/mybookings")
    .then(response => response.json())
    .then(data => {
      const bookingsList = document.getElementById("bookings-list");
      bookingsList.innerHTML = "";
      if (data.error) {
        bookingsList.innerHTML = `<li>Error: ${data.error}</li>`;
      } else if (data.length === 0) {
        bookingsList.innerHTML = `<li>No bookings found.</li>`;
      } else {
        data.forEach(booking => {
          const li = document.createElement("li");
          li.textContent = `Booking ID: ${booking.booking_id} | Vehicle: ${booking.brand} ${booking.model} | Rent: ${booking.rent_date} | Return: ${booking.return_date} | Price: $${booking.total_price} | Status: ${booking.status}`;
          bookingsList.appendChild(li);
        });
      }
    })
    .catch(error => console.error("Error fetching bookings:", error));
}
