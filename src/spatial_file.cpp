//First define a list of objects. 
//Define the model to tag relative pose between two objects in a labelled image with all objects. 
//Run this model over the entire dataset, save the matrices generated by each. 
//Compute the relationship for the final matrix as the argmax over Values of (s_ij) of the sum of norm of ||s(ij)-p(i,j)||
//Write the final matrix to a file.

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
// #include <ar_track_alvar/AlvarMarker.h>
// #include <ar_track_alvar/AlvarMarkers.h>
#include <sstream>
#include <vector>
#include <cmath> 

const int number_objects = 130; 
const int number_dimensions = 2; 
// const int number_spatial_states = number_dimensions*2 + 2; 

// double spatial_states[number_spatial_states][2]; 
// double model_result[2];
// double object_centroids[number_objects][3];

typedef pcl::PointXYZRGBCamSL PointT;

double same_threshold = 0.1; 
double no_relation_threshold = 10; 
const int number_training_scenes = 10; 

geometry_msgs::Vector3 object_centroids[number_objects];
geometry_msgs::PoseStamped robot_pose;

double sample_spatial_relation[number_training_scenes][number_objects][number_objects];
double spatial_relation[number_objects][number_objects];

// pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
pcl::PointCloud<PointT>::Ptr cloud (new pcl::PointCloud<PointT>);

// pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);

void compute_sample_relationships();
void compute_relationship_matrix();

class objects
	{	public: 
			int label_number, number_points; 
			tf::Vector3 centroid; 
			geometry_msgs::Vector3 geo_centroid;

			objects()
				{	label_number=-1;
					number_points=0;  
					geo_centroid.x = 0; 
					geo_centroid.y = 0; 
					geo_centroid.z = 0; 
				}


			friend std::ostream& operator<<(std::ostream& os, const objects& obj_op_ptr)
				{			
					// write out individual members of s with an end of line between each one					
					os<<obj_op_ptr.label_number<<std::endl; 
					os<<obj_op_ptr.number_points<<std::endl;
					os<<obj_op_ptr.geo_centroid;
					return os;
				} 

			// Extraction operator
			// friend std::istream& operator>>(std::istream& is, const& obj_ip_ptr)
			// 	{
			// 		// read in individual members of scene_ip_ptr					
			// 		is>>obj_ip_ptr.label_number; 
			// 		is>>obj_ip_ptr.number_points;
			// 		is>>obj_ip_ptr.geo_centroid;
			// 		return is;
			// 	}
	};

class scenes
	{	public: 
			std::vector<objects> scene_obj_vector;
			int scene_num_obj;
			double scene_spatial_rel[number_objects][number_objects];
			
			scenes()
				{	objects dummy_obj; 
	
					scene_obj_vector.push_back(dummy_obj);
					scene_num_obj = 0; 
				}


	};

std::vector<scenes> scene_vector; 

int main(int argc, char** argv)
	{	
		objects temp_obj; 
		
		// scene_vector.push_back(temp_scene);
		int file_index;
		int flag; 
		pcl::PCDReader reader;
		std::cout<<"Value of argc: "<<argc<<std::endl;
		for (int file_ind=1; file_ind<argc; file_ind++)
			{	
				std::cout<<"File number: "<<file_ind-1<<std::endl;
				// scene_vector.push_back(temp_scene);
				reader.read (argv[file_ind], *cloud);
				file_index = file_ind - 1; 
				scenes temp_scene; 
				for (size_t pt_index=0; pt_index<cloud->size(); pt_index++)			
					{	
						// std::cout<<"Started loop 2. "<<"Point number "<<pt_index<<std::endl;
						flag=0; 
						// for (int vec_index=0; vec_index<sizeof(temp_scene.scene_obj_vector); vec_index++)
						for (int vec_index=0; vec_index<temp_scene.scene_obj_vector.size(); vec_index++)
							{	
								//std::cout<<"Started loop 3."<<vec_index<<" th iteration."<<std::endl;
								// if (cloud->points[pt_index].label > number_objects)
									// continue;									
								if (cloud->points[pt_index].label == temp_scene.scene_obj_vector[vec_index].label_number)
								// if (cloud->points[pt_index].label == scene_vector[file_index].scene_obj_vector[vec_index].label_number)
									{										
										temp_scene.scene_obj_vector[vec_index].geo_centroid.x += cloud->points[pt_index].x; 
										temp_scene.scene_obj_vector[vec_index].geo_centroid.y += cloud->points[pt_index].y;
										temp_scene.scene_obj_vector[vec_index].geo_centroid.z += cloud->points[pt_index].z; 

										temp_scene.scene_obj_vector[vec_index].number_points++; 
										int np = temp_scene.scene_obj_vector[vec_index].number_points; 

										temp_scene.scene_obj_vector[vec_index].geo_centroid.x = (temp_scene.scene_obj_vector[vec_index].geo_centroid.x)/np;
										temp_scene.scene_obj_vector[vec_index].geo_centroid.y = (temp_scene.scene_obj_vector[vec_index].geo_centroid.y)/np;
										temp_scene.scene_obj_vector[vec_index].geo_centroid.z = (temp_scene.scene_obj_vector[vec_index].geo_centroid.z)/np;
							
										flag=1;
										continue; 
									}
								// else 
									// {	
										// flag=0; 
										// continue; 									
									// }
							}	
						if (flag==0)
							{	
								temp_obj.label_number = cloud->points[pt_index].label;
								temp_obj.number_points = 1; 
								temp_obj.geo_centroid.x = cloud->points[pt_index].x; 
								temp_obj.geo_centroid.y = cloud->points[pt_index].y; 
								temp_obj.geo_centroid.z = cloud->points[pt_index].z; 
								// temp_scene.number_objects++;
								temp_scene.scene_num_obj++;
								temp_scene.scene_obj_vector.push_back(temp_obj);
							}
					}

				// int i=vec_index;
				char buffer[32];
				snprintf(buffer, sizeof(char) * 32, "file%i.txt", file_index);						
				std::ofstream ofs(buffer);
				for (int vec_index=0; vec_index<temp_scene.scene_obj_vector.size(); vec_index++)
					{	
						ofs<<temp_scene.scene_obj_vector[vec_index]<<std::endl; // store the object to file
						// std::cout<<temp_scene.scene_obj_vector.size()<<std::endl;										
					}
				ofs.close();
				// std::cout<<temp_scene.scene_obj_vector.size()<<std::endl;
			}
		
		std::cout<<"Break point 1."<<std::endl;


		// compute_sample_relationships();
		// std::cout<<"Break point 2."<<std::endl;
		//compute_relationship_matrix();
		// std::cout<<"Break point 3."<<std::endl;

		// for(int i=0; i<number_objects; i++)
		// 	{	for(int j=0; j<number_objects; j++)
		// 			std::cout<<spatial_relation[i][j]<<" ";
		// 		std::cout<<std::endl;
		// 	}

		// for(int i=0; i<number_objects; i++)
			// {	for(int j=0; j<number_objects; j++)
					// std::cout<<scene_vector[0].scene_spatial_rel[i][j]<<" ";
				// std::cout<<std::endl;
			// }
		return 0; 
	}

