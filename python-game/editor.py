# import pygame
# pygame.init()

# # --- Setup ---
# WIDTH, HEIGHT = 800, 600
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Slideable Tile Editor Menu")

# font = pygame.font.SysFont(None, 28)
# clock = pygame.time.Clock()

# # --- Data ---
tile_data = {
    "x": 0,
    "y": 0,
    "type": 0,
    "collidable": False,
    "interactable": False,
    "layer": 1
}

# def tile_package(x=0, y=0, type=0, collidable=False, interactable=False, layer=1):
#     return {"x": x, "y": y, "type": type, "collidable": collidable, "interactable": interactable, "layer": layer}

# # --- Drawer Settings ---
# drawer_width = 300
# drawer_x = -drawer_width
# drawer_target_x = -drawer_width
# drawer_speed = 15
# buttons = []

# # --- Gear Button (always visible) ---
# toggle_button = pygame.Rect(10, 10, 40, 40)

# def toggle_drawer():
#     """Slide drawer in or out."""
#     global drawer_target_x
#     drawer_target_x = 0 if drawer_x < 0 else -drawer_width

# def update_drawer():
#     """Smooth animation of the drawer."""
#     global drawer_x
#     if drawer_x < drawer_target_x:
#         drawer_x = min(drawer_x + drawer_speed, drawer_target_x)
#     elif drawer_x > drawer_target_x:
#         drawer_x = max(drawer_x - drawer_speed, drawer_target_x)

# # --- Button Handling ---
# def make_button(rect, label, action, kind="button", checked=False):
#     buttons.append({
#         "rect": pygame.Rect(rect),
#         "label": label,
#         "action": action,
#         "kind": kind,
#         "checked": checked
#     })

# def create_buttons():
#     """Rebuild the button list with updated values."""
#     buttons.clear()
#     y_offset = 80
#     for key, value in tile_data.items():
#         base_x = drawer_x + 20
#         if isinstance(value, bool):
#             # Checkbox toggle
#             make_button((base_x, y_offset, 25, 25), key, lambda k=key: toggle_bool(k), kind="checkbox", checked=value)
#         else:
#             # Numeric controls
#             make_button((base_x, y_offset, 160, 30), f"{key}: {value}", None)
#             make_button((base_x + 170, y_offset, 30, 30), "+", lambda k=key: increment(k, 1))
#             make_button((base_x + 210, y_offset, 30, 30), "-", lambda k=key: increment(k, -1))
#         y_offset += 45

# def increment(key, amount):
#     if isinstance(tile_data[key], (int, float)):
#         tile_data[key] += amount

# def toggle_bool(key):
#     tile_data[key] = not tile_data[key]

# def handle_mouse_click(pos):
#     """Handle click for gear and drawer buttons."""
#     # Gear icon (always clickable)
#     if toggle_button.collidepoint(pos):
#         toggle_drawer()
#         return

#     # Menu buttons
#     for btn in buttons:
#         if btn["rect"].collidepoint(pos) and btn["action"]:
#             btn["action"]()
#             break

# # --- Drawing ---
# def draw_checkbox(rect, checked):
#     pygame.draw.rect(screen, (180, 180, 180), rect, 2)
#     if checked:
#         pygame.draw.line(screen, (0, 255, 0), (rect.x+4, rect.y+12), (rect.x+10, rect.y+20), 3)
#         pygame.draw.line(screen, (0, 255, 0), (rect.x+10, rect.y+20), (rect.x+22, rect.y+4), 3)

# def draw_buttons():
#     for btn in buttons:
#         if btn["kind"] == "checkbox":
#             draw_checkbox(btn["rect"], tile_data[btn["label"]])
#             label = font.render(btn["label"], True, (255, 255, 255))
#             screen.blit(label, (btn["rect"].x + 35, btn["rect"].y + 2))
#         else:
#             pygame.draw.rect(screen, (60, 60, 60), btn["rect"])
#             pygame.draw.rect(screen, (150, 150, 150), btn["rect"], 2)
#             text = font.render(btn["label"], True, (255, 255, 255))
#             screen.blit(text, (btn["rect"].x + 5, btn["rect"].y + 5))

# def draw_toggle_button():
#     """Draws the always-visible gear icon."""
#     pygame.draw.rect(screen, (50, 50, 50), toggle_button, border_radius=8)
#     pygame.draw.rect(screen, (200, 200, 200), toggle_button, 2, border_radius=8)
#     center = toggle_button.center
#     for i in range(6):
#         angle = i * 60
#         vec = pygame.math.Vector2(1, 0).rotate(angle)
#         x = center[0] + 10 * vec.x
#         y = center[1] + 10 * vec.y
#         pygame.draw.circle(screen, (230, 230, 230), (int(x), int(y)), 3)
#     pygame.draw.circle(screen, (230, 230, 230), center, 5)

# # --- Main Loop ---
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             handle_mouse_click(event.pos)

#     # Example background (your game world here)
#     screen.fill((10, 10, 25))
#     pygame.draw.circle(screen, (255, 180, 50), (WIDTH // 2, HEIGHT // 2), 50)

#     # --- Drawer logic ---
#     update_drawer()

#     # Draw drawer if visible
#     if drawer_x > -drawer_width:
#         pygame.draw.rect(screen, (30, 30, 30), (drawer_x, 0, drawer_width, HEIGHT))
#         create_buttons()
#         draw_buttons()

#         # Show preview
#         preview = tile_package(**tile_data)
#         preview_text = font.render(str(preview), True, (100, 200, 255))
#         screen.blit(preview_text, (drawer_x + 20, HEIGHT - 40))

#     # Always draw the gear icon on top
#     draw_toggle_button()

#     pygame.display.flip()
#     clock.tick(60)

# pygame.quit()
