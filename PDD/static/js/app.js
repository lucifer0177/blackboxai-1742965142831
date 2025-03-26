// Global variables
let isUploading = false;

// Image upload handling
function handleImageUpload() {
    const fileInput = document.getElementById('file');
    const dropZone = document.getElementById('dropZone');
    const imagePreview = document.getElementById('imagePreview');
    const preview = document.getElementById('preview');
    const uploadPrompt = document.getElementById('uploadPrompt');
    const uploadForm = document.getElementById('uploadForm');
    const errorDiv = document.getElementById('uploadError');
    const errorMessage = document.getElementById('errorMessage');
    const fileInfo = document.getElementById('fileInfo');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const uploadSpinner = document.getElementById('uploadSpinner');

    if (!fileInput || !dropZone) return;

    // Drag and drop handling
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('dragover');
    }

    function unhighlight() {
        dropZone.classList.remove('dragover');
    }

    // Handle dropped files
    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    }

    // Handle file selection
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            const maxSize = 16 * 1024 * 1024; // 16MB
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png'];

            // Reset error state
            errorDiv.classList.add('d-none');
            analyzeBtn.disabled = true;

            // Validate file type
            if (!allowedTypes.includes(file.type)) {
                errorDiv.classList.remove('d-none');
                errorMessage.textContent = 'Please upload a valid image file (JPG, JPEG, or PNG).';
                return;
            }

            // Validate file size
            if (file.size > maxSize) {
                errorDiv.classList.remove('d-none');
                errorMessage.textContent = 'File size exceeds 16MB limit.';
                return;
            }

            // Show preview
            const reader = new FileReader();
            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                preview.classList.remove('d-none');
                uploadPrompt.classList.add('d-none');
                
                // Show file info
                const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
                fileInfo.textContent = `${file.name} (${sizeMB} MB)`;
                
                // Enable analyze button
                analyzeBtn.disabled = false;
            }
            reader.readAsDataURL(file);
        }
    }

    // Form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            if (isUploading) return;
            
            // Show loading state
            isUploading = true;
            uploadSpinner.classList.remove('d-none');
            analyzeBtn.disabled = true;
            errorDiv.classList.add('d-none');

            // Create FormData
            const formData = new FormData();
            const fileInput = document.getElementById('file');
            if (fileInput.files.length > 0) {
                formData.append('file', fileInput.files[0]);
            } else {
                errorDiv.classList.remove('d-none');
                errorMessage.textContent = 'Please select a file first.';
                isUploading = false;
                uploadSpinner.classList.add('d-none');
                return;
            }

            // Submit form
            fetch('/api/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.error || 'Upload failed');
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.redirect) {
                    window.location.href = data.redirect;
                } else {
                    throw new Error('Invalid server response');
                }
            })
            .catch(error => {
                errorDiv.classList.remove('d-none');
                errorMessage.textContent = error.message || 'Error uploading image. Please try again.';
                console.error('Upload error:', error);
            })
            .finally(() => {
                isUploading = false;
                uploadSpinner.classList.add('d-none');
                analyzeBtn.disabled = false;
            });
        });
    }

    // Remove button functionality
    const removeButton = document.getElementById('removeImage');
    if (removeButton) {
        removeButton.addEventListener('click', function() {
            fileInput.value = '';
            preview.classList.add('d-none');
            uploadPrompt.classList.remove('d-none');
            analyzeBtn.disabled = true;
            errorDiv.classList.add('d-none');
        });
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    handleImageUpload();
});

// Handle service worker for PWA support
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
            console.log('ServiceWorker registration successful');
        }, function(err) {
            console.log('ServiceWorker registration failed: ', err);
        });
    });
}
