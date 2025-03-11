import { camera } from './Camera.js';

function Move(speed) {
    camera.x += speed * Math.sin(camera.rx);
    camera.z += speed * Math.cos(camera.rx);
};

function Control(speed) {
    if (keyDown === "w") {
        Move(speed);
    }
    if (keyDown === "s") {
        Move(-speed);
    }
    camera.rx += 90;
    if (keyDown === "d") {
        Move(speed);
    }
    if (keyDown === "a") {
        Move(-speed);
    }
    camera.rx -= 90;
};

window.addEventListener('keydown', (event) => {
    const keyDown = event.key;
});