import turtle
import random
import time

# Sprite class that inherits from Turtle
class Sprite(turtle.Turtle):
    def __init__(self, color, shape, x, y, stride=20):
        super().__init__()
        self.color(color)
        self.shape(shape)
        self.penup()
        self.goto(x, y)
        self.stride = stride
        self.direction = random.choice(['up', 'down', 'left', 'right'])
# Movement methods for player control
    def move_left(self):
        self.setx(self.xcor() - self.stride)

    def move_right(self):
        self.setx(self.xcor() + self.stride)

    def move_up(self):
        self.sety(self.ycor() + self.stride)

    def move_down(self):
        self.sety(self.ycor() - self.stride)
# Method to set direction for obstacles
    def set_move(self):
        if self.xcor() >= 340 or self.xcor() <= -340:
            self.direction = 'left' if self.direction == 'right' else 'right'
        if self.ycor() >= 340 or self.ycor() <= -340:
            self.direction = 'down' if self.direction == 'up' else 'up'

    # Method to make a step based on the current direction
    def make_step(self):
        self.set_move()
        if self.direction == 'up':
            self.sety(self.ycor() + self.stride)
        elif self.direction == 'down':
            self.sety(self.ycor() - self.stride)
        elif self.direction == 'left':
            self.setx(self.xcor() - self.stride)
        elif self.direction == 'right':
            self.setx(self.xcor() + self.stride)

    # Collision detection method
    def is_collide(self, other):
        return self.distance(other) < 20
    
def obstacles_game():
    # Game setup
    screen = turtle.Screen()
    screen.setup(width=700, height=700)
    screen.tracer(0)  # Disable automatic updates

    # Player, target, and obstacles
    player = Sprite('blue', 'turtle', 0, 0, 25)
    target = Sprite('green', 'circle', random.randint(-340, 340), random.randint(-340, 340))
    obstacles = [Sprite('red', 'square', random.randint(-340, 340), random.randint(-340, 340), stride=15) for _ in range(3)]

    # Writer Specifics
    #writer = turtle.Turtle()
    #writer.penup()
    #writer.color('red')
    #font = ('Arial', 28, 'normal')
    #writer.pendown()

    # Score and game state
    score = 0
    game_over = False
    oldcolor = 'blue'

    # Keyboard bindings
    screen.listen()
    screen.onkey(player.move_left, 'Left')
    screen.onkey(player.move_right, 'Right')
    screen.onkey(player.move_up, 'Up')
    screen.onkey(player.move_down, 'Down')
    # Main game loop
    while not game_over:
        screen.update()
        time.sleep(0.1)

        # Random Player Colors
        randomcolor = random.choice(['darkred', 'springgreen', 'blue', 'gold', 'purple', 'darkturquoise', 'saddlebrown',
            'violet', 'mediumseagreen', 'salmon', 'violet', 'orange', 'indigo', 'powderblue'])

        # Move obstacles
        for obstacle in obstacles:
            obstacle.make_step()

        # Check collision with target
        if player.is_collide(target):
            score += 1
            print('Score:', score)
            for obstacle in obstacles:
                obstacle.hideturtle()
            player.color(randomcolor)
            target.goto(random.randint(-340, 340), random.randint(-340, 340))  # Relocate target
            obstacles = [Sprite('red', 'square', random.randint(-340, 340), random.randint(-340, 340), stride=15) for _ in range(score + 3)]
            

        # Check collision with obstacles
        for obstacle in obstacles:
            if player.is_collide(obstacle):
                print("Congratulations! You caught", score, 'points!')
                game_over = True
                target.hideturtle()
                time.sleep(1)
                turtle.bye()

    screen.mainloop()