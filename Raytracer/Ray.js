import { camera } from './Camera.js';

const spheres = [];
const lights = [
    { x: 5, y: 5, z: 0, intensity: 1 },
    { x: -5, y: 5, z: 0, intensity: 0.5 }
];

const waterPlane = {
    y: -2,
    color: { r: 0, g: 100, b: 255 },
    reflectivity: 0.3,
    transparency: 0.7,
    waveStrength: 0.5
};

function loadObjectsFromJSON() {
    fetch('Objects.json')
        .then(response => response.json())
        .then(data => {
            data.objects.forEach(obj => {
                if (obj.type === "sphere") {
                    addSphere(obj.x, obj.y, obj.z, obj.radius, obj.color, obj.reflectivity, obj.transparency, obj.alpha);
                }
            });
        });
};

function addSphere(x, y, z, radius, color, reflectivity = 0, transparency = 0, alpha = 1) {
    spheres.push({ x, y, z, radius, color, reflectivity, transparency, alpha });
};

export function pixel(u, v) {
    const fovFactor = Math.tan((camera.FOV * Math.PI) / 360); 

    const direction = {
        x: (2 * u - 1) * fovFactor,
        y: (1 - 2 * v) * fovFactor,
        z: 1 
    };

    const cosRx = Math.cos(camera.rx);
    const sinRx = Math.sin(camera.rx);
    const cosRy = Math.cos(camera.ry);
    const sinRy = Math.sin(camera.ry);
    const cosRz = Math.cos(camera.rz);
    const sinRz = Math.sin(camera.rz);

    let dx = direction.x;
    let dy = direction.y * cosRx - direction.z * sinRx;
    let dz = direction.y * sinRx + direction.z * cosRx;

    let tempX = dx * cosRy + dz * sinRy;
    dz = -dx * sinRy + dz * cosRy;
    dx = tempX;

    let tempX2 = dx * cosRz - dy * sinRz;
    dy = dx * sinRz + dy * cosRz;
    dx = tempX2;

    ray.rx = dx;
    ray.ry = dy;
    ray.rz = dz;

    return applyPostProcessing(getPixelColor(ray, 3));
};

function getPixelColor(ray, depth) {
    if (depth <= 0) return { r: 0, g: 0, b: 0 };

    let closestColor = { r: 0, g: 0, b: 0 };
    let closestDist = Infinity;
    let closestSphere = null;

    // Water plane intersection
    if (ray.ry !== 0) {
        const t = (waterPlane.y - camera.y) / ray.ry;
        if (t > 0 && t < closestDist) {
            closestDist = t;
            closestSphere = 'WATER_PLANE';
        }
    }

    for (const sphere of spheres) {
        const oc = { x: camera.x - sphere.x, y: camera.y - sphere.y, z: camera.z - sphere.z };
        const a = ray.rx ** 2 + ray.ry ** 2 + ray.rz ** 2;
        const b = 2 * (oc.x * ray.rx + oc.y * ray.ry + oc.z * ray.rz);
        const c = oc.x ** 2 + oc.y ** 2 + oc.z ** 2 - sphere.radius ** 2;
        const discriminant = b ** 2 - 4 * a * c;

        if (discriminant > 0) {
            const t = (-b - Math.sqrt(discriminant)) / (2 * a);
            if (t < closestDist) {
                closestDist = t;
                closestSphere = sphere;
            }
        }
    }

    if (closestSphere) {
        if (closestSphere === 'WATER_PLANE') {
            const hitPoint = {
                x: camera.x + ray.rx * closestDist,
                y: camera.y + ray.ry * closestDist,
                z: camera.z + ray.rz * closestDist
            };

            const waveHeight = Math.sin(hitPoint.x * 0.2 + hitPoint.z * 0.2) * waterPlane.waveStrength;
            if (hitPoint.y < waterPlane.y + waveHeight) {
                const reflectedRay = { rx: ray.rx, ry: -ray.ry, rz: ray.rz };
                const reflectedColor = getPixelColor(reflectedRay, depth - 1);
                const transmittedColor = getPixelColor(ray, depth - 1);

                return {
                    r: waterPlane.color.r * (1 - waterPlane.transparency) + transmittedColor.r * waterPlane.transparency + reflectedColor.r * waterPlane.reflectivity,
                    g: waterPlane.color.g * (1 - waterPlane.transparency) + transmittedColor.g * waterPlane.transparency + reflectedColor.g * waterPlane.reflectivity,
                    b: waterPlane.color.b * (1 - waterPlane.transparency) + transmittedColor.b * waterPlane.transparency + reflectedColor.b * waterPlane.reflectivity
                };
            }
        }

        const hitPoint = {
            x: camera.x + ray.rx * closestDist,
            y: camera.y + ray.ry * closestDist,
            z: camera.z + ray.rz * closestDist
        };

        const baseColor = applyLighting(closestSphere.color, closestSphere, ray, closestDist);
        return baseColor;
    }

    return closestColor;
};

function applyPostProcessing(color) {
    const gamma = 2.2;
    return {
        r: Math.pow(color.r / 255, 1 / gamma) * 255,
        g: Math.pow(color.g / 255, 1 / gamma) * 255,
        b: Math.pow(color.b / 255, 1 / gamma) * 255
    };
};

loadObjectsFromJSON();
