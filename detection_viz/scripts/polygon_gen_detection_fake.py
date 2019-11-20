#!/usr/bin/env python2

import rospy

from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray

# from jsk_recognition_msgs.msg import PolygonArray
from geometry_msgs.msg import Polygon, PolygonStamped, Point32, Point
from std_msgs.msg import Header

from msgs.msg import *

from rosgraph_msgs.msg import Clock

class Node:

    def __init__(self):
        rospy.init_node("detected_object_polygons")

        self.inputTopic = rospy.get_param("~topic")
        self.c_red = rospy.get_param("~red")
        self.c_green = rospy.get_param("~green")
        self.c_blue = rospy.get_param("~blue")
        self.t_clock = rospy.Time()

        self.polygon_pub = rospy.Publisher(self.inputTopic + "/polygons", MarkerArray, queue_size=100)

        self.clock_sub = rospy.Subscriber("/clock", Clock, self.clock_CB)
        self.detection_sub = rospy.Subscriber(self.inputTopic, DetectedObjectArray, self.detection_callback)


    def run(self):
        rospy.spin()

    def clock_CB(self, msg):
        self.t_clock = msg.clock

    def SquarePolygon(self,header,cPoint,TrackingIndex):
        marker = Marker()
        marker.header.frame_id = "base_link" # header.frame_id
        marker.header.stamp = header.stamp
        marker.ns = self.inputTopic
        marker.action = Marker.ADD
        marker.pose.orientation.w = 1.0

        marker.id = TrackingIndex
        marker.type = Marker.LINE_STRIP
        marker.scale.x = 0.1
        marker.lifetime = rospy.Duration(0.2)
        marker.color.r = self.c_red
        marker.color.g = self.c_green
        marker.color.b = self.c_blue
        marker.color.a = 1.0

        marker.points = []
        if len(cPoint.lowerAreaPoints) > 0:
            for i in range(len(cPoint.lowerAreaPoints)):
                marker.points.append(cPoint.lowerAreaPoints[i])
            marker.points.append(cPoint.lowerAreaPoints[0])

        return marker

    def detection_callback(self, message):
        box_list = MarkerArray()
        TrackingIndex = 1
        for objectMessage in message.objects:
            box_list.markers.append(self.SquarePolygon(message.header, objectMessage.cPoint, TrackingIndex))
            TrackingIndex += 1
        self.polygon_pub.publish(box_list)


if __name__ == "__main__":
    node = Node()
    node.run()