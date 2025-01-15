~/catkin_ws/src/

catkin_create_pkg test_ros_topic std_msgs rospy

cd ..

catkin_make

roscore 

-------------------------
파일을 복사하세요
test_pub_topic.py , test_sub_topic.py 

cd ~/catkin_ws/src/test_ros_topic/src
chmod 777 *

(new 터미널)
# 실행
rosrun test_ros_topic test_pub_topic.py

---------------------------------
 (new 터미널)
# 실행
rosrun test_ros_topic test_sub_topic.py

 (다른 터미널)
rqt_graph

-------------------------------------------

(모두 중지하고 터미널을 모두 끄고 다시 다른 창)

cd ~/catkin_ws/src/test_ros_topic/

mkdir launch

cd launch

# make file "topic_test.launch" and type code.

 topic_test.launch
파일을 복사하세요

source ~/.bashrc

# 실행

roslaunch test_ros_topic topic_test.launch

 (다른 터미널)
 
rqt_graph
