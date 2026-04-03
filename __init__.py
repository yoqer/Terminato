"""
Terminato Framework
===================

Framework de entrenamiento e inferencia que integra la librería TeMiNaTor
con interfaz web para control de GPU/NVMe y gestión de entrenamientos.

Características:
- Fusión de modelos
- Fine-tuning dirigido
- Reinforcement Learning por capas
- Aprendizaje relacional multimodal
- Análisis de capas
- Selección dinámica de GPU/NVMe
"""

__version__ = "1.0.0"
__author__ = "Terminato Team"
__description__ = "Framework de entrenamiento dirigido con TeMiNaTor"

from .core.device_manager import DeviceManager
from .training.trainer import TrainingManager
from .inference.predictor import InferenceEngine

__all__ = [
    "DeviceManager",
    "TrainingManager", 
    "InferenceEngine",
]
