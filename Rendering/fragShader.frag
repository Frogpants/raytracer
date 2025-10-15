
#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform float u_time;

#define MAX_STEPS 1000
#define MAX_DIST 1.0
#define VOXEL_SIZE 0.1

vec3 lightDir = normalize(vec3(-0.5, 1.0, -0.3));

float hash(vec3 p) {
    return fract(sin(dot(p, vec3(127.1, 311.7, 74.7))) * 43758.5453);
}

bool voxelExists(ivec3 cell) {
    // Only one flat plane of voxels at y == 0
    return cell.y == 0;
}

vec2 rayBox(vec3 ro, vec3 rd, vec3 minB, vec3 maxB) {
    vec3 invDir = 1.0 / rd;
    vec3 t0s = (minB - ro) * invDir;
    vec3 t1s = (maxB - ro) * invDir;
    vec3 tsmaller = min(t0s, t1s);
    vec3 tbigger = max(t0s, t1s);
    float tmin = max(max(tsmaller.x, tsmaller.y), tsmaller.z);
    float tmax = min(min(tbigger.x, tbigger.y), tbigger.z);
    return vec2(tmin, tmax);
}

void main() {
    vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution) / u_resolution.y;

    vec3 ro = vec3(0.0, 2.0, 5.0);
    vec3 rd = normalize(vec3(uv, -1.5));

    vec3 color = vec3(0.6, 0.8, 1.0); // background sky
    float closestT = 1e9;

    vec3 pos = floor(ro / VOXEL_SIZE);
    vec3 stepDir = sign(rd);
    vec3 tMax = ((pos + stepDir * 0.5 + 0.5) * VOXEL_SIZE - ro) / rd;
    vec3 tDelta = stepDir * VOXEL_SIZE / rd;

    for (int i = 0; i < MAX_STEPS; i++) {
        ivec3 cell = ivec3(pos);

        if (voxelExists(cell)) {
            vec3 minB = vec3(cell) * VOXEL_SIZE;
            vec3 maxB = minB + VOXEL_SIZE;
            vec2 hit = rayBox(ro, rd, minB, maxB);

            if (hit.x < hit.y && hit.y > 0.0) {
                float t = max(hit.x, 0.0);
                if (t < closestT) {
                    vec3 hp = ro + rd * t;

                    vec3 normal = vec3(0.0);
                    float eps = 0.001;
                    if (abs(hp.x - minB.x) < eps) normal = vec3(-1,0,0);
                    else if (abs(hp.x - maxB.x) < eps) normal = vec3(1,0,0);
                    else if (abs(hp.y - minB.y) < eps) normal = vec3(0,-1,0);
                    else if (abs(hp.y - maxB.y) < eps) normal = vec3(0,1,0);
                    else if (abs(hp.z - minB.z) < eps) normal = vec3(0,0,-1);
                    else if (abs(hp.z - maxB.z) < eps) normal = vec3(0,0,1);

                    float diff = max(dot(normal, lightDir), 0.0);
                    float brightnessVar = 0.8 + 0.2 * hash(vec3(cell));
                    color = vec3(0.6,0.6,0.6) * diff * brightnessVar;
                    closestT = t;
                }
            }
        }

        if (tMax.x < tMax.y && tMax.x < tMax.z) {
            tMax.x += tDelta.x;
            pos.x += stepDir.x;
        } else if (tMax.y < tMax.z) {
            tMax.y += tDelta.y;
            pos.y += stepDir.y;
        } else {
            tMax.z += tDelta.z;
            pos.z += stepDir.z;
        }
    }

    gl_FragColor = vec4(color, 1.0);
}
