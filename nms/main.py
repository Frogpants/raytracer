import pygame
import math as m

width, height = 1280, 720

hw, hh = width/2, height/2
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Universe")

universe_seed = 999
chunk_size = 500

camx, camy, camz = 0, 0, 0
speed = 8

rotx, roty = 0, 0
rotspeed = 0.4

# NEW: chunk streaming system
loaded_chunks = {}           # {(cx,cy,cz): [stars]}
render_distance = 8         # how many chunks away to load


def distance(pos):
    return m.sqrt((pos[0]-camx)**2 + (pos[1]-camy)**2 + (pos[2]-camz)**2)


def move(speed):
    global camx, camz, rotx

    rx = m.radians(rotx)
    camx += speed * m.sin(rx)
    camz += speed * m.cos(rx)


def goto(pos):
    rx, ry = m.radians(rotx), m.radians(roty)
    x, y, z = pos[0] - camx, pos[1] - camy, pos[2] - camz
    x, z = x*m.cos(rx) - z*m.sin(rx), x*m.sin(rx) + z*m.cos(rx)
    y, z = y*m.cos(ry) - z*m.sin(ry), y*m.sin(ry) + z*m.cos(ry)
    if (z <= 0.1):
        z = 0.1
    x, y = hw*(x/z), hw*(y/z)
    return [x, y]


def skybox(pos):
    rx, ry = m.radians(rotx), m.radians(roty)
    x, y, z = pos[0] - camx, pos[1] - camy, pos[2] - camz
    dist = distance(pos)
    x, z = x*m.cos(rx) - z*m.sin(rx), x*m.sin(rx) + z*m.cos(rx)
    y, z = y*m.cos(ry) - z*m.sin(ry), y*m.sin(ry) + z*m.cos(ry)
    if (z <= 0.1):
        z = 0.1
    x, y, z = 1000*(x/dist), 1000*(y/dist), 1000*(z/dist)
    x, y = hw*(x/z), hw*(y/z)
    return [x, y]


def seeded_value(x, y, z):
    return (((x * 374761) + (y * 668265) + (z * 987643) +
             (universe_seed * 12345.6789)) * 43758.5453) % 1


def solar_rng(x, y, z, offset):
    return seeded_value((x*13.13 + y*7.77) + (universe_seed*offset),
                        y+offset, z*12.12+y*9.99)


def star_density(x, y, z):
    return seeded_value(x*1.1, y*1.3, z*0.9)


def generate_planets(star):
    x = star[0]
    y = star[1]
    z = star[2]
    base = solar_rng(x, y, z, 1000)
    planets = []
    base_orbit = 0.3 + solar_rng(x, y, z, 2000)*1.5
    growth = 1.8 + solar_rng(x, y, z, 3000)*0.7
    count = int(1 + base*6)
    for i in range(0, count):
        orbit = base_orbit * growth**i
        orbit *= 1 + solar_rng(x, y, z, 4000+i)*0.5
        size = 1.2 + solar_rng(x, y, z, 5000+i)*5
        planets.append([orbit, size])
    return planets


def generate_local_chunks(gx, gy, gz):
    tempx = gx * chunk_size
    tempy = gy * chunk_size
    tempz = gz * chunk_size
    chunk = []
    density = star_density(tempx, tempy, tempz)
    expected = density * 2 * 0.0008 * (1 / (chunk_size/1000))
    count = int(expected * chunk_size * 2.5)
    for i in range(0, count):
        r = seeded_value(gx + (i*17), gy + (i*29), gz + (i*41))
        x = tempx + (seeded_value(r, i, expected)*chunk_size)
        y = tempy + (seeded_value(i, expected, r)*chunk_size)
        z = tempz + (seeded_value(expected, r, i)*chunk_size)
        star = [x, y, z]
        planets = generate_planets(star)
        star.append(planets)
        star.append(density)
        chunk.append(star)
    return chunk


# NEW — replaces generate_chunks()
def update_chunks():
    global loaded_chunks

    # camera chunk coordinates
    ccx = int(camx // chunk_size)
    ccy = int(camy // chunk_size)
    ccz = int(camz // chunk_size)

    needed = set()
    for x in range(ccx - render_distance, ccx + render_distance + 1):
        for y in range(ccy - render_distance, ccy + render_distance + 1):
            for z in range(ccz - render_distance, ccz + render_distance + 1):
                needed.add((x, y, z))

    # load missing chunks
    for c in needed:
        if c not in loaded_chunks:
            loaded_chunks[c] = generate_local_chunks(*c)

    # unload far chunks
    for c in list(loaded_chunks.keys()):
        if c not in needed:
            del loaded_chunks[c]


def render(stars):
    for star in stars:
        dist = distance(star)

        if (dist < 2):
            pos = goto(star)
            pygame.draw.circle(screen, (255, 255, 255),
                               (pos[0]+hw, pos[1]+hh), dist*1)
        else:
            pos = skybox(star)
            pygame.draw.circle(screen, (255, 255, 255),
                               (pos[0]+hw, pos[1]+hh), star[4]*2)


# removed: chunks = generate_chunks(10)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    rotx += 90
    if keys[pygame.K_a]:
        move(-speed)
    if keys[pygame.K_d]:
        move(speed)
    rotx += -90

    if keys[pygame.K_w]:
        move(speed)
    if keys[pygame.K_s]:
        move(-speed)

    if keys[pygame.K_e]:
        camy += -speed
    if keys[pygame.K_q]:
        camy += speed

    if keys[pygame.K_RIGHT]:
        rotx += rotspeed
    if keys[pygame.K_LEFT]:
        rotx += -rotspeed
    if keys[pygame.K_UP]:
        roty += -rotspeed
    if keys[pygame.K_DOWN]:
        roty += rotspeed

    # NEW: dynamic chunk streaming
    update_chunks()

    # flatten visible stars into one list
    chunks = []
    for c in loaded_chunks.values():
        chunks += c

    render(chunks)

    pygame.display.flip()

pygame.quit()
