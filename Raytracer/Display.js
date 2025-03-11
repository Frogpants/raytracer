// Function to load the saved render data from localStorage (or SavedRenders.json)
function loadSavedRenderData() {
    const savedRenders = JSON.parse(localStorage.getItem('SavedRenders'));

    // Check if we have saved render data
    if (savedRenders && savedRenders.length > 0) {
        return savedRenders;
    } else {
        console.error("No saved render data found.");
        return [];
    }
}

// Function to render the video frames based on the saved pixel data
function renderVideo() {
    const savedRenders = loadSavedRenderData();  // Load all the saved render data
    let currentFrame = 0;  // Track the current frame
    const frameRate = 30;  // Number of frames per second (adjustable)
    const canvas = document.getElementById('videoCanvas');  // Assuming you have a canvas in your HTML
    const ctx = canvas.getContext('2d');  // Get the 2D context for drawing
    const totalFrames = savedRenders.length;  // Total number of frames to render

    // Set canvas size based on the first frame's width/height
    if (totalFrames > 0) {
        const firstRender = savedRenders[0];
        canvas.width = firstRender.width;
        canvas.height = firstRender.height;
    }

    // Function to render each frame of the "video"
    function displayFrame() {
        if (currentFrame < totalFrames) {
            const renderData = savedRenders[currentFrame];  // Get the current frame's data
            const pixelData = renderData.pixelData;  // Pixel color data for this frame

            // Clear the canvas before rendering the next frame
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Render each pixel
            pixelData.forEach((pixel) => {
                ctx.fillStyle = `rgb(${pixel.r}, ${pixel.g}, ${pixel.b})`;
                ctx.fillRect(pixel.x, pixel.y, 1, 1);  // Draw each pixel on the canvas
            });

            currentFrame++;  // Move to the next frame

            // Simulate frame rate by using requestAnimationFrame with a time interval
            setTimeout(() => {
                requestAnimationFrame(displayFrame);  // Call this function again for the next frame
            }, 1000 / frameRate);  // Wait for the next frame based on the frame rate
        } else {
            console.log("Video playback completed.");
        }
    }

    // Start the rendering process
    displayFrame();
}
