import pygame
import numpy as np
from numba import njit

WIDTH, HEIGHT = 400, 300
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# ---------------------
# Voxel grid
# ---------------------
GRID_SIZE = 32
voxels = np.zeros((GRID_SIZE, GRID_SIZE, GRID_SIZE), dtype=np.int32)

# Simple shapes
voxels[12:20, 12:20, 12:20] = 1
voxels[4:8, 4:8, 4:8] = 2
voxels[0:32, 0:2, 20:22] = 3
for i in range(10,20):
    voxels[i,i,5] = 4

colors = np.array([
    [0,0,0],
    [255,0,0],
    [0,255,0],
    [0,0,255],
    [255,255,0]
], dtype=np.uint8)

# ---------------------
# Camera
# ---------------------
cam_pos = np.array([16.0, 16.0, -10.0])
fov = 60
aspect = WIDTH / HEIGHT
scale = np.tan(np.radians(fov * 0.5))

# ---------------------
# Light
# ---------------------
light_dir = np.array([1,1,-1])
light_dir = light_dir / np.linalg.norm(light_dir)

# ---------------------
# 3D DDA Raycasting
# ---------------------
@njit
def cast_dda(voxels, cam_pos, ray_dir):
    x, y, z = cam_pos
    dx, dy, dz = ray_dir
    ix, iy, iz = int(x), int(y), int(z)

    step_x = 1 if dx >= 0 else -1
    step_y = 1 if dy >= 0 else -1
    step_z = 1 if dz >= 0 else -1

    t_max_x = ((ix + (step_x>0)) - x)/dx if dx !=0 else 1e10
    t_max_y = ((iy + (step_y>0)) - y)/dy if dy !=0 else 1e10
    t_max_z = ((iz + (step_z>0)) - z)/dz if dz !=0 else 1e10

    t_delta_x = abs(1/dx) if dx !=0 else 1e10
    t_delta_y = abs(1/dy) if dy !=0 else 1e10
    t_delta_z = abs(1/dz) if dz !=0 else 1e10

    for _ in range(200):
        if 0 <= ix < voxels.shape[0] and 0 <= iy < voxels.shape[1] and 0 <= iz < voxels.shape[2]:
            val = voxels[ix, iy, iz]
            if val != 0:
                return val
        # step to next voxel
        if t_max_x < t_max_y:
            if t_max_x < t_max_z:
                ix += step_x
                t_max_x += t_delta_x
            else:
                iz += step_z
                t_max_z += t_delta_z
        else:
            if t_max_y < t_max_z:
                iy += step_y
                t_max_y += t_delta_y
            else:
                iz += step_z
                t_max_z += t_delta_z
    return 0

@njit
def render(voxels, colors, cam_pos, WIDTH, HEIGHT):
    buf = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for y in range(HEIGHT):
        py = (1 - 2*(y+0.5)/HEIGHT) * scale
        for x in range(WIDTH):
            px = (2*(x+0.5)/WIDTH - 1) * scale * aspect
            ray_dir = np.array([px, py, 1.0])
            ray_dir /= np.linalg.norm(ray_dir)
            voxel_idx = cast_dda(voxels, cam_pos, ray_dir)
            if voxel_idx != 0:
                shade = max(0.3, np.dot(ray_dir, -light_dir))
                buf[y,x] = colors[voxel_idx] * shade
    return buf

# ---------------------
# Main loop
# ---------------------
running = True
angle = 0.0

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    # Rotate camera around Y
    angle += 0.01
    cam_pos[0] = 16 + np.sin(angle)*40
    cam_pos[2] = -10 + np.cos(angle)*40

    buf = render(voxels, colors, cam_pos, WIDTH, HEIGHT)
    surf = pygame.surfarray.make_surface(buf.swapaxes(0,1))
    screen.blit(surf, (0,0))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
