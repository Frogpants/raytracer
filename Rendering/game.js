const canvas = document.getElementById("glcanvas");
const gl = canvas.getContext("webgl");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Load shaders from files
async function loadShader(url) {
  const res = await fetch(url);
  return await res.text();
}

const vertSrc = await loadShader("vertShader.vert");
const fragSrc = await loadShader("fragShader.frag");

function compile(src, type) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, src);
  gl.compileShader(shader);
  if(!gl.getShaderParameter(shader, gl.COMPILE_STATUS))
    console.error(gl.getShaderInfoLog(shader));
  return shader;
}

const vs = compile(vertSrc, gl.VERTEX_SHADER);
const fs = compile(fragSrc, gl.FRAGMENT_SHADER);

const prog = gl.createProgram();
gl.attachShader(prog, vs);
gl.attachShader(prog, fs);
gl.linkProgram(prog);
gl.useProgram(prog);

// Fullscreen quad
const buf = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1,1,-1,-1,1,1,1]), gl.STATIC_DRAW);
const a_pos = gl.getAttribLocation(prog,"a_pos");
gl.enableVertexAttribArray(a_pos);
gl.vertexAttribPointer(a_pos,2,gl.FLOAT,false,0,0);

const u_camPos = gl.getUniformLocation(prog,"u_camPos");
const u_camRot = gl.getUniformLocation(prog,"u_camRot");
const u_time = gl.getUniformLocation(prog,"u_time");

let cam = {x:0, y:2, z:5, yaw:0, pitch:0};
let keys = {};

document.addEventListener("keydown", e => keys[e.key] = true);
document.addEventListener("keyup", e => keys[e.key] = false);

function loop(t) {
    const speed = 0.05;
    if(keys["w"]) cam.z -= speed;
    if(keys["s"]) cam.z += speed;
    if(keys["a"]) cam.x -= speed;
    if(keys["d"]) cam.x += speed;
    if(keys["ArrowLeft"]) cam.yaw -= 0.02;
    if(keys["ArrowRight"]) cam.yaw += 0.02;
    if(keys["ArrowUp"]) cam.pitch += 0.02;
    if(keys["ArrowDown"]) cam.pitch -= 0.02;

    gl.uniform3f(u_camPos, cam.x, cam.y, cam.z);
    gl.uniform2f(u_camRot, cam.yaw, cam.pitch);
    gl.uniform1f(u_time, t*0.001);

    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    requestAnimationFrame(loop);
}
loop();
