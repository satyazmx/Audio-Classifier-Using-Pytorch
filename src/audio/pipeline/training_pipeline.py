import sys
from src.audio.components.data_ingestion import DataIngestion
from src.audio.components.data_transformation import DataTransformation
from src.audio.components.model_training import ModelTraining
from src.audio.components.mode_pusher import ModelPusher
from src.audio.logger import logging
from src.audio.exception import CustomException
from src.audio.entity.config_entity import *
from src.audio.entity.artifact_entity import *
from src.audio.components.model_evaluation import ModelEvaluation

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.model_evaluation_config = ModelEvaluationConfig()

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Starting data ingestion in training pipeline")
        try: 
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion step completed successfully in train pipeline")
            return data_ingestion_artifacts
        except Exception as e:
            raise CustomException(e, sys)
        
    def start_data_transformation(self,data_ingestion_artifacts: DataIngestionArtifacts) ->DataTransformationArtifacts:
        logging.info("Starting data preprocessing in training pipeline")
        try: 
            data_transformation = DataTransformation(data_transformation_config=self.data_transformation_config,
            data_ingestion_artifact=data_ingestion_artifacts)
            data_preprocessing_artifacts = data_transformation.initiate_data_transformation()
            logging.info("Data preprocessing step completed successfully in train pipeline")
            return data_preprocessing_artifacts
        except Exception as e:
            raise CustomException(e, sys)
        
    def start_model_trainer(self,data_transformation_artifact : DataTransformationArtifacts):
        try:
            logging.info("Entered the start_model_trainer method of TrainPipeline class")
            
            model_trainer = ModelTraining(data_transformation_artifact=data_transformation_artifact,
            model_trainer_config=self.model_trainer_config)
            model_trainer_artifact =  model_trainer.initiate_model_trainer()
            logging.info("Exited the start_model_trainer method of TrainPipeline class")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_model_evaluation(self,data_transformation_artifact: DataTransformationArtifacts,model_trainer_artifacts: ModelTrainerArtifacts) -> ModelEvaluationArtifacts:
        logging.info("Starting model evaluation in training pipeline")
        try: 
            model_evaluation = ModelEvaluation(self.model_evaluation_config, data_transformation_artifact, model_trainer_artifacts)
            logging.info("Evaluating current trained model")
            model_evaluation_artifacts = model_evaluation.initiate_model_evaluation()
            logging.info("Model evaluation step completed successfully in train pipeline")
            return model_evaluation_artifacts
        except Exception as e:
            raise CustomException(e, sys)
        
    def start_model_pusher(self, model_evaluation_artifacts: ModelEvaluationArtifacts):
        logging.info("Starting model pusher in training pipeline")
        try: 
            model_pusher = ModelPusher(model_evaluation_artifacts=model_evaluation_artifacts)
            logging.info("If model is accepted in model evaluation. Pushing the model into production storage")
            model_pusher_artifacts = model_pusher.initiate_model_pusher()
            logging.info("Model pusher step completed successfully in train pipeline")
            return model_pusher_artifacts
        except Exception as e:
            raise CustomException(e, sys)
        
    def run_pipeline(self) -> None:
        logging.info(">>>> Initializing training pipeline <<<<")
        try:
            data_ingestion_artifacts = self.start_data_ingestion()
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifacts=data_ingestion_artifacts)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifacts = self.start_model_evaluation(data_transformation_artifact, model_trainer_artifact)
            model_pusher_artifact = self.start_model_pusher(model_evaluation_artifacts=model_evaluation_artifacts)
            print(model_pusher_artifact)
        except Exception as e:
            raise CustomException(e, sys)