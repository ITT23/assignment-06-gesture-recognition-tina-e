# $1 gesture recognizer
import math
import os
import xml.etree.ElementTree as ET
from shapely.geometry import Polygon
from scipy.signal import resample
import numpy as np


class OneDollarRecognizer:

    def __init__(self, gestures):
        self.gestures = gestures
        self.size = 250
        self.num_points_per_polygon = 64
        self.templates = self.read_data()  # dict {'_gesture_': _list of interpolated points as tuples_}

    def read_data(self):
        templates = dict()
        for gest in self.gestures:
            # read xmls
            root = ET.parse(f'dataset/s01/slow/{gest}05.xml').getroot()
            points = []
            for point in root:
                points.append((int(point.attrib['X']), int(point.attrib['Y'])))
            # preprocess points
            points = self.preprocess(points)
            # save as dict
            templates[gest] = points
        return templates

    def preprocess(self, points):
        points = self.resample(points)
        points = self.rotate(points)
        points = self.scale(points)
        points = self.translate(points)
        return points

    def resample(self, points):
        return resample(points, self.num_points_per_polygon)
        #points_nd = np.array(points)
        #distance = np.cumsum(np.r_[0, np.sqrt((np.diff(points_nd, axis=0) ** 2).sum(axis=1))])
        #distance_sampled = np.linspace(0, distance.max(), self.num_points_per_polygon)
        #points_resampled = np.c_[np.interp(distance_sampled, distance, points_nd[:, 0]), np.interp(distance_sampled, distance, points_nd[:, 1])]
        #return points_resampled

    def get_centroid(self, points):
        polygon = Polygon(points)
        centroid = polygon.centroid
        return centroid

    def find_angle(self, points, centroid):
        return math.atan2(centroid.y - points[0, 1], centroid.x - points[0, 0])

    def rotate(self, points):
        centroid = self.get_centroid(points)
        angle = self.find_angle(points, centroid)
        return self.rotate_by(points, angle)

    def rotate_by(self, points, angle):
        centroid = self.get_centroid(points)
        new_points = []
        for point in points:
            new_x = (point[0] - centroid.x) * math.cos(angle) - (point[1] - centroid.y) * math.sin(angle) + centroid.x
            new_y = (point[0] - centroid.x) * math.sin(angle) + (point[1] - centroid.y) * math.cos(angle) + centroid.y
            new_points.append((new_x, new_y))
        return new_points

    def get_boundings(self, points):
        points_nd = np.array(points)
        min_x = np.min(points_nd[:, 0])
        max_x = np.max(points_nd[:, 0])
        min_y = np.min(points_nd[:, 1])
        max_y = np.max(points_nd[:, 1])
        width = max_x - min_x
        height = max_y - min_y
        return width, height

    def scale(self, points):
        bounding_box = self.get_boundings(points)
        new_points = []
        for point in points:
            new_x = point[0] * (self.size / bounding_box[0])
            new_y = point[1] * (self.size / bounding_box[1])
            new_points.append((new_x, new_y))
        return new_points

    def translate(self, points):
        centroid = self.get_centroid(points)
        new_points = []
        for point in points:
            new_x = point[0] - centroid.x
            new_y = point[1] - centroid.y
            new_points.append((new_x, new_y))
        return new_points

    def recognize(self, input_points):
        input_points = self.preprocess(input_points)
        theta = 45 * (math.pi / 180)
        delta_theta = 2 * (math.pi / 180)
        b = math.inf
        recognized_gesture = None
        for gesture, base_points in self.templates.items():
            distance = self.get_distance_at_best_angle(input_points, base_points, -theta, theta, delta_theta)
            if distance < b:
                b = distance
                recognized_gesture = gesture
        score = 1 - b / (0.5 * math.sqrt(self.size ** 2 + self.size ** 2))
        return recognized_gesture, score
    
    def recognize_without_preprocessing(self, input_points):
        theta = 45 * (math.pi / 180)
        delta_theta = 2 * (math.pi / 180)
        b = math.inf
        recognized_gesture = None
        for gesture, base_points in self.templates.items():
            distance = self.get_distance_at_best_angle(input_points, base_points, -theta, theta, delta_theta)
            if distance < b:
                b = distance
                recognized_gesture = gesture
        score = 1 - b / (0.5 * math.sqrt(self.size ** 2 + self.size ** 2))
        return recognized_gesture, score

    def get_distance_at_best_angle(self, input, base, a_theta, b_theta, delta_theta):
        phi = 0.5 * (-1 + math.sqrt(5))
        x1 = phi * a_theta + (1 - phi) * b_theta
        f1 = self.get_distance_at_angle(input, base, x1)
        x2 = (1 - phi) * a_theta + phi * b_theta
        f2 = self.get_distance_at_angle(input, base, x2)
        while abs(b_theta - a_theta) > delta_theta:
            if f1 < f2:
                b_theta = x2
                x2 = x1
                f2 = f1
                x1 = phi * a_theta + (1 - phi) * b_theta
                f1 = self.get_distance_at_angle(input, base, x1)
            else:
                a_theta = x1
                x1 = x2
                f1 = f2
                x2 = (1 - phi) * a_theta + phi * b_theta
                f2 = self.get_distance_at_angle(input, base, x2)
        return min(f1, f2)

    def get_distance_at_angle(self, input, base, theta):
        input = self.rotate_by(input, theta)
        distance = self.get_path_distance(input, base)
        return distance

    def get_path_distance(self, points_a, points_b):
        distance = 0
        for i, point_a in enumerate(points_a):
            distance = distance + math.dist(point_a, points_b[i])
        return distance / len(points_a)
