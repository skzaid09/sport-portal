// admin.js - Admin Panel Logic

// Load events into dropdown on page load
window.onload = function () {
  fetch('http://127.0.0.1:8000/api/events')
    .then(res => res.json())
    .then(events => {
      const eventSelect = document.getElementById('eventSelect');
      events.forEach(event => {
        const opt = document.createElement('option');
        opt.value = event._id.$oid;
        opt.textContent = event.event_name;
        eventSelect.appendChild(opt);
      });
    })
    .catch(err => console.error("Failed to load events:", err));
};

// Handle Event Form Submission
document.getElementById('eventForm').onsubmit = function (e) {
  e.preventDefault();

  const formData = {
    event_name: document.getElementById('eventName').value,
    sport_type: document.getElementById('sportType').value,
    start_date: document.getElementById('startDate').value,
    end_date: document.getElementById('endDate').value,
    max_teams: parseInt(document.getElementById('maxTeams').value),
    organizer_id: "FAC2025"
  };

  fetch('http://127.0.0.1:8000/api/create-event', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData)
  })
  .then(res => res.json())
  .then(data => {
    alert("✅ Event created successfully!");
    document.getElementById('eventForm').reset();
    // Reload dropdown
    location.reload();
  })
  .catch(err => alert("❌ Failed to create event."));
};