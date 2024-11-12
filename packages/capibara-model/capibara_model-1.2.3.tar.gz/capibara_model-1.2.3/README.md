# CapibaraModel CLI

![Capibara SSBD Model](./capibara_model/src/public/3BSSBD.webp)

CapibaraModel is a command-line tool for training, evaluating, and deploying language models based on State Space and Mamba architectures, optimized for TPUs and featuring advanced hyperparameter optimization.

## 🚀 Key Features

- **Advanced Architectures**:
  - BitNet + Liquid Architecture
  - Aleph-TILDE Module Integration
  - Mamba SSM Architecture
  - Capibara JAX SSM Implementation
  
- **Core Capabilities**:
  - Model training and evaluation
  - Native TPU/GPU support
  - Automatic hyperparameter optimization
  - Integrated deployment system
  - Performance measurement
  - Docker containers (optional)
  - Weights & Biases integration

## 📋 Requirements

- Python 3.9+
- JAX 0.4.13+
- CUDA 11.8+ (for GPU)
- TensorFlow 2.13+
- Weights & Biases
- Docker (optional)

## 🛠️ Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/anachroni-io/CapibaraModel-cli.git
   cd CapibaraModel-cli
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up Weights & Biases:

   ```bash
   wandb login
   ```

## 📖 Documentation

Full documentation available at [Read the Docs](https://capibaramodel.readthedocs.io/):

- Quick start guide
- Complete tutorial
- API reference
- Usage examples
- Contribution guide

## 💻 Usage

```bash
capibara [options]

# Basic training
capibara --train

# Evaluation with specific layer
capibara --evaluate --new-layer BitNetLiquid

# Optimization with sub-model
capibara --optimize --sub-model AlephTilde
```

### Available Options

- `--log-level`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `--train`: Train model
- `--evaluate`: Evaluate model
- `--optimize`: Hyperparameter optimization
- `--deploy`: Deploy model
- `--measure-performance`: Measure performance
- `--model`: Path to model YAML file
- `--new-layer`: Activate new layers
- `--sub-model`: Specify sub-models

## ⚙️ Configuration

```yaml
model:
  name: "capibara-ent"
  version: "2.0"
  layers:
    - type: "BitNetLiquid"
      config:
        hidden_size: 768
        num_heads: 12
    - type: "AlephTilde"
      config:
        rule_format: "prolog"
        min_confidence: 0.8
```

## 🧪 Testing

```bash
# Unit tests
pytest tests/

# Integration tests
pytest tests/integration/

# Verify documentation
sphinx-build -b doctest docs/source/ docs/build/
```

## 📝 Citation

```bibtex
@software{capibara2024,
  author = {Durán, Marco},
  title = {CapibaraModel: A Large Language Model Framework},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/anachroni-io/CapibaraModel-cli}
}
```

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📫 Contact

Marco Durán - marco@anachroni.co

[Website](https://www.anachroni.co) | [GitHub](https://github.com/anachroni-io/CapibaraModel-cli)
