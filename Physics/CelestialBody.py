import physics
import turtle as t

time = physics.Time()

physics.deleteAllObjects()

balls = []
for x in range(-1,2):
    ball = physics.Rigidbody2D([x * 100, 0], [0, 0], 1, 0)
    obj = t.Turtle()
    obj.pencolor("white")
    obj.shape("circle",)
    obj.shapesize(stretch_wid=1, stretch_len=1)
    obj.penup()
    balls.append((obj, ball))

t.setup(width=800, height=800)
t.bgcolor("black")

t.speed(0)
t.penup()

def game_loop():
    for obj, ball in balls:
        ball.gravity(2, 1)
        ball.updateObj()
        obj.goto(ball.position)

    t.ontimer(game_loop, 16)

game_loop()

t.done()
