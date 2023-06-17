# gesture input program for first task

import sys
import pyglet
from recognizer import OneDollarRecognizer

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

window = pyglet.window.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
result_text = pyglet.text.Label("???", x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT-20, anchor_x='center', anchor_y='center')
gestures = ['x', 'caret', 'circle', 'check', 'star']
points = []

recognizer = OneDollarRecognizer(gestures)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        points.clear()
    elif symbol == pyglet.window.key.Q:
        sys.exit(0)


@window.event
def on_mouse_release(x, y, button, modifiers):
    global points
    window.clear()
    if button & pyglet.window.mouse.LEFT:
        points = recognizer.preprocess(points)
        result = recognizer.recognize(points)
        result_text.text = f'{result[0]}: {round(result[1], 2)}'
        points.clear()
        result_text.draw()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if buttons & pyglet.window.mouse.LEFT:
        points.append((int(x), int(WINDOW_HEIGHT-y)))
        rect = pyglet.shapes.Line(x, y, x+dx, y+dy, width=7, color=(156, 0, 75))
        rect.draw()


pyglet.app.run()
