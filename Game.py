import os
import pyglet
import random


# https://media.harrypotterfanzone.com/first-flying-lesson.jpg -> arrow
# https://win.gg/wp-content/uploads/2023/03/Leviosa.jpg -> pigtail
# https://static.wikia.nocookie.net/harrypotter/images/c/ce/MargeBalloon.jpg -> circle


class Game:
    def __init__(self, gestures, win_w, win_h):
        self.num_spells = len(gestures)
        self.gestures = gestures
        self.images = self.read_images()
        self.current_task = random.choice(self.gestures)
        self.score = self.game_state = 0
        self.tries = 1
        self.again = False
        self.rects = []
        self.visualization_sprite = pyglet.sprite.Sprite(img=pyglet.resource.image(os.path.normpath(f'assets/task3/{self.current_task}-resized.png')))
        self.drawing = pyglet.shapes.Line(0, 0, 0, 0, width=10)
        self.score_label = pyglet.text.Label(text='Score: 0', x=win_w - 50, y=win_h - 20, anchor_x='center', font_name='Times New Roman', font_size=16)
        self.status_label = pyglet.text.Label(text='--- WELCOME WIZARD! ---', x=win_w/2, y=win_h/2, anchor_x='center', font_name='Times New Roman', font_size=20)
        self.status_outcome_label = pyglet.text.Label(text='Press SPACE to solemnly swear that you are up to no good.', x=win_w/2, y=win_h/2.5, anchor_x='center', font_name='Times New Roman', font_size=18)

    def read_images(self):
        images = dict()
        for gesture in self.gestures:
            images[gesture] = pyglet.resource.image(os.path.normpath(f'assets/task3/{gesture}-resized.png'))
        return images

    def draw(self):
        if self.game_state == 1:
            self.visualization_sprite.draw()
        else:
            self.status_outcome_label.draw()
        self.score_label.draw()
        self.status_label.draw()
        for rect in self.rects:
            rect.draw()

    def on_end(self):
        self.game_state = 2
        self.status_label.text = "You've learned all spells."
        if self.score < self.num_spells * 30:
            self.status_outcome_label.text = "Your skills are ok. Take your chance to improve next semester!"
        elif self.num_spells * 30 < self.score < self.num_spells * 60:
            self.status_outcome_label.text = "You are a good wizard! Well done!"
        elif self.score > self.num_spells * 60:
            self.status_outcome_label.text = "You are an excellent wizard! Awesome!"

    def on_space(self):
        # no more actions when game ended
        if self.game_state == 2:
            return

        self.status_label.text = ' '
        self.status_outcome_label.text = ' '
        # just start the game
        if self.game_state == 0:
            self.game_state = 1
        # game is running
        else:
            self.game_state = 1
            if not self.again:
                self.gestures.remove(self.current_task)
                if len(self.gestures) > 0:
                    self.current_task = random.choice(self.gestures)
                    self.visualization_sprite.image = self.images[self.current_task]
                else:
                    self.on_end()

    def check_recognized_gestures(self, recognized_gesture, score):
        self.rects = []
        self.game_state = 3
        if recognized_gesture == self.current_task:
            self.status_label.text = '--- CORRECT ---'
            self.status_outcome_label.text = 'Press SPACE to learn the next spell.'
            self.score += int((score * 100) / self.tries)
            self.score_label.text = f'Score: {self.score}'
            self.again = False
            self.tries = 1
        else:
            self.status_label.text = '--- NOT CORRECT ---'
            self.status_outcome_label.text = 'Press SPACE to try again.'
            self.tries += 1
            self.again = True


