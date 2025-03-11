import { pixel } from './Main.js';  // Import the pixel color function from your main code

// Function to render the scene with quality control
export function renderScene(width, height, quality = 1) {
    // Initialize an array to store the pixel data
    const pixelData = [];

    // Loop through each pixel in the canvas
    for (let v = 0; v < height; v++) {
        for (let u = 0; u < width; u++) {
            // Depending on quality, adjust the amount of detail
            const pixelColor = getPixelColorWithQuality(u, v, width, height, quality);
            const r = Math.floor(pixelColor.r);
            const g = Math.floor(pixelColor.g);
            const b = Math.floor(pixelColor.b);

            // Save the pixel data as an object
            pixelData.push({ x: u, y: v, r, g, b });
        }
    }

    // Save the pixel data to JSON file
    saveRenderData({
        type: 'image',
        width: width,
        height: height,
        quality: quality,
        pixelData: pixelData,
        timestamp: Date.now()
    });
};

function getPixelColorWithQuality(u, v, width, height, quality) {
    let finalColor = { r: 0, g: 0, b: 0 };

    // For higher quality, average over more samples
    const sampleCount = Math.max(1, Math.floor(quality));  // Number of samples based on quality

    for (let i = 0; i < sampleCount; i++) {
        // You can randomize the sample to add anti-aliasing effects based on quality
        const offsetU = (u + Math.random() * 0.5 - 0.25) / width;
        const offsetV = (v + Math.random() * 0.5 - 0.25) / height;

        // Get the pixel color from the pixel function (you can apply anti-aliasing or more detail with randomization)
        const color = pixel(offsetU, offsetV);  // Normalize u, v coordinates based on quality
        
        finalColor.r += color.r;
        finalColor.g += color.g;
        finalColor.b += color.b;
    }

    // Average the color based on the number of samples
    finalColor.r /= sampleCount;
    finalColor.g /= sampleCount;
    finalColor.b /= sampleCount;

    return finalColor;
};

// Function to save the pixel data to SavedRenders.json
export function saveRenderData(renderData) {
    // Fetch existing data from the SavedRenders.json file or create an empty array if it doesn't exist
    const savedRenders = JSON.parse(localStorage.getItem('SavedRenders')) || [];

    // Add the new render metadata to the array
    savedRenders.push(renderData);

    // Save the updated array back to local storage
    localStorage.setItem('SavedRenders', JSON.stringify(savedRenders));
};
