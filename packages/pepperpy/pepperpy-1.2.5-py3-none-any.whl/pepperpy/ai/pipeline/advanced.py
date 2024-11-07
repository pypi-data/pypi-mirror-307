from typing import Any, Dict, List, Optional

import numpy as np
from sklearn.model_selection import train_test_split

from ..module import AIModule
from .base import Pipeline


class AdvancedPipelines:
    """Advanced AI pipeline templates"""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}

    @staticmethod
    def create_fine_tuning_pipeline(
        ai_module: "AIModule", validation_split: float = 0.2
    ) -> Pipeline:
        """Create model fine-tuning pipeline"""
        pipeline = Pipeline("fine_tuning")

        # Data preparation step
        async def prepare_data(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            texts = data["texts"]
            labels = data["labels"]

            # Split into train/validation
            train_texts, val_texts, train_labels, val_labels = train_test_split(
                texts, labels, test_size=validation_split
            )

            return {
                "train": {"texts": train_texts, "labels": train_labels},
                "validation": {"texts": val_texts, "labels": val_labels},
            }

        pipeline.add_step("prepare", prepare_data)

        # Tokenization and embedding
        async def embed_texts(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            train_embeddings = await ai_module.embed_batch(data["train"]["texts"])
            val_embeddings = await ai_module.embed_batch(data["validation"]["texts"])

            return {
                "train": {
                    "embeddings": train_embeddings,
                    "labels": data["train"]["labels"],
                },
                "validation": {
                    "embeddings": val_embeddings,
                    "labels": data["validation"]["labels"],
                },
            }

        pipeline.add_step("embed", embed_texts)

        # Model fine-tuning
        async def fine_tune(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            # Implement model fine-tuning logic here
            return {
                "model_path": "path/to/fine_tuned_model",
                "metrics": {
                    "train_loss": 0.1,
                    "val_loss": 0.2,
                    "train_accuracy": 0.95,
                    "val_accuracy": 0.92,
                },
            }

        pipeline.add_step("fine_tune", fine_tune)

        return pipeline

    @staticmethod
    def create_evaluation_pipeline(
        ai_module: "AIModule", metrics: List[str] = ["accuracy", "f1"]
    ) -> Pipeline:
        """Create model evaluation pipeline"""
        pipeline = Pipeline("evaluation")

        # Generate predictions
        async def predict(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            texts = data["texts"]
            predictions = []

            for text in texts:
                response = await ai_module.generate(text, **kwargs)
                predictions.append(response.content)

            return {"predictions": predictions, "ground_truth": data["labels"]}

        pipeline.add_step("predict", predict)

        # Calculate metrics
        async def evaluate(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            from sklearn.metrics import accuracy_score, f1_score

            results = {}
            if "accuracy" in metrics:
                results["accuracy"] = accuracy_score(data["ground_truth"], data["predictions"])
            if "f1" in metrics:
                results["f1"] = f1_score(
                    data["ground_truth"], data["predictions"], average="weighted"
                )

            return results

        pipeline.add_step("evaluate", evaluate)

        return pipeline

    @staticmethod
    def create_data_augmentation_pipeline(
        ai_module: "AIModule", num_variations: int = 3
    ) -> Pipeline:
        """Create data augmentation pipeline"""
        pipeline = Pipeline("augmentation")

        # Generate variations
        async def generate_variations(texts: List[str], **kwargs) -> Dict[str, Any]:
            variations = []

            for text in texts:
                text_variations = []
                for _ in range(num_variations):
                    prompt = f"Generate a different version of: {text}"
                    response = await ai_module.generate(prompt, **kwargs)
                    text_variations.append(response.content)
                variations.extend(text_variations)

            return {"original": texts, "variations": variations}

        pipeline.add_step("generate", generate_variations)

        # Filter and validate variations
        async def validate_variations(data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
            original_embeddings = await ai_module.embed_batch(data["original"])
            variation_embeddings = await ai_module.embed_batch(data["variations"])

            # Calculate similarities
            valid_variations = []
            for i, var_emb in enumerate(variation_embeddings):
                # Find closest original
                similarities = [np.dot(var_emb, orig_emb) for orig_emb in original_embeddings]
                max_sim = max(similarities)

                # Keep if similar enough but not too similar
                if 0.7 <= max_sim <= 0.9:
                    valid_variations.append(data["variations"][i])

            return {"augmented_data": valid_variations}

        pipeline.add_step("validate", validate_variations)

        return pipeline
