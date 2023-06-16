# application for task 3

import sys
import pyglet
from recognizer import OneDollarRecognizer
from Game import Game

WINDOW_WIDTH = 750
WINDOW_HEIGHT = 500
GESTURES = ['circle', 'arrow', 'pigtail']

recognizer = OneDollarRecognizer(GESTURES)
points = []

window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
game = Game(GESTURES, WINDOW_WIDTH, WINDOW_HEIGHT)


@window.event
def on_draw():
    window.clear()
    game.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        points.clear()
        game.on_space()
    elif symbol == pyglet.window.key.Q:
        sys.exit(0)


@window.event
def on_mouse_release(x, y, button, modifiers):
    if button & pyglet.window.mouse.LEFT:
        if len(points) > 0:
            result = recognizer.recognize(points)
            game.check_recognized_gestures(result[0], result[1])
            points.clear()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT:
        points.append(recognizer.get_point(int(x), int(WINDOW_HEIGHT-y)))
        rect = pyglet.shapes.Line(x, y, x+dx, y+dy, width=3, color=(156, 0, 75))
        game.rects.append(rect)


pyglet.app.run()

