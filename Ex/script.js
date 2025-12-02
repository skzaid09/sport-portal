// script.js - QR Login & Navigation

function startCamera() {
  const video = document.getElementById('video');
  const result = document.getElementById('result');
  video.style.display = 'block';

  navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(stream => {
      video.srcObject = stream;
      video.play();
      scan();
    })
    .catch(err => {
      result.textContent = "Error accessing camera: " + err.message;
    });

  function scan() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    requestAnimationFrame(function process() {
      if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const code = jsQR(imageData.data, imageData.width, imageData.height);

        if (code) {
          result.textContent = "Scanned: " + code.data;
          simulateLogin(code.data);
        } else {
          requestAnimationFrame(process);
        }
      }
    });
  }
}

// script.js - Updated: Send QR to Backend
function simulateLogin(qrCode) {
  fetch('http://127.0.0.1:8000/api/verify-qr', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ qr_code: qrCode })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Invalid QR Code");
    }
    return response.json();
  })
  .then(data => {
    document.getElementById('result').textContent = `Welcome, ${data.name}!`;
    
    // Save user info
    localStorage.setItem("user", JSON.stringify(data));
    
    // Redirect to dashboard
    setTimeout(() => {
      window.location.href = "dashboard.html";
    }, 1000);
  })
  .catch(err => {
    document.getElementById('result').textContent = "❌ " + err.message;
    setTimeout(() => {
      location.reload();
    }, 2000);
  });
}