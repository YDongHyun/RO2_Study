import rclpy
import cv2
import matplotlib.pyplot as plt
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class PoseNetPublisher(Node):
    def __init__(self):
        super().__init__("pose_net_pub")
        self.publisher = self.create_publisher(Image,'posenet',10)   
        self.img_data = cv2.imread('posenet_pkg/posenet_pkg/test/test.png')
        self.cv_bridge = CvBridge()

    def publish_callback(self):
        img=Image()
        img=self.cv_bridge.cv2_to_imgmsg(self.img_data)
        self.publisher.publish(img)
        self.get_logger().info("image published")

def main(args=None):
    rclpy.init(args=args)
    node = PoseNetPublisher()
    node.publish_callback()
    node.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()
