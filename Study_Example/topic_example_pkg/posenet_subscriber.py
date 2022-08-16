import sys
sys.path.append("/home/ydh/posenet_pkg/posenet_pkg/posenet_pkg")
import rclpy
from rclpy.node import Node 
from sensor_msgs.msg import Image as Msg_img
from PIL import Image 
import cv2
from cv_bridge import CvBridge
import torch
from torch.utils.data import TensorDataset, DataLoader
from data_loader import get_loader
from solver import Solver
from torch.backends import cudnn 

class PoseNetSubscriber(Node):
    def __init__(self):
        super().__init__("pose_net_sub")
        self.subscriber = self.create_subscription(Msg_img,'posenet',self.sub_callback,10)
        self.cv_bridge = CvBridge()
        self.subscriber

    def sub_callback(self,img):
        msg=self.cv_bridge.imgmsg_to_cv2(img)
        pil_image=Image.fromarray(msg)
        cudnn.benchmark = True
        data_loader = get_loader(model='Resnet', image_path=pil_image ,mode='test', batch_size=1)
        sol=Solver(data_loader)
        a,b=sol.test()
        self.get_logger().info("image subscribed")
        
        print(a)

      

def main(args=None):
    rclpy.init(args=args)
    node= PoseNetSubscriber()
    try:
        node.get_logger().info("Waitting msg....")
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger.info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__=="__main__":
    main()
