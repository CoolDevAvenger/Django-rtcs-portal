document.addEventListener("DOMContentLoaded", function () {
    const trySamplesLink = document.querySelector('.samples');
    const modalContainer = document.querySelector('.modal_active');
    const modalCloseBtn = document.querySelector('.modal_close_btn');
    const sampleImages = document.querySelectorAll('.sample_image');
    const fileInput = document.getElementById("file-input");
    const fileInputLabel = document.querySelector(".file-upload .choose_btn");
    const fileUploadContainer = document.querySelector('.file-upload');
    const apiProgressContainer = document.getElementById("api-progress-container");
    const apiResponseContainer = document.getElementById("apiResponseContainer");
    const progressContainer = document.getElementById("progressContainer");
const progressImage = document.getElementById("progressImage");
const nameBarContainer = document.getElementById("nameBarContainer");
    const progressBar = document.getElementById("progress-bar"); // Add this line


    


    // Function to show the modal
    const showModal = () => {
        modalContainer.style.display = 'flex';
       
    };

    // Function to hide the modal
    const hideModal = () => {
        modalContainer.style.display = 'none';
       
    };

    // Event listener for "Try samples" link
    trySamplesLink.addEventListener('click', (event) => {
        event.preventDefault();
    
        showModal();
        
        
    });

    // Event listener for modal close button
    modalCloseBtn.addEventListener('click', hideModal);

    // Close modal if user clicks outside the modal content
    window.addEventListener('click', (event) => {
        if (event.target === modalContainer) {
            hideModal();
        }
    });

    

    // Add event listener for file input change
fileInput.addEventListener("change", function () {
handleFileUpload();
// Reset progress bar
progressBar.style.width = "0%";
document.getElementById("progress-text").textContent = "Uploading...";

apiProgressContainer.style.display = "flex";


// Simulate file upload progress (replace this with your actual upload logic)
var progress = 0;
var interval = setInterval(function () {
    progress += 2;
    progressBar.style.width = progress + "%";

    if (progress >= 100) {
        clearInterval(interval);
        document.getElementById("progress-text").textContent = "Processing...";

        // Simulate API processing (replace this with your actual API call)
        setTimeout(function () {
            const apiResponse = 'API response goes here';
            updateAPIResponse(apiResponse);
            apiProgressContainer.style.display = "flex";
    }, 2000);
        
    }

}, 100);

});




    

    function displaySelectedImage(imageUrl) {
        const imgContainer = document.querySelector(".file-upload img");
        imgContainer.src = imageUrl;
        fileInputLabel.textContent = "Change File";
        
        
        const resetButton = document.createElement('img');
        resetButton.src = 'https://cdn3.iconfinder.com/data/icons/bold-media-player-ui/100/Retry-1024.png';
        resetButton.alt = 'Reset Image';
        resetButton.style = 'width: 30px; height: 30px; cursor: pointer; margin-left: 10px;';

        fileUploadContainer.innerHTML = ''; // Clear existing content
        fileUploadContainer.appendChild(imgContainer);
        fileUploadContainer.appendChild(resetButton);
       

        imgContainer.style.maxWidth = '50%';
        imgContainer.style.height = 'auto';

        resetButton.addEventListener('click', resetCard);

        const sampleContainer = document.querySelector('.sample_container');
        if (sampleContainer) {
            sampleContainer.style.display = 'none';
        }

      hideModal();
    }
        sampleImages.forEach((image) => {
            image.addEventListener('click', function () {
                const imageUrl = image.src;
                fileInput.value = "";
                displaySelectedImage(imageUrl);
    
                // Close the modal or perform other actions
               
            });
        });
    
        
    
        function resetCard() {
            fileUploadContainer.innerHTML = '<img src="" alt="Selected Image" style="max-width: 50%; height: auto;">';
            const sampleContainer = document.querySelector('.sample_container');
            if (sampleContainer) {
                sampleContainer.style.display = 'block';
            }
    
         showModal();
         apiProgressContainer.style.display = "none";
        }
    
        function updateAPIResponse(response) {
            // Update the content of the API response container
            apiResponseContainer.innerHTML = response;
    
            // Display the reset button after receiving the API response
            const resetButton = document.createElement('img');
            resetButton.src = 'https://cdn3.iconfinder.com/data/icons/bold-media-player-ui/100/Retry-1024.png';
            resetButton.alt = 'Reset Image';
            resetButton.style = 'width: 30px; height: 30px; cursor: pointer; margin-top: 10px;';
            resetButton.addEventListener('click', resetCard);
    
            apiProgressContainer.appendChild(resetButton);
        }
    
    
    
            
        
    


         


    }); 