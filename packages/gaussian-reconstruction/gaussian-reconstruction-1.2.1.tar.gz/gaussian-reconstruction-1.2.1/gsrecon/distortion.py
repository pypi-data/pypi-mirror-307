import pycolmap

# def print_available_options(pipeline_options):
#     print("Available mapper_options for IncrementalPipelineOptions:")
#     for attr in dir(pipeline_options):
#         if not attr.startswith("__"):
#             print(f"  - {attr}")

def setup_incremental_pipeline_options():
    options = pycolmap.IncrementalPipelineOptions()
    
    # Set the global bundle adjustment tolerance, which is equivalent to the COLMAP ba_tolerance
    # Decreasing it speeds up bundle adjustment steps.
    options.ba_global_function_tolerance = 0.0000001  

    # Other bundle adjustment options
    options.ba_global_max_num_iterations = 100
    options.ba_global_max_refinements = 5
    options.ba_global_images_ratio = 1.1
    options.ba_global_points_ratio = 1.1
    options.ba_global_images_freq = 500
    options.ba_global_points_freq = 250000

    # Local bundle adjustment options
    options.ba_local_max_num_iterations = 25
    options.ba_local_function_tolerance = 0.0000001
    options.ba_local_max_refinements = 2
    options.ba_local_num_images = 6

    # Refinement options
    options.ba_refine_focal_length = True
    options.ba_refine_principal_point = False
    options.ba_refine_extra_params = True

    # Other relevant options
    options.min_num_matches = 15
    options.max_model_overlap = 20
    options.min_model_size = 10
    options.init_num_trials = 200
    options.extract_colors = True

    return options

def perform_bundle_adjustment(database_path, image_path, output_path):
    print("Starting bundle adjustment and mapping...")

    '''
    incremental_mapping() 
    The following argument types are supported:
        database_path: str, 
        image_path: str, 
        output_path: str, 
        options: pycolmap.IncrementalPipelineOptions = <pycolmap.IncrementalPipelineOptions object at 0x7f738ea48b30>, 
        input_path: str = '', 
        initial_image_pair_callback: Callable[[], None] = None, 
        next_image_callback: Callable[[], None] = None) -> Dict[int, pycolmap.Reconstruction]
    '''
    # Set up the pipeline options
    pipeline_options = setup_incremental_pipeline_options()
    
    # Print available pipeline_options for debugging
    # print_available_options(pipeline_options)

    # Run the incremental mapping
    try:
        reconstructions = pycolmap.incremental_mapping(
            database_path=database_path,
            image_path=image_path,
            output_path=output_path,
            options=pipeline_options
        )
        
        if reconstructions is None:
            print("Reconstruction failed.")
            return False
        
        return reconstructions
    except Exception as e:
        print(f"Bundle adjustment failed: {str(e)}")
        return False
