# 🤖 Terminato Framework

**Framework de Entrenamiento Dirigido con TeMiNaTor del proyecto [AlIAmAlIA](http://github.com/yoqer/AlIAmAlIA)** [(Uso Web)](http://carlomaxxine.com/tragadatos/Enhanced/frontend/dashboard_v5.html)




[![wapi](https://github.com/user-attachments/assets/c47b040f-dd26-4b2f-a813-1f778d017b5f)](http://carlomaxxine.com/tragadatos/Enhanced/frontend/dashboard_v5.html)




Sistema completo para entrenar, fusionar y analizar modelos de IA con control dinámico de GPU/NVMe, interfaz web intuitiva y API REST.

## 🚀 Inicio Rápido

```bash
# 1. Extraer framework
unzip Terminato_Complete.zip

cd Terminato




# 2. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac

# o

venv\Scripts\activate  # Windows


# 3. Instalar dependencias
pip install -r requirements.txt


# 4. Iniciar servidor
python -m uvicorn api.app:app --host 0.0.0.0 --port 8000


# 5. Acceder a http://localhost:8000
```



## ✨ Características

### 🎯 Selección de Dispositivos
- Detectar automáticamente GPUs disponibles
- Detectar discos NVMe
- Seleccionar GPU/NVMe desde interfaz web
- Monitoreo de memoria en tiempo real

### 🏋️ Entrenamientos
- Crear sesiones de entrenamiento
- Configurar learning rate, batch size, épocas
- Congelar capas específicas
- Monitoreo en tiempo real
- Early stopping (12 iteraciones similares)
- Guardado de checkpoints

### 🔀 Fusión de Modelos
- Fusionar 2+ modelos
- Estrategias: average, weighted, max, min
- Eliminar pesos duplicados
- Combinar especialidades

### 🔬 Análisis de Capas
- Evaluar capas específicas
- Detectar problemas de entrenamiento
- Análisis de gradientes
- Identificar neuronas muertas
- Dirigir RL a capas problemáticas

### 🧠 Reinforcement Learning
- Feedback por capas
- Corrección automática de errores
- Steering de modelos
- Aprendizaje relacional multimodal



## 📋 Requisitos

### Mínimos
- Python 3.10+
- 32 GB RAM
- 1x GPU NVIDIA 16GB
- 500 GB SSD

### Recomendados
- Python 3.11
- 64-128 GB RAM
- 2-4x GPU NVIDIA RTX 4090/A100
- 2-4x NVMe 2TB

## 📖 Documentación

- **Manual Completo**: Ver `MANUAL_TERMINATO.md`
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc


## 🌐 Interfaz Web

### Tabs Disponibles

1. **Dispositivos**: Seleccionar GPU/NVMe
2. **Entrenamiento**: Crear y monitorear entrenamientos
3. **Sesiones**: Listar sesiones históricas
4. **Análisis**: Analizar capas específicas


## 🔌 API REST


### Endpoints Principales

```bash
# Obtener dispositivos
GET /api/devices

# Seleccionar dispositivos
POST /api/devices/select

# Crear sesión
POST /api/training/create

# Iniciar entrenamiento
POST /api/training/start

# Ver estado
GET /api/training/status/{session_id}

# Fusionar modelos
POST /api/models/fuse

# Analizar capa
POST /api/layers/analyze

# Listar sesiones
GET /api/training/sessions
```

## 💻 Uso Programático

```python
from Terminato import DeviceManager, TrainingManager
import torch

# Detectar dispositivos
device_mgr = DeviceManager()
device_mgr.select_gpu(0)
device_mgr.select_nvme("/mnt/nvme0")

# Crear trainer
device = device_mgr.get_torch_device()
trainer = TrainingManager(device, "/mnt/nvme0")

# Crear sesión
session_id = trainer.create_training_session(
    session_name="my_training",
    model_path="./models/model.pt",
    dataset_path="./datasets/data",
    config={"learning_rate": 0.001}
)

# Congelar capas
trainer.freeze_layers(session_id, ["layer1", "layer2"])

# Entrenar
trainer.start_training(session_id, max_epochs=100)

# Analizar
analysis = trainer.evaluate_layer(session_id, "layer3")
print(f"Precisión: {analysis['accuracy']:.2%}")
```

## 📁 Estructura del Proyecto

```
Terminato/
├── api/
│   ├── app.py              # API REST con FastAPI
│   └── __init__.py
├── core/
│   ├── device_manager.py   # Gestión de GPU/NVMe
│   └── __init__.py
├── training/
│   ├── trainer.py          # Manager de entrenamientos
│   └── __init__.py
├── inference/
│   ├── __init__.py
├── web/
│   ├── index.html          # Landing page web
│   └── __init__.py
├── config/
│   ├── default.yaml        # Configuración
│   └── __init__.py
├── models/                 # Modelos guardados
├── datasets/               # Datasets
├── logs/                   # Logs
├── requirements.txt        # Dependencias
├── MANUAL_TERMINATO.md     # Manual completo
├── README.md               # Este archivo
└── __init__.py
```

## 🔧 Configuración

Editar `config/default.yaml`:

```yaml
server:
  host: "0.0.0.0"
  port: 8000
  workers: 4

training:
  max_iterations: 12
  early_stopping: true

device:
  auto_detect: true
  memory_fraction: 0.9

storage:
  models_dir: "./models"
  datasets_dir: "./datasets"
```

## 📊 Ejemplos

### Fine-Tuning Simple

```python
trainer = TrainingManager(device)
session_id = trainer.create_training_session(
    "bert_finetune",
    "./models/bert.pt",
    "./datasets/my_data",
    {}
)
trainer.freeze_layers(session_id, ["embeddings", "encoder.layer.0"])
trainer.start_training(session_id, max_epochs=10)
```

### Fusión de Modelos

```python
trainer.fuse_models(
    session_id,
    [
        "./models/model1.pt",
        "./models/model2.pt",
        "./models/model3.pt"
    ],
    strategy="weighted"
)
```

### Análisis de Capas

```python
analysis = trainer.evaluate_layer(session_id, "transformer.layer.5")
print(f"Error: {analysis['error_rate']:.2%}")
print(f"Neuronas muertas: {analysis['dead_neurons']}")
```

## 🚀 Despliegue

### Local
```bash
python -m uvicorn api.app:app --reload
```

### Producción
```bash
python -m uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```bash
docker build -t terminato:latest .
docker run -d --gpus all -p 8000:8000 terminato:latest
```

## 📝 Logs

```bash
# Ver logs
tail -f logs/terminato.log

# Nivel de log en config.yaml
server:
  log_level: "info"  # debug, info, warning, error
```

## 🆘 Solución de Problemas

### CUDA out of memory
```python
trainer.start_training(session_id, batch_size=8)
```

### GPU no detectada
```bash
nvidia-smi
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### NVMe no montado
```bash
sudo mount /dev/nvme0n1p1 /mnt/nvme0
```

Ver `MANUAL_TERMINATO.md` para más soluciones.

## 📦 Dependencias

- **torch** >= 2.0.0
- **transformers** >= 4.30.0
- **fastapi** >= 0.100.0
- **uvicorn** >= 0.23.0
- **pydantic** >= 2.0.0
- **numpy** >= 1.24.0

## 📄 Licencia

MIT License

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

- **Documentación**: http://localhost:8000/docs
- **Manual**: `MANUAL_TERMINATO.md`
- **Issues**: Reportar en GitHub

---

**Terminato Framework v1.0.0**  
*Framework de Entrenamiento Dirigido con TeMiNaTor*  
*Listo para Producción*
