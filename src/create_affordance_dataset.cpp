#include <ros/ros.h>
// PCL specific includes
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/conversions.h>
#include <pcl/point_cloud.h>
#include <pcl_ros/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/ModelCoefficients.h>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/passthrough.h>
#include <pcl/features/normal_3d.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/ModelCoefficients.h>
#include <pcl/filters/voxel_grid.h>

#include "includes/custom_point_types.h"

#include <pcl/kdtree/kdtree.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/segmentation/extract_clusters.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <geometry_msgs/Twist.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/Vector3.h>
#include <sensor_msgs/Joy.h>
#include <nav_msgs/Path.h>
#include <nav_msgs/Odometry.h>
// #include <tf/Vector3.h>
#include <tf/transform_broadcaster.h>
#include <tf/transform_datatypes.h>
#include <std_msgs/String.h>
#include <ros/console.h>
#include <cv_bridge/cv_bridge.h>
#include <ar_track_alvar/AlvarMarker.h>
#include <ar_track_alvar/AlvarMarkers.h>
#include <sstream>
#include <vector>
#include <cmath> 

int number_objects=25; 
int number_actions=10;

void initialize()
{	

	
	
}

void ar_tag_callback(const ar_track_alvar::AlvarMarkers::ConstPtr& marker_msg)
{	

}

int main (int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "query_spatial_relationships");
  ros::NodeHandle nh;

  ros::Subscriber sub = nh.subscribe<sensor_msgs::PointCloud2> ("/points2", 1, point_cloud_callback);

  pub = nh.advertise<sensor_msgs::PointCloud2> ("cloud_in", 1);

  ros::spin ();
}