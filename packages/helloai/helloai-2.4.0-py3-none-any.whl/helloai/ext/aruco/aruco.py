# https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/aruco_basics.html
import cv2
import cv2.aruco as aruco
import numpy as np
import os
from helloai.core.image import Image

__all__ = ["ArUco"]


class ArUco:
    def __init__(self):
        self.__img = None
        self.__markers = None

    def detect(self, img, marker_size=6, draw=True):
        self.process(img, marker_size, draw)

    def process_(self, img, marker_size=6, draw=True):
        total_markers = 1000
        frame = img.frame.copy()
        img_gray = img.to_gray().frame

        key = getattr(aruco, f"DICT_{marker_size}X{marker_size}_{total_markers}")
        arucoDict = aruco.Dictionary_get(key)
        arucoParam = aruco.DetectorParameters_create()
        bboxs, ids, rejected = aruco.detectMarkers(
            img_gray, arucoDict, parameters=arucoParam
        )

        if draw:
            frame = aruco.drawDetectedMarkers(frame.copy(), bboxs, ids)

        corners = []
        if bboxs:
            for i in range(len(ids)):
                c = bboxs[i][0]
                corners.append(c.tolist())

            self.__markers = [ids.flatten().tolist(), corners]
            self.__img = Image(frame)
        else:
            self.__markers = [[], []]
            self.__img = img

        return self.__img, self.__markers

    def process(self, img, marker_size=6, draw=True):
        total_markers = 1000
        frame = img.frame.copy()
        img_gray = img.to_gray().frame

        key = getattr(aruco, f"DICT_{marker_size}X{marker_size}_{total_markers}")
        arucoDict = aruco.Dictionary_get(key)
        arucoParam = aruco.DetectorParameters_create()
        bboxs, ids, rejected = aruco.detectMarkers(
            img_gray, arucoDict, parameters=arucoParam
        )

        if draw:
            frame = aruco.drawDetectedMarkers(frame.copy(), bboxs, ids)

        corners = []
        if bboxs:
            for i in range(len(ids)):
                c = bboxs[i][0]
                corners.append(c.tolist())

            markers = dict()
            for id, corner in zip(ids.flatten().tolist(), corners):
                markers[id] = corner

            self.__markers = markers
            self.__img = Image(frame)
        else:
            self.__markers = dict()
            self.__img = img

        return self.__img, self.__markers

    # def augment(self, img, imgAug, drawId=True):
    #     # Loop through all the markers and augment each one
    #     frame = img.frame.copy()
    #     frame_over = imgAug.frame.copy()

    #     if len(self.__markers[0]) != 0:
    #         for bbox, id in zip(self.__markers[0], self.__markers[1]):
    #             frame = self.__draw(bbox, id, frame, frame_over)
    #     return Image(frame)

    def augment(self, bbox, id, img, imgAug, drawId=True):
        """
        :param bbox: the four corner points of the box
        :param id: maker id of the corresponding box used only for display
        :param img: the final image on which to draw
        :param imgAug: the image that will be overlapped on the marker
        :param drawId: flag to display the id of the detected markers
        :return: image with the augment image overlaid
        """

        frame = img.frame.copy()
        frame_over = imgAug.frame.copy()

        tl = bbox[0][0][0], bbox[0][0][1]
        tr = bbox[0][1][0], bbox[0][1][1]
        br = bbox[0][2][0], bbox[0][2][1]
        bl = bbox[0][3][0], bbox[0][3][1]

        # tl = bbox[0][0], bbox[0][1]
        # tr = bbox[1][0], bbox[1][1]
        # br = bbox[2][0], bbox[2][1]
        # bl = bbox[3][0], bbox[3][1]

        h, w, c = frame_over.shape

        pts1 = np.array([tl, tr, br, bl])
        pts2 = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        matrix, _ = cv2.findHomography(pts2, pts1)
        frame_out = cv2.warpPerspective(
            frame_over, matrix, (frame.shape[1], frame.shape[0])
        )
        cv2.fillConvexPoly(frame, pts1.astype(int), (0, 0, 0))
        frame_out = frame + frame_out

        if drawId:
            cv2.putText(
                frame_out, str(id), tl, cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2
            )

        return Image(frame_out)
