// Import necessary objects
import { ray, lights } from './Ray.js';  // Import ray and lights from Ray.js
import { spheres, waterPlane } from './SceneObjects.js';  // Import scene objects

// A utility function to calculate the dot product of two vectors
function dotProduct(v1, v2) {
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
}

// A utility function to calculate the normalized vector
function normalize(v) {
    const length = Math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2);
    return { x: v.x / length, y: v.y / length, z: v.z / length };
}

// Function to calculate the color based on the lighting effects (shadows, reflections, refractions, fog, etc.)
export function applyLighting(ray, hitPoint, normal, material, depth) {
    let color = { r: 0, g: 0, b: 0 }; // Default to black (no color)

    // Calculate ambient light contribution
    const ambientLight = 0.1;  // A constant value for ambient light
    color.r += ambientLight * material.color.r;
    color.g += ambientLight * material.color.g;
    color.b += ambientLight * material.color.b;

    // Loop through each light source to calculate the diffuse and specular components
    lights.forEach(light => {
        // Calculate the direction from the hit point to the light source
        const lightDir = { x: light.x - hitPoint.x, y: light.y - hitPoint.y, z: light.z - hitPoint.z };
        const lightDistance = Math.sqrt(lightDir.x ** 2 + lightDir.y ** 2 + lightDir.z ** 2);
        const normalizedLightDir = normalize(lightDir);

        // Check for shadows: A simple shadow check by tracing a ray from the hit point to the light
        const shadowRay = { rx: normalizedLightDir.x, ry: normalizedLightDir.y, rz: normalizedLightDir.z };
        const shadowRayOrigin = { x: hitPoint.x + normal.x * 0.001, y: hitPoint.y + normal.y * 0.001, z: hitPoint.z + normal.z * 0.001 }; // A small offset to avoid self-intersection
        if (!isInShadow(shadowRay, shadowRayOrigin, lightDistance)) {
            // Diffuse lighting (Lambertian reflection)
            const diffuseFactor = Math.max(dotProduct(normal, normalizedLightDir), 0);
            color.r += diffuseFactor * material.color.r * light.intensity;
            color.g += diffuseFactor * material.color.g * light.intensity;
            color.b += diffuseFactor * material.color.b * light.intensity;

            // Specular lighting (Phong reflection model)
            const viewDir = normalize({ x: ray.rx, y: ray.ry, z: ray.rz });
            const reflectionDir = { 
                x: 2 * dotProduct(normal, normalizedLightDir) * normal.x - normalizedLightDir.x,
                y: 2 * dotProduct(normal, normalizedLightDir) * normal.y - normalizedLightDir.y,
                z: 2 * dotProduct(normal, normalizedLightDir) * normal.z - normalizedLightDir.z
            };
            const specularFactor = Math.pow(Math.max(dotProduct(viewDir, reflectionDir), 0), material.shininess);
            color.r += specularFactor * light.intensity * material.specularColor.r;
            color.g += specularFactor * light.intensity * material.specularColor.g;
            color.b += specularFactor * light.intensity * material.specularColor.b;
        }
    });

    // Reflections
    if (material.reflectivity > 0 && depth > 0) {
        const reflectionRay = reflectRay(ray, hitPoint, normal);
        const reflectionColor = getPixelColor(reflectionRay, depth - 1); // Recursively calculate the reflection color
        color.r += reflectionColor.r * material.reflectivity;
        color.g += reflectionColor.g * material.reflectivity;
        color.b += reflectionColor.b * material.reflectivity;
    }

    // Refraction (for transparent materials like water)
    if (material.transparency > 0 && depth > 0) {
        const refractionRay = refractRay(ray, hitPoint, normal, material.refractiveIndex);
        const refractionColor = getPixelColor(refractionRay, depth - 1); // Recursively calculate the refraction color
        color.r += refractionColor.r * material.transparency;
        color.g += refractionColor.g * material.transparency;
        color.b += refractionColor.b * material.transparency;
    }

    // Apply the fog effect for transparent materials
    if (material.transparency > 0) {
        const fogEffect = calculateFog(hitPoint, material.alpha);
        color.r = blendWithFog(color.r, fogEffect, material.alpha);
        color.g = blendWithFog(color.g, fogEffect, material.alpha);
        color.b = blendWithFog(color.b, fogEffect, material.alpha);
    }

    // Ensure that the color values are within valid RGB range (0-255)
    color.r = Math.min(Math.max(color.r, 0), 255);
    color.g = Math.min(Math.max(color.g, 0), 255);
    color.b = Math.min(Math.max(color.b, 0), 255);

    return color;
}