void compute_sample_relationships()
	{	// Load a point cloud file, run the detector, store the object centroids, 
		//Then call spatial_model over each pair of objects
		//Store / save the results into whatever 
		
		std::cout<<"Break point 3.5, "<<scene_vector.size()<<std::endl;
		for (int scene_ind=0; scene_ind<scene_vector.size(); scene_ind++)	
			{	
				// std::cout<<"Break point 4 at loop number: "<<scene_ind<<std::endl;
				for (int i=0; i<number_objects; i++)
					{	
						// std::cout<<"Break point 5 at loop number: "<<i<<std::endl;
						for (int j=0; j<number_objects; j++)
							scene_vector[scene_ind].scene_spatial_rel[i][j] = -1;
					}
			}
			
		for (int scene_ind=0; scene_ind<scene_vector.size(); scene_ind++)
			{	
				for (int obj_ind_i=0; obj_ind_i<scene_vector[scene_ind].scene_obj_vector.size(); obj_ind_i++)
					{	
						for (int obj_ind_j=0; obj_ind_j<scene_vector[scene_ind].scene_obj_vector.size(); obj_ind_j++)
							{	
								tf::Vector3 rel_trans(scene_vector[scene_ind].scene_obj_vector[obj_ind_i].geo_centroid.x - scene_vector[scene_ind].scene_obj_vector[obj_ind_j].geo_centroid.x,
													  scene_vector[scene_ind].scene_obj_vector[obj_ind_i].geo_centroid.y - scene_vector[scene_ind].scene_obj_vector[obj_ind_j].geo_centroid.y,
   												  	scene_vector[scene_ind].scene_obj_vector[obj_ind_i].geo_centroid.z - scene_vector[scene_ind].scene_obj_vector[obj_ind_j].geo_centroid.z);					
								if (rel_trans.length()<no_relation_threshold)
									scene_vector[scene_ind].scene_spatial_rel[obj_ind_i][obj_ind_j] = rel_trans.length();
								// else 
									// scene_vector[scene_ind].scene_spatial_rel[obj_ind_i][obj_ind_j] = -1; 
							}
					}
			}
		
	}


void compute_relationship_matrix()
	{	
		int num_training_scenes = scene_vector.size();
		int num_corr_objs;
		int num_obs=10; 
		float value=0;
		for (int i=0; i<number_objects; i++)
			{	for (int j=0; j<number_objects; j++)
					{	//std::cout<<"Break point 7: "<<scene_vector.size()<<std::endl;
						spatial_relation[i][j]=-1;
					}
			}
		for (int i=0; i<number_objects; i++)
			{	for (int j=0; j<number_objects; j++)
					{	//std::cout<<"Break point 7.1: "<<scene_vector.size()<<std::endl;
						num_corr_objs=0;
						value=0;
						if (j<i)
							continue; 										
						for (int k=0; k<scene_vector.size(); k++)
							{	//std::cout<<"Break point 7.2: "<<scene_vector.size()<<std::endl;
								if (scene_vector[k].scene_spatial_rel[i][j]>0)
									{	value += scene_vector[k].scene_spatial_rel[i][j];
										num_corr_objs++;
									}
							}
						// spatial_relation[i][j] = value/num_training_scenes;
						// spatial_relation[j][i] = value/num_training_scenes;

						if (value!=0)
							{	spatial_relation[i][j] = value/num_corr_objs;
								spatial_relation[j][i] = value/num_corr_objs;
							}
					}
			}		
	}



