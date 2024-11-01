document.getElementById('sendButton').addEventListener('click', function() {
    const sensorValue = document.getElementById('sensorValueInput').value;

    fetch('/sensor-data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ sensor_value: sensorValue }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('greeting').innerText = `Sensor Value Sent: ${data.sensor_value}`;
        } else {
            document.getElementById('greeting').innerText = `Error: ${data.error}`;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('greeting').innerText = 'Error sending data.';
    });
});
