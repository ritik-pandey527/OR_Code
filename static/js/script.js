function greet() {
    const name = document.getElementById('nameInput').value;
    fetch(`/greet?name=${name}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('greetMessage').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function sendSensorData() {
    // Replace with actual sensor value if needed
    const sensorValue = Math.floor(Math.random() * 1024); // Simulated sensor value

    fetch('/sensor-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ sensor_value: sensorValue })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('sensorResponse').innerText = `Sensor value sent: ${data.sensor_value}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
