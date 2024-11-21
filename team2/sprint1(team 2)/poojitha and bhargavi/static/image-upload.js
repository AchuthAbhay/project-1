document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent form from submitting normally

    const fileInput = document.getElementById('image-file');
    const file = fileInput.files[0];

    if (!file) {
        document.getElementById('upload-result').innerHTML = `<p>Please select a file to upload.</p>`;
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    // Using httpbin for demonstration, replace this with your actual image upload endpoint
    fetch('https://httpbin.org/post', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.files && data.files.image) {
            // Displaying the uploaded image as a preview
            document.getElementById('upload-result').innerHTML = `
                <p>Image uploaded successfully!</p>
                <img src="${data.files.image}" alt="Uploaded Image" class="uploaded-image">
            `;
        } else {
            document.getElementById('upload-result').innerHTML = `<p>Upload failed. Try again.</p>`;
        }
    })
    .catch(error => {
        console.error('Error uploading image:', error);
        document.getElementById('upload-result').innerHTML = `<p>Upload failed. Please try again later.</p>`;
    });
});
