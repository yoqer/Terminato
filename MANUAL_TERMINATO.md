# 📖 Manual Terminato - Framework de Entrenamiento

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Uso de la Web Landing](#uso-de-la-web-landing)
5. [API REST](#api-rest)
6. [Entrenamientos](#entrenamientos)
7. [Fusión de Modelos](#fusión-de-modelos)
8. [Análisis de Capas](#análisis-de-capas)
9. [Ejemplos Prácticos](#ejemplos-prácticos)
10. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

**Terminato** es un framework completo de entrenamiento que integra la librería **TeMiNaTor** con una interfaz web intuitiva para:

- ✅ Seleccionar dinámicamente GPU/NVMe disponibles
- ✅ Crear y gestionar sesiones de entrenamiento
- ✅ Fusionar múltiples modelos
- ✅ Fine-tuning dirigido con congelación de capas
- ✅ Reinforcement Learning por capas específicas
- ✅ Análisis detallado de capas
- ✅ Aprendizaje relacional multimodal

---

## Instalación

### Requisitos Mínimos

- **Python 3.10+**
- **CUDA 11.8+** (para GPU)
- **32 GB RAM**
- **1x GPU NVIDIA 16GB** (recomendado)
- **500 GB SSD**

### Requisitos Recomendados

- **Python 3.11**
- **CUDA 12.1+**
- **64-128 GB RAM**
- **2-4x GPU NVIDIA RTX 4090 / A100**
- **2-4x NVMe 2TB**

### Pasos de Instalación

#### 1. Clonar o Extraer el Framework

```bash
# Extraer ZIP
unzip Terminato_Complete.zip
cd Terminato

# O clonar desde git
git clone <repository>
cd Terminato
```

#### 2. Crear Entorno Virtual

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Instalar Dependencias

```bash
# Instalar requisitos base
pip install -r requirements.txt

# Instalar TeMiNaTor desde PyPI (cuando esté disponible)
pip install TeMiNaTor

# O instalar desde fuente
pip install -e /path/to/TeMiNaTor
```

#### 4. Verificar Instalación

```bash
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"
```

---

## Configuración

### Archivo de Configuración Principal

Editar `config/default.yaml`:

```yaml
# Terminato Configuration

server:
  host: "0.0.0.0"
  port: 8000
  workers: 4
  reload: true
  log_level: "info"

training:
  max_iterations: 12          # Convergencia después de 12 iteraciones similares
  early_stopping: true
  checkpoint_interval: 10

device:
  auto_detect: true           # Detectar GPUs automáticamente
  memory_fraction: 0.9        # Usar 90% de memoria GPU

storage:
  models_dir: "./models"
  datasets_dir: "./datasets"
  logs_dir: "./logs"
  checkpoints_dir: "./checkpoints"
```

### Variables de Entorno

```bash
# Crear archivo .env
cat > .env << 'EOF'
# CUDA
CUDA_VISIBLE_DEVICES=0,1,2,3

# Logging
LOG_LEVEL=INFO

# API
API_HOST=0.0.0.0
API_PORT=8000
EOF

# Cargar variables
export $(cat .env | xargs)
```

---

## Uso de la Web Landing

### Iniciar Servidor

```bash
# Opción 1: Script automático
./scripts/start.sh

# Opción 2: Uvicorn directo
python -m uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload

# Opción 3: Con workers para producción
python -m uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Acceder a la Interfaz Web

```
http://localhost:8000
```

### Tabs de la Interfaz

#### 1. **Dispositivos**
- Ver GPUs disponibles
- Ver discos NVMe disponibles
- Seleccionar GPU y NVMe
- Monitorear memoria disponible

#### 2. **Entrenamiento**
- Crear sesiones de entrenamiento
- Configurar parámetros (LR, batch size, épocas)
- Congelar capas específicas
- Monitorear progreso en tiempo real

#### 3. **Sesiones**
- Listar todas las sesiones
- Ver estado de cada sesión
- Acceder a métricas históricas

#### 4. **Análisis**
- Analizar capas específicas
- Ver métricas por capa
- Detectar problemas de entrenamiento

---

## API REST

### Endpoints Principales

#### Dispositivos

**GET /api/devices**
```bash
curl http://localhost:8000/api/devices
```

Respuesta:
```json
{
  "gpus": [
    {
      "id": 0,
      "name": "NVIDIA RTX 4090",
      "total_memory_gb": 24.0,
      "available_memory_gb": 23.5,
      "compute_capability": "8.9"
    }
  ],
  "nvmes": [
    {
      "device": "/dev/nvme0n1",
      "mount_point": "/mnt/nvme0",
      "total_size_gb": 2000.0,
      "available_size_gb": 1800.0
    }
  ]
}
```

**POST /api/devices/select**
```bash
curl -X POST http://localhost:8000/api/devices/select \
  -H "Content-Type: application/json" \
  -d '{
    "gpu_id": 0,
    "nvme_mount": "/mnt/nvme0"
  }'
```

#### Entrenamiento

**POST /api/training/create**
```bash
curl -X POST http://localhost:8000/api/training/create \
  -H "Content-Type: application/json" \
  -d '{
    "session_name": "training_v1",
    "model_path": "/path/to/model.pt",
    "dataset_path": "/path/to/dataset",
    "learning_rate": 0.001,
    "batch_size": 32,
    "max_epochs": 100,
    "frozen_layers": ["layer1", "layer2"]
  }'
```

**POST /api/training/start**
```bash
curl -X POST http://localhost:8000/api/training/start?session_id=training_v1_20240204_120000
```

**GET /api/training/status/{session_id}**
```bash
curl http://localhost:8000/api/training/status/training_v1_20240204_120000
```

#### Fusión de Modelos

**POST /api/models/fuse**
```bash
curl -X POST http://localhost:8000/api/models/fuse \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "training_v1_20240204_120000",
    "model_paths": [
      "/path/to/model1.pt",
      "/path/to/model2.pt",
      "/path/to/model3.pt"
    ],
    "strategy": "average"
  }'
```

Estrategias disponibles:
- `average`: Promedio simple de pesos
- `weighted`: Promedio ponderado
- `max`: Máximo valor por peso
- `min`: Mínimo valor por peso

#### Análisis de Capas

**POST /api/layers/analyze**
```bash
curl -X POST http://localhost:8000/api/layers/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "training_v1_20240204_120000",
    "layer_name": "transformer.layer.5"
  }'
```

Respuesta:
```json
{
  "layer": "transformer.layer.5",
  "accuracy": 0.95,
  "error_rate": 0.05,
  "gradient_flow": "normal",
  "activation_range": [-1.0, 1.0],
  "dead_neurons": 0
}
```

---

## Entrenamientos

### Crear Sesión Simple

```python
from Terminato import TrainingManager
import torch

# Crear manager
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
manager = TrainingManager(device, nvme_path="/mnt/nvme0")

# Crear sesión
session_id = manager.create_training_session(
    session_name="my_training",
    model_path="/path/to/model.pt",
    dataset_path="/path/to/dataset",
    config={
        "learning_rate": 0.001,
        "batch_size": 32,
        "max_epochs": 100
    }
)

# Iniciar entrenamiento
manager.start_training(session_id)

# Ver estado
status = manager.get_session_status(session_id)
print(f"Pérdida: {status['metrics']['loss'][-1]:.4f}")
```

### Entrenamiento con Congelación de Capas

```python
# Congelar capas base
manager.freeze_layers(session_id, ["layer1", "layer2", "layer3"])

# Iniciar fine-tuning
manager.start_training(
    session_id,
    learning_rate=0.0001,  # LR más bajo para fine-tuning
    max_epochs=50
)
```

### Entrenamiento con Reinforcement Learning

```python
# Aplicar RL a una capa específica
manager.apply_reinforcement_learning(
    session_id,
    layer_name="transformer.layer.5",
    feedback={
        "error_rate": 0.05,
        "correction_strength": 0.8
    }
)
```

---

## Fusión de Modelos

### Fusionar Dos Modelos

```python
# Fusionar modelos
success = manager.fuse_models(
    session_id,
    model_paths=[
        "/path/to/model1.pt",
        "/path/to/model2.pt"
    ],
    strategy="average"
)

if success:
    print("Modelos fusionados exitosamente")
```

### Fusionar Múltiples Modelos

```python
# Fusionar 3+ modelos
success = manager.fuse_models(
    session_id,
    model_paths=[
        "/path/to/model_general.pt",
        "/path/to/model_especializado.pt",
        "/path/to/model_fine_tuned.pt"
    ],
    strategy="weighted"  # Promedio ponderado
)
```

---

## Análisis de Capas

### Analizar Capa Específica

```python
# Analizar capa
analysis = manager.evaluate_layer(
    session_id,
    layer_name="transformer.layer.5"
)

print(f"Precisión: {analysis['accuracy']:.2%}")
print(f"Tasa de Error: {analysis['error_rate']:.2%}")
print(f"Flujo de Gradientes: {analysis['gradient_flow']}")
print(f"Neuronas Muertas: {analysis['dead_neurons']}")
```

### Detectar Capas Problemáticas

```python
# Analizar todas las capas
layer_names = ["layer1", "layer2", "layer3", "layer4", "layer5"]

for layer in layer_names:
    analysis = manager.evaluate_layer(session_id, layer)
    
    if analysis['error_rate'] > 0.1:
        print(f"⚠️ {layer}: Error alto ({analysis['error_rate']:.2%})")
    elif analysis['dead_neurons'] > 100:
        print(f"⚠️ {layer}: Neuronas muertas ({analysis['dead_neurons']})")
    else:
        print(f"✅ {layer}: OK")
```

---

## Ejemplos Prácticos

### Ejemplo 1: Fine-Tuning Simple

```python
from Terminato import DeviceManager, TrainingManager
import torch

# 1. Detectar dispositivos
device_mgr = DeviceManager()
print(f"GPUs: {len(device_mgr.get_available_gpus())}")
print(f"NVMes: {len(device_mgr.get_available_nvmes())}")

# 2. Seleccionar dispositivos
device_mgr.select_gpu(0)
device_mgr.select_nvme("/mnt/nvme0")

# 3. Crear manager
device = device_mgr.get_torch_device()
trainer = TrainingManager(device, "/mnt/nvme0")

# 4. Crear sesión
session_id = trainer.create_training_session(
    session_name="bert_finetune",
    model_path="./models/bert-base.pt",
    dataset_path="./datasets/my_data",
    config={"learning_rate": 0.00005}
)

# 5. Congelar capas base
trainer.freeze_layers(session_id, [
    "embeddings",
    "encoder.layer.0",
    "encoder.layer.1",
    "encoder.layer.2"
])

# 6. Entrenar
trainer.start_training(session_id, max_epochs=10)

# 7. Guardar checkpoint
trainer.save_checkpoint(session_id, "./checkpoints/bert_finetuned.json")
```

### Ejemplo 2: Fusión de Modelos

```python
from Terminato import TrainingManager
import torch

device = torch.device("cuda:0")
trainer = TrainingManager(device)

# Crear sesión para fusión
session_id = trainer.create_training_session(
    session_name="model_fusion",
    model_path="./models/base.pt",
    dataset_path="./datasets/test",
    config={}
)

# Fusionar 3 modelos
trainer.fuse_models(
    session_id,
    model_paths=[
        "./models/model_v1.pt",
        "./models/model_v2.pt",
        "./models/model_v3.pt"
    ],
    strategy="weighted"
)

# Entrenar modelo fusionado
trainer.start_training(session_id, max_epochs=20)
```

### Ejemplo 3: Análisis y Corrección de Capas

```python
from Terminato import TrainingManager
import torch

device = torch.device("cuda:0")
trainer = TrainingManager(device)

session_id = trainer.create_training_session(
    session_name="layer_analysis",
    model_path="./models/model.pt",
    dataset_path="./datasets/test",
    config={}
)

# Analizar capas
layers_to_check = [
    "encoder.layer.0",
    "encoder.layer.1",
    "encoder.layer.2",
    "encoder.layer.3"
]

problem_layers = []
for layer in layers_to_check:
    analysis = trainer.evaluate_layer(session_id, layer)
    
    if analysis['error_rate'] > 0.1:
        problem_layers.append(layer)
        print(f"Problema detectado en {layer}")

# Aplicar RL a capas problemáticas
for layer in problem_layers:
    trainer.apply_reinforcement_learning(
        session_id,
        layer_name=layer,
        feedback={"correction_strength": 0.9}
    )

# Entrenar solo las capas problemáticas
trainer.freeze_layers(
    session_id,
    [l for l in layers_to_check if l not in problem_layers]
)
trainer.start_training(session_id, max_epochs=30)
```

---

## Solución de Problemas

### Error: "CUDA out of memory"

**Solución:**
```python
# Reducir batch size
trainer.start_training(session_id, batch_size=8)

# O reducir memory_fraction en config.yaml
device:
  memory_fraction: 0.7  # Usar 70% en lugar de 90%
```

### Error: "GPU not found"

**Solución:**
```bash
# Verificar CUDA
nvidia-smi

# Instalar CUDA Toolkit
# https://developer.nvidia.com/cuda-downloads

# Reinstalar PyTorch con CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Error: "NVMe not mounted"

**Solución:**
```bash
# Listar discos
lsblk

# Montar NVMe
sudo mkdir -p /mnt/nvme0
sudo mount /dev/nvme0n1p1 /mnt/nvme0

# Hacer permanente en /etc/fstab
echo "/dev/nvme0n1p1 /mnt/nvme0 ext4 defaults 0 0" | sudo tee -a /etc/fstab
```

### Entrenamiento muy lento

**Solución:**
```python
# Aumentar batch size
trainer.start_training(session_id, batch_size=128)

# Usar múltiples GPUs (si están disponibles)
# Configurar en config.yaml
device:
  devices: [0, 1, 2, 3]
  strategy: "data_parallel"

# Reducir max_epochs
trainer.start_training(session_id, max_epochs=50)
```

---

## Próximos Pasos

1. **Integración con Hugging Face**: Cargar modelos directamente de HF
2. **Soporte para LoRA**: Fine-tuning eficiente con LoRA
3. **Cuantización**: Comprimir modelos post-entrenamiento
4. **Exportación ONNX**: Convertir a formato ONNX
5. **Despliegue**: Servir modelos con TorchServe

---

## Soporte

- **Documentación**: http://localhost:8000/docs
- **Logs**: `./logs/terminato.log`
- **Issues**: Reportar en el repositorio

---

**Terminato Framework v1.0.0**  
*Listo para Producción*
