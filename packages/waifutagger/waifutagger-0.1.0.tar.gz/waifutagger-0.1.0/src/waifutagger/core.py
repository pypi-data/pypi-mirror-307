from typing import Dict, List, Optional, Union, Tuple
import numpy as np
import onnxruntime as rt
import pandas as pd
from PIL import Image
import huggingface_hub
import time
import logging
from pathlib import Path

from .constants import (
    AVAILABLE_MODELS,
    KAOMOJI,
    MODEL_FILENAME,
    LABEL_FILENAME,
    CATEGORY_MAPPING,
    DEFAULT_GENERAL_THRESHOLD,
    DEFAULT_CHARACTER_THRESHOLD
)
from .utils import setup_logger, get_elapsed_time

logger = setup_logger()

class WaifuTagger:
    """Main class for image tagging using WaifuDiffusion models."""
    
    def __init__(
        self, 
        model_key: str = "swinv2-v3",
        verbose: bool = False
    ):
        """
        Initialize the tagger.
        
        Args:
            model_key: Key from AVAILABLE_MODELS
            verbose: Whether to print verbose output
        """
        self.verbose = verbose
        self._model_target_size = None
        self._model = None
        self._tag_names = []
        self._rating_indexes = []
        self._general_indexes = []
        self._character_indexes = []
        
        if model_key not in AVAILABLE_MODELS:
            raise ValueError(
                f"Model {model_key} not found. Available models: {list(AVAILABLE_MODELS.keys())}"
            )
        
        self.load_model(AVAILABLE_MODELS[model_key])
    
    @staticmethod
    def list_models() -> List[str]:
        """Return list of available models."""
        return list(AVAILABLE_MODELS.keys())
    
    def load_model(self, model_repo: str) -> None:
        """
        Load model and labels from HuggingFace hub.
        
        Args:
            model_repo: HuggingFace repository name
        """
        start_time = time.time()
        if self.verbose:
            logger.info("Starting model download...")
        
        try:
            # Download files
            csv_path = huggingface_hub.hf_hub_download(model_repo, LABEL_FILENAME)
            model_path = huggingface_hub.hf_hub_download(model_repo, MODEL_FILENAME)
            
            if self.verbose:
                logger.info(f"Files downloaded in {get_elapsed_time(start_time)}")
            
            # Load and process labels
            tags_df = pd.read_csv(csv_path)
            self._tag_names = tags_df['name'].tolist()
            
            # Process special tags (kaomoji)
            self._tag_names = [
                tag if tag in KAOMOJI else tag.replace('_', ' ')
                for tag in self._tag_names
            ]
            
            # Get category indices
            self._rating_indexes = list(np.where(tags_df['category'] == CATEGORY_MAPPING['rating'])[0])
            self._general_indexes = list(np.where(tags_df['category'] == CATEGORY_MAPPING['general'])[0])
            self._character_indexes = list(np.where(tags_df['category'] == CATEGORY_MAPPING['character'])[0])
            
            if self.verbose:
                logger.info(f"Labels processed in {get_elapsed_time(start_time)}")
            
            # Load ONNX model
            self._model = rt.InferenceSession(model_path)
            _, height, width, _ = self._model.get_inputs()[0].shape
            self._model_target_size = height
            
            if self.verbose:
                logger.info(f"Model loaded in {get_elapsed_time(start_time)}")
                
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def prepare_image(self, image_path: Union[str, Path]) -> np.ndarray:
        """
        Prepare image for inference.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Preprocessed image array
        """
        start_time = time.time()
        if self.verbose:
            logger.info(f"Processing image: {image_path}")
        
        try:
            # Load and convert image
            image = Image.open(image_path).convert('RGBA')
            
            # Convert to RGB with white background
            canvas = Image.new('RGB', image.size, (255, 255, 255))
            canvas.paste(image, mask=image.split()[3])
            image = canvas
            
            # Pad to square
            max_dim = max(image.size)
            pad_left = (max_dim - image.size[0]) // 2
            pad_top = (max_dim - image.size[1]) // 2
            
            padded_image = Image.new('RGB', (max_dim, max_dim), (255, 255, 255))
            padded_image.paste(image, (pad_left, pad_top))
            
            # Resize if needed
            if max_dim != self._model_target_size:
                padded_image = padded_image.resize(
                    (self._model_target_size, self._model_target_size),
                    Image.BICUBIC
                )
            
            # Convert to array
            image_array = np.asarray(padded_image, dtype=np.float32)
            image_array = image_array[:, :, ::-1]  # RGB to BGR
            
            if self.verbose:
                logger.info(f"Image processing completed in {get_elapsed_time(start_time)}")
            
            return np.expand_dims(image_array, axis=0)
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise
    
    def _mcut_threshold(self, probs: np.ndarray) -> float:
        """Calculate MCut threshold from probabilities."""
        sorted_probs = np.sort(probs)[::-1]
        difs = sorted_probs[:-1] - sorted_probs[1:]
        t = difs.argmax()
        return (sorted_probs[t] + sorted_probs[t + 1]) / 2
    
    def predict(
        self,
        image_path: Union[str, Path],
        general_threshold: float = DEFAULT_GENERAL_THRESHOLD,
        general_use_mcut: bool = False,
        character_threshold: float = DEFAULT_CHARACTER_THRESHOLD,
        character_use_mcut: bool = False
    ) -> Dict:
        """
        Predict tags for an image.
        
        Args:
            image_path: Path to image file
            general_threshold: Threshold for general tags
            general_use_mcut: Whether to use MCut for general tags
            character_threshold: Threshold for character tags
            character_use_mcut: Whether to use MCut for character tags
            
        Returns:
            Dictionary containing predictions
        """
        start_time = time.time()
        if self.verbose:
            logger.info("Starting prediction process")
        
        try:
            # Prepare image
            image = self.prepare_image(image_path)
            
            # Run inference
            input_name = self._model.get_inputs()[0].name
            label_name = self._model.get_outputs()[0].name
            predictions = self._model.run([label_name], {input_name: image})[0]
            
            if self.verbose:
                logger.info(f"Inference completed in {get_elapsed_time(start_time)}")
            
            # Process predictions
            labels = list(zip(self._tag_names, predictions[0].astype(float)))
            
            # Get ratings
            ratings = {labels[i][0]: labels[i][1] for i in self._rating_indexes}
            rating = max(ratings.items(), key=lambda x: x[1])
            
            # Process general tags
            general_predictions = np.array([labels[i][1] for i in self._general_indexes])
            general_names = [labels[i][0] for i in self._general_indexes]
            
            if general_use_mcut:
                general_threshold = self._mcut_threshold(general_predictions)
                if self.verbose:
                    logger.info(f"MCut general threshold: {general_threshold:.3f}")
            
            general_tags = {
                name: conf for name, conf in zip(general_names, general_predictions)
                if conf > general_threshold
            }
            
            # Process character tags
            character_predictions = np.array([labels[i][1] for i in self._character_indexes])
            character_names = [labels[i][0] for i in self._character_indexes]
            
            if character_use_mcut:
                character_threshold = self._mcut_threshold(character_predictions)
                character_threshold = max(0.15, character_threshold)
                if self.verbose:
                    logger.info(f"MCut character threshold: {character_threshold:.3f}")
            
            character_tags = {
                name: conf for name, conf in zip(character_names, character_predictions)
                if conf > character_threshold
            }
            
            results = {
                'rating': rating,
                'general_tags': dict(sorted(general_tags.items(), key=lambda x: x[1], reverse=True)),
                'character_tags': dict(sorted(character_tags.items(), key=lambda x: x[1], reverse=True)),
                'thresholds': {
                    'general': general_threshold,
                    'character': character_threshold
                }
            }
            
            if self.verbose:
                logger.info(f"Total prediction completed in {get_elapsed_time(start_time)}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise