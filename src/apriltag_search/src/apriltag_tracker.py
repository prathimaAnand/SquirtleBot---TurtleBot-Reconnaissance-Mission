#!/usr/bin/env python3

import rospy
from tf import TransformListener, TransformBroadcaster
from geometry_msgs.msg import Twist, PoseStamped, PoseWithCovariance, TwistWithCovariance
from apriltag_ros.msg import AprilTagDetection, AprilTagDetectionArray

class ApriltagTracker(object):
    def __init__(self):
        rospy.init_node('apriltag_tracker', log_level=rospy.DEBUG)
        rospy.loginfo("Starting apriltag_tracker node...")

        # Read params
        self.detection_topic = rospy.get_param('~detection_topic', '/tag_detections')
        self.cmd_vel_topic = rospy.get_param('~cmd_vel_topic', '/cmd_vel')
        self.angular_coefficient = rospy.get_param('~angular_coefficient', 2)
        self.map_frame = rospy.get_param('~map_frame', '/map')
        self.detection_frame = rospy.get_param('~detection_frame', '/camera')

        self.tf_listener_ = TransformListener()

        # subscribe to apriltag detections
        rospy.Subscriber(self.detection_topic, AprilTagDetectionArray, self.on_tag_detection)
        # subscribe to cmd_vel
        rospy.Subscriber(self.cmd_vel_topic, Twist, self.on_cmd_vel)

        # Publish tag poses in map
        self.publisher = rospy.Publisher('mapped_tags', PoseStamped, queue_size=10)

        self.velocity_score = 0

        # Store the best tag poses in map (vel_score, map_pose)
        self.best_tag_poses = dict()

    def on_tag_detection(self, msg: AprilTagDetectionArray):
        velocity_score = self.velocity_score

        for detection in msg.detections:
            rospy.logdebug("Detected tag: {}".format(detection.id))
            map_pose = self.transform_detection_pose(detection)

            try:
                # If the stored pose for this tag has a worse velocity score than current score
                if self.best_tag_poses[detection.id][0] >= velocity_score:
                    # Update the best pose and velocity score
                    self.best_tag_poses[detection.id] = (velocity_score, map_pose)

            except KeyError:
                # If we haven't seen this tag yet, store this pose
                self.best_tag_poses[detection.id] = (velocity_score, map_pose)

    def on_cmd_vel(self, msg: Twist):
        velocity_score = msg.linear.x**2 + msg.linear.y**2 + msg.linear.z**2 + \
                         self.angular_coefficient*(msg.angular.x**2 + msg.angular.y**2 + msg.angular.z**2)

        self.velocity_score = velocity_score
        rospy.logdebug("Velocity Score: {}".format(velocity_score))

    def transform_detection_pose(self, detection: AprilTagDetection):
        ps = PoseStamped()
        ps.header = detection.pose.header
        ps.pose = detection.pose.pose.pose

        p_in_map = self.tf_listener_.transformPose(self.map_frame, ps)

        # rospy.logdebug('Camera Pose:')
        # rospy.logdebug(detection.pose)
        #
        # rospy.logdebug('Map pose:')
        # rospy.logdebug(p_in_map)
        # rospy.logdebug('####################################')

        return p_in_map

    def publish_known_tag_transforms(self):
        for id, best_tag_pose in self.best_tag_poses.items():
            _, tag_pose = best_tag_pose

            br = TransformBroadcaster()
            br.sendTransform((tag_pose.pose.position.x,
                              tag_pose.pose.position.y,
                              tag_pose.pose.position.z),
                             (tag_pose.pose.orientation.x,
                              tag_pose.pose.orientation.y,
                              tag_pose.pose.orientation.z,

                              tag_pose.pose.orientation.w),
                            rospy.Time.now(),
                            "map_tag_{}".format(id[0]),
                            self.map_frame)

    def print_mapped_tags(self):
        msg = ""
        msg += "-----------------------------------\n"

        for id, best_tag_pose in self.best_tag_poses.items():
            _, tag_pose = best_tag_pose

            msg += "Tag: {}\nPose:{}\n".format(id[0], tag_pose.pose)
        msg += "-----------------------------------\n"

        rospy.loginfo(msg)

    def spin(self):
        # Set rate
        rate = rospy.Rate(1)

        while not rospy.is_shutdown():
            try:
                self.publish_known_tag_transforms()
                self.print_mapped_tags()

            except Exception as e:
                rospy.logerr(e)

            rate.sleep()

if __name__ == '__main__':
    try:
        node = ApriltagTracker()
        rospy.loginfo("apriltag_tracker node started.")

        node.spin()

        rospy.loginfo("apriltag_tracker node shutdown.")

    except rospy.ROSInterruptException:
        node.close()
        rospy.loginfo("apriltag_tracker node (interrupt).")
