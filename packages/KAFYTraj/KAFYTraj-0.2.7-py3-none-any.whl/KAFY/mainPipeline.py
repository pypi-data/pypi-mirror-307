"""Pipeline Class Definition"""

# On TOP of all of this, the user shall define FLOW.py which should
# give him the desired trajectory operation output
from os import path as os_path
from os import makedirs as os_makedirs
from pandas import DataFrame as pd_DataFrame

# os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from .utilFunctions import tokenize_trajectory, detokenize_trajectory,add_entry_to_csv
from .constraintsClass import SpatialConstraints
from .partioningClass import PartitioningModule
from pathlib import Path as pathlib_Path
from datetime import datetime as datetime_datetime

import logging
from  warnings import filterwarnings,warn

filterwarnings(
    "ignore", category=FutureWarning, module="transformers.deepspeed"
)

from pandas import read_csv
from typing import Tuple, List
from KAFY.modelsLoader import *
from json import dump as json_dump

# Configure the logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TrajectoryPipeline:
    """
    A configurable pipeline that orchestrates various processes such as
    tokenization, spatial constraints,
    trajectory plugins, and de-tokenization. This class is designed to be
    flexible and extensible, allowing
    the user to customize and modify different components according to their needs.
    """

    def __init__(
        self,
        mode: str = "",
        operation_type: str = "",
        use_tokenization: bool = False,
        use_spatial_constraints: bool = True,
        use_detokenization: bool = True,
        modify_transformers_plugin: bool = False,
        modify_spatial_constraints: bool = False,
        use_predefined_spatial_constraints: bool = False,
        project_path: str = "/KafyProject/",
    ):
        """
        Initializes the pipeline with needed params.

        Args:
            mode (str): Either 'addingModel','addingPretrainingData','addingFinetuningData', 'finetuning', or 'testing'.
            operation_type (str): User sets the operationt type
            use_tokenization (bool): Whether to use tokenization.
            use_spatial_constraints (bool): Whether to use spatial constraints.
            use_trajectory_plugin (bool): Whether to use trajectory plugin.
            use_detokenization (bool): Whether to use de-tokenization.
            modify_transformers_plugin (bool): Whether to modify transformers plugin.
            modify_trajectory_plugin (bool): Whether to modify trajectory plugin.
            modify_spatial_constraints (bool): Whether to modify spatial constraints.
            use_predefined_spatial_constraints (bool): Whether to user predefined
                                                        spatial constraints or not.
            project_path (str): where to save modelsRepo and trajectoryStore
        """
        # Case Scenarios 
        self.mode_options = ['startNewProject','addPretrainingData','addPretrainingArchitecture','addFinetuningData',"addFinetuningArchitecture", 'testing']
        # Those are the only required arguments
        if not mode:
            raise TypeError("Missing required argument: 'mode'")
        if mode not in self.mode_options:
            raise TypeError("wrong mode initialization. \n'mode' should be one of the following ",self.mode_options)
        if not project_path:
            raise TypeError("Missing required argument: 'project_path'")
        self.mode,self.use_tokenization,self.use_spatial_constraints = mode,use_tokenization,use_spatial_constraints
        self.use_detokenization,self.modify_transformers_plugin = use_detokenization,modify_transformers_plugin
        self.modify_spatial_constraints,self.use_predefined_spatial_constraints,self.operation_type = modify_spatial_constraints,use_predefined_spatial_constraints,operation_type
        # Create ModelsRepo and trajectoryStore at specified projectPath if they don't exist already
        self.project_path = project_path
        self.models_repository_path = os_path.join(self.project_path, "modelsRepo")
        self.trajecotry_store_path = os_path.join(self.project_path, "trajectoryStore")
        self.transformers_plugin_path = os_path.join(self.project_path, "transformersPlugin")
        
        
        if self.mode == "startNewProject":
            self.start_new_project()
        # elif self.mode=="addPretrainingData":
        #     self.add_training_data()
        # elif self.mode=="addPretrainModel":
        #     self.pretrain_model_on_all_datasets()
        # Initialize any other attributes or perform setup based on the parameters
        (
            self.model,
            self.tokenizer,
            self.spatial_constraints,
            self.trajectory_plugin,
            self.tokenized_trajectories,
            self.input_attributes,
            self.trajectories_list,
            self.spatial_constraints,
        ) = (None,) * 8
        (
            self.resolution_set_by_user,
            self.user_did_define_spatial_constraints,
            self.trajectories_got_tokenized,
            self.data_saved_to_trajectory_store,
        ) = (False,) * 4
        self.resolution = 10
        self.data_path_trajectory_store, self.metadata_path_trajectory_store = "", ""
        logging.info("Pipeline Initialized with mode: %s", self.mode)

    def is_valid_input(self,H, L):
        if not (3 <= H <= 20):
            print("H should be between 3 and 20.")
            return False
        if not (3 <= L <= 20):
            print("L should be between 3 and 20.")
            return False
        if L >= H:
            print("L should be less than H.")
            return False
        return True

    def get_pyramid_values(self):
        pyramid_data = { "H": 5,  "L": 3,  "build_pyramid_from_scratch": True}
        # Ask the user if they want to use default values or enter custom values
        use_default = input("Do you want to use default values for Pyramid parameters (H and L)? (yes/no): ").strip().lower()
        if use_default == "no":
            try:
                # Prompt the user for input for H and L
                H = int(input("Enter the value for H (height of the pyramid, between 5 and 20): "))
                L = int(input("Enter the value for L (levels of the pyramid, between 3 and 18, must be less than H): "))

                # Validate user input
                if self.is_valid_input(H, L):
                    # Update the dictionary with the user's input if valid
                    pyramid_data["H"] = H
                    pyramid_data["L"] = L
                else:
                    logging.info("Invalid input, reverting to default values.")
            
            except ValueError:
                print("Invalid input. Please enter valid integers. Reverting to default values.")

        else:
            print("Using default pyramid data:", pyramid_data)
        return pyramid_data
    
    def start_new_project(self):
        logging.info("Hidden Case Scenario #1: Starting a new project")

        try:
            project_dir_name = os_path.basename(os_path.normpath(self.project_path))
            # Check if the project path is the default and issue a warning
            if project_dir_name == "KafyProjectDirectory":
                warn(
                    "No alternative project path provided. Will default to {self.project_path} directory",
                    UserWarning,
                )

            # Create the project directories if they do not exist
            if not os_path.exists(self.project_path):
                logging.info(
                    "First time creating projectDirectory, modelsRepo, trajectoryStore, transformersPlugin."
                )
                # os_makedirs(self.project_path)
                # os_makedirs(self.models_repository_path)
                os_makedirs(os_path.join(self.models_repository_path,"pretrainedModels"))
                os_makedirs(os_path.join(self.models_repository_path,"finetunedModels"))
                #These should be the architectures .py files the user will provide to pretrain and finetune
                os_makedirs(os_path.join(self.transformers_plugin_path,"pretrainingArchitectures"))
                os_makedirs(os_path.join(self.transformers_plugin_path,"finetuningArchitectures"))
                # os_makedirs(self.trajecotry_store_path)
                os_makedirs(os_path.join(self.trajecotry_store_path,"pretrainingDatasets"))
                os_makedirs(os_path.join(self.trajecotry_store_path,"finetuningDatasets"))
                # os_makedirs(self.transformers_plugin_path)
                logging.info("Created necessary files in modelsRepo...")
                pyramid_data = self.get_pyramid_values()
                # Define the file path for pyramidConfigs.json
                pyramid_config_file = os_path.join(
                    self.models_repository_path, "pyramidConfigs.json"
                )
                # Write the JSON data to the file
                with open(pyramid_config_file, "w") as json_file:
                    json_dump(pyramid_data, json_file, indent=4)

                logging.info(
                    "Created the pyramid configurations for the first time."
                )
                # This by default will create the two pyramids for pretraining and finetuning
                module = PartitioningModule(
                        models_repo_path=self.models_repository_path,
                        operation=self.mode,
                    )
                # Define the paths using pathlib.Path
                # Define column headers
                PreTrainedColumns = ["DatasetPath", "Level", "Cell", "NumOfTokens", "PretrainedModels"]
                FinetunedColumns = ["FinetuningTask","DatasetPath", "Level", "Cell", "NumOfTokens", "FinetunedModels"]
                self.storedDatasetsTablePretrained = pathlib_Path(self.trajecotry_store_path) / "pretrainingDatasets" / 'storedDatasetsMetadata.csv'
                self.storedDatasetsTableFinetuned = pathlib_Path(self.trajecotry_store_path) / "finetuningDatasets" / 'storedDatasetsMetadata.csv'

                
                if not self.storedDatasetsTablePretrained.exists():
                    # Create an empty DataFrame with specified columns
                    self.storedDatasetsTablePretrained.parent.mkdir(parents=True, exist_ok=True)
                    df = pd_DataFrame(columns=PreTrainedColumns)
                    df.to_csv(self.storedDatasetsTablePretrained, index=False)
                if not self.storedDatasetsTableFinetuned.exists():
                    # Create an empty DataFrame with specified columns
                    self.storedDatasetsTableFinetuned.parent.mkdir(parents=True, exist_ok=True)
                    df = pd_DataFrame(columns=FinetunedColumns)
                    df.to_csv(self.storedDatasetsTableFinetuned, index=False)
                logging.info(
                    "Created the storedDatasetsMetadata.csv file(s) for the first time."
                )
            else:
                logging.info(
                    f"Project path '{self.project_path}' already exists.   No directories were created."
                )
                

        except OSError as e:
            raise ValueError(f"Error creating project directories: {e}")

    def set_tokenization_resolution(self, resolution: int = 10):
        """
        Sets the resolution to be used if tokenization is enabled.

        Args:
            resolution (int):resolution for the tokenization.

        Returns:
            None
        """
        if not self.use_tokenization:
            raise ValueError("Tokenization is not used. No need to set resolution.")
        self.resolution = resolution
        self.resolution_set_by_user = True
 
    def get_trajectories_from_csv(
        self, column_name,file_path: str = ""
    ) -> List[List[Tuple[float, float]]]:
        """
        Reads a CSV file containing trajectories and returns the trajectories as a list of lists of tuples.

        Each trajectory is represented as a list of (latitude, longitude) tuples.

        Args:
            file_path (str): A CSV file path containing the trajectories.

        Returns:
            List[List[Tuple[float, float]]]: List of trajectories, where each trajectory is a list of (latitude, longitude) tuples.
        """
        # Read the CSV file into a DataFrame
        df = read_csv(file_path)

        # Initialize a list to hold the trajectories
        trajectories = []

        # Process each row in the DataFrame
        for _, row in df.iterrows():
            # Extract the trajectory string
            trajectory_str = row[column_name]

            # Split the trajectory string into individual points
            points_str = trajectory_str.split(",")

            # Convert the points to (latitude, longitude) tuples
            trajectory = [
                (round(float(point.split()[0]), 6), round(float(point.split()[1]), 6))
                for point in points_str
            ]

            # Append the trajectory to the list
            trajectories.append(trajectory)

        return trajectories

    def __tokenization_module(
        self, trajectories: list[list[tuple[float, float]]]
    ) -> list[list[str]]:
        """
        Tokenizes a list of trajectories.

        Args:
            trajectories (list of list of tuple[float, float]]): A list of trajectories,
                                                    where each trajectory is a list of
            (latitude, longitude) tuples.

        Returns:
            list of list of str: A list of tokenized trajectories, where
                                    each trajectory is a list of tokens.
        """

        if not self.resolution_set_by_user:
            info = "Tokenization Resolution Set By Default to: " + self.resolution
            logging.info(info)
        tokenized_trajectories = [
            tokenize_trajectory(trajectory, self.resolution)
            for trajectory in trajectories
        ]
        return tokenized_trajectories

    def __save_trajectories_to_store(self, tokenized_trajectories, operation,cell):
        if tokenized_trajectories is not None:
            self.data_saved_to_trajectory_store = False
            # Generate a random dataset name
             # Convert each trajectory to a single string where tokens are joined by spaces
            data = [" ".join(trajectory) for trajectory in tokenized_trajectories]
            l = cell["height"]
            index = cell["index"]
            # Create a DataFrame with a single column
            df = pd_DataFrame(data, columns=["tokenizedTrajectory"])
            dataset_filename = os_path.join(
                self.trajecotry_store_path, operation,f"{l}_{index}", f"dataset.csv"
            )
            # Ensure the directory exists
            os_makedirs(os_path.dirname(dataset_filename), exist_ok=True)
            df.to_csv(dataset_filename, index=False)
            vocab_file_path = os_path.join(
                self.trajecotry_store_path, operation,f"{l}_{index}", f"vocab.txt"
            )
            
            # generate the vocab file which will be used by the tokenizer
            unique_tokens = set(token for sublist in tokenized_trajectories for token in sublist)
            # Write the unique tokens to the vocabulary file
            # TODO Those tokens are for BERT only, need to find a more general way
            with open(vocab_file_path, "w") as vocab_file:
                vocab_file.write(f"[UNK]\n")
                vocab_file.write(f"[PAD]\n")
                vocab_file.write(f"[MASK]\n")
                for token in sorted(unique_tokens):  # Sort for consistency
                    vocab_file.write(f"{token}\n")

            # Create metadata
            num_tokens = sum(len(traj) for traj in tokenized_trajectories)
            metadata = {
                "total_number_of_trajectories": len(tokenized_trajectories),
                "total_number_of_tokens": num_tokens,
                "date_of_data_storage": datetime_datetime.now().strftime(
                    "%Y-%m-%d %H:%M"
                ),
                "type_of_data": operation,
                "tokenized": self.trajectories_got_tokenized,
            }

            # Save metadata to a .txt file
            metadata_filename = os_path.join(
                self.trajecotry_store_path,
                operation,
                f"{l}_{index}",
                f"metadata.json",
            )
            # Ensure the directory exists
            os_makedirs(os_path.dirname(metadata_filename), exist_ok=True)
            with open(metadata_filename, "w", encoding="utf-8") as f:
                json_dump(metadata, f, ensure_ascii=False, indent=4)

            logging.info("Trajectories saved to %s with metadata and vocab file.", dataset_filename)
            self.data_saved_to_trajectory_store = True
            return dataset_filename, metadata_filename, num_tokens
 
    def add_pretraining_data(self,trajectories_list:List[List[Tuple[float, float]]]):
        """
        Tokenizes training data if needed and adds it to trajectoryStore/pretraining/
        """
        logging.info("Hidden Case Scenario #2: Adding a pretraining dataset")

        #This should load the pretrainingPyramid to the partitioning_module
        partitioning_module = PartitioningModule(
                        models_repo_path=self.models_repository_path,
                        operation=self.mode,
                    )
        self.trajectories_list = trajectories_list
        #find the mbr and then find the enclosing cell, this should be in the pretraining pyramid 
        # cuz of the init of the paritioining class fn
        mbr = partitioning_module.calculate_mbr_gps(trajectories_list = self.trajectories_list)
        print(mbr)
        least_enclosing_cell =  partitioning_module._find_enclosing_cell(mbr)
        if least_enclosing_cell:
            logging.info("Enclosing cell will be %s",least_enclosing_cell)
            l = least_enclosing_cell["height"]
            if self.use_tokenization and self.trajectories_list is not None:
                logging.info(
                    "Tokenizing the provided trajectories and adding to TrajectoryStore."
                )
                self.tokenized_trajectories = self.__tokenization_module(
                self.trajectories_list
                )
                self.trajectories_got_tokenized = True
                
                #if cell is not occupied (first time recieving data in this city)
                '''
                Save data under TrajStore/ pretrainingDatasets/cell#180
                Pretrain all models available in transformersPlugin/pretrainingArchitectures 
                For every model save the checkpoint under modelsRepo/pretrainedModels/cell#180
                Mark cell in the pretraining Pyramid as occupied

                '''
                if not least_enclosing_cell['occupied']:
                    self.data_path_trajectory_store, self.metadata_path_trajectory_store,num_tokens = (
                    self.__save_trajectories_to_store(
                        self.tokenized_trajectories, "pretrainingDatasets",least_enclosing_cell
                        )
                    )
                    #Update the pretrainingDatasets table

                    file_path = pathlib_Path(self.trajecotry_store_path) / "pretrainingDatasets" / 'storedDatasetsMetadata.csv'
                    new_entry = {
                        "DatasetPath": self.data_path_trajectory_store,
                        "Level": l,
                        "Cell": least_enclosing_cell["index"],
                        "NumOfTokens": num_tokens,
                        "PretrainedModels": []
                    }
                    add_entry_to_csv(file_path,new_entry)
                    # If the dataset passes this condition then we can train a model
                    #  and mark it as occupied
                    #  For now I will relax this condition by making the threshhold but need to think abpit this more
                    
                    if num_tokens >= (
                        partitioning_module.tokens_threshold_per_cell * 4 ** (partitioning_module.pyramid_height - l)
                    ):
                        partitioning_module._update_cell_with_model("pretrainedModels",least_enclosing_cell,num_tokens)
                        partitioning_module.save_pyramid()
                        # Now need to start the pretraining here.
                    # Otherwise let's wait for someone else to add more data to this dataset later
                    # I need to think about this part as it is a bit complicated
                    else:
                        raise Warning("Dataset was added to the trajectory store. However, it was not sufficient to trigger models' pretraining. You need to add more trajectories in the same city.")
                    # Need to mark the cell as occupied and save the pyramid

                #if cell is occupied 
                '''
                Go to TrajStore/pretrainingDatasets/cell#180 and combine data in this location with my input data and save it in this location
                Re-Pretrain all models available in transformersPlugin/pretrainingArchitectures
                For every model save the checkpoint under modelsRepo/pretrainedModels/cell#180

                '''
                
               
            else:
                if not self.use_tokenization :
                    raise ValueError("use_tokenization was not set to true, (not allowed in training mode)")
                else:
                    raise ValueError("trajectories list is None, (not allowed in training mode)")

        else:
            raise ValueError("Could not find encosing cell in the pretraining pyramid to contain the dataset (should not happen)...")

        
