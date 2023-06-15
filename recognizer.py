# $1 gesture recognizer

import os
import xml.etree.ElementTree as ET
from dollarpy import Recognizer, Template, Point


class OneDollarRecognizer:

    def __init__(self):
        self.gestures = ['arrow', 'caret', 'circle', 'check', 'rectangle']
        self.recognizer = self.read_data_and_define_recognizer()

    def read_data_and_define_recognizer(self):
        #gesture_data = dict()
        templates = []
        for gest in self.gestures:
            tree = ET.parse(f'dataset/s01/slow/{gest}01.xml')
            root = tree.getroot()
            points = []
            for point in root:
                points.append(Point(int(point.attrib['X']), int(point.attrib['Y'])))

                # x = point.attrib['X']
                # y = point.attrib['Y']
                # print(x, y)
                # gesture_data[gest] = point.attrib
            templates.append(Template(gest, points))
        return Recognizer(templates)

    def get_point(self, x, y):
        return Point(x, y)

    def recognize(self, point_list):
        return self.recognizer.recognize(point_list)