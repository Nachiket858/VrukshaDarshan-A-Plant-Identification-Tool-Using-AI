document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();  

    const formData = new FormData(this);  

    // Display the uploaded image
    const fileInput = this.querySelector('input[type="file"]');
    const uploadedImage = document.getElementById('uploaded-image');
    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        uploadedImage.src = e.target.result;  
        uploadedImage.style.display = 'block';  
    }

    reader.readAsDataURL(file);  

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = '';  

        if (data.error) {
            resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
        } else {
            // Display the results
            resultDiv.innerHTML = `
                <p class="success">Common Name: ${data.common_name}</p>
                <p class="success">Scientific Name: ${data.scientific_name}</p>
                <p class="success">Probability: ${data.probability}</p>
            `;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = `<p class="error">An error occurred while processing the request.</p>`;
    });
});
