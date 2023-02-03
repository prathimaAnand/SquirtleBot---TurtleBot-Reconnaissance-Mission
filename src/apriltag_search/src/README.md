Code description:
This is a Python script for a ROS node that tracks AprilTag detections, stores the best poses in the map frame and publishes the transforms for those poses. It does this by subscribing to two topics, one for the AprilTag detections and another for cmd_vel (command velocity). The node receives AprilTag detections and transforms the poses into the map frame using a TransformListener. It also receives cmd_vel and uses it to calculate a velocity score. It updates the best pose for a tag if the new detection has a higher velocity score than the previous best. The node also publishes the known tag transforms to the ROS system.

This script is an implementation of an Apriltag tracker node for ROS (Robot Operating System). The node listens to two topics:

/tag_detections: The detections of Apriltags from a camera or a similar device.
/cmd_vel: The velocity of the robot.
The node's purpose is to transform the poses of the Apriltags from the detection frame to the map frame and publish them as the map_tag_<id> transforms. It also calculates a velocity score and keeps track of the best Apriltag poses in the map frame, based on the velocity score.

Additionally, the node also publishes the known tag poses in the map frame as PoseStamped messages on the topic 'mapped_tags'.