// Function to check if a point is in shadow (ray-tracing)
function isInShadow(shadowRay, shadowRayOrigin, lightDistance) {
    for (const obj of spheres) {
        const t = intersectRayWithSphere(shadowRayOrigin, shadowRay, obj);
        if (t > 0 && t < lightDistance) {
            return true;  // The point is in shadow
        }
    }

    // Check for water plane shadow (you could add more objects here)
    if (shadowRay.ry !== 0) {
        const t = (waterPlane.y - shadowRayOrigin.y) / shadowRay.ry;
        if (t > 0 && t < lightDistance) {
            return true;  // The point is in shadow
        }
    }

    return false;  // The point is not in shadow
}

// Function to reflect the ray (used for reflections)
function reflectRay(ray, hitPoint, normal) {
    const dotProd = dotProduct(ray, normal);
    return {
        rx: ray.rx - 2 * dotProd * normal.x,
        ry: ray.ry - 2 * dotProd * normal.y,
        rz: ray.rz - 2 * dotProd * normal.z
    };
}

// Function to calculate refraction (used for transparent objects)
function refractRay(ray, hitPoint, normal, refractiveIndex) {
    const dotProd = dotProduct(ray, normal);
    const k = 1 - refractiveIndex ** 2 * (1 - dotProd ** 2);
    if (k < 0) return null;  // Total internal reflection
    const refractionDir = {
        x: refractiveIndex * ray.rx - (refractiveIndex * dotProd + Math.sqrt(k)) * normal.x,
        y: refractiveIndex * ray.ry - (refractiveIndex * dotProd + Math.sqrt(k)) * normal.y,
        z: refractiveIndex * ray.rz - (refractiveIndex * dotProd + Math.sqrt(k)) * normal.z
    };
    return refractionDir;
}

// Utility to calculate ray-object intersection (for shadow checking and other purposes)
function intersectRayWithSphere(rayOrigin, rayDir, sphere) {
    const oc = { x: rayOrigin.x - sphere.x, y: rayOrigin.y - sphere.y, z: rayOrigin.z - sphere.z };
    const a = rayDir.x ** 2 + rayDir.y ** 2 + rayDir.z ** 2;
    const b = 2 * (oc.x * rayDir.x + oc.y * rayDir.y + oc.z * rayDir.z);
    const c = oc.x ** 2 + oc.y ** 2 + oc.z ** 2 - sphere.radius ** 2;
    const discriminant = b ** 2 - 4 * a * c;

    if (discriminant < 0) return -1;  // No intersection
    return (-b - Math.sqrt(discriminant)) / (2 * a);  // Return the distance to the intersection point
}

// Calculate fog effect based on distance from the camera and transparency
function calculateFog(hitPoint, alpha) {
    const fogDensity = 0.1;  // Density of the fog
    const distance = Math.sqrt(hitPoint.x ** 2 + hitPoint.y ** 2 + hitPoint.z ** 2);  // Distance from the camera (origin)
    return Math.exp(-fogDensity * distance) * alpha;  // Exponential fog effect
}

// Blend color with fog effect (more fog for more transparent objects)
function blendWithFog(color, fogEffect, alpha) {
    return color * (1 - fogEffect) + fogEffect * 255;  // Blend fog effect with the color
}
