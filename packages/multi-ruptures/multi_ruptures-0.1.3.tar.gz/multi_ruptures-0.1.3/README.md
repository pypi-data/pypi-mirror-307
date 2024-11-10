# Multi-ruptures

## Features

🔥 A powerful Python library for multiple change point detection with:

- High-performance implementation of rupture detection algorithms
- Support for multiple data types (time series, signals, sequences)
- Easy-to-use API for both beginners and advanced users
- Comprehensive visualization tools
- Extensive documentation and examples

## 🚀 Quick Start

> **Note**: Requires Python 3.8+

1. Install via pip:

```bash
pip install multi-ruptures
```

2. Basic usage:

```python
import multi_ruptures as mr

# Load your data
signal = ...

# Detect change points
algo = mr.Pelt()
change_points = algo.fit_predict(signal)
```

## 📊 Examples

```python
# Example with visualization
import multi_ruptures as mr
import matplotlib.pyplot as plt

# Generate sample signal
signal = mr.datasets.generate_random_peaks(n_samples=1000)

# Detect ruptures
algo = mr.Pelt(model="rbf", min_size=5)
change_points = algo.fit_predict(signal)

# Display results
mr.display(signal, change_points)
plt.show()
```

## 🛠️ Development

For development setup:

1. Clone the repository
2. Install development dependencies:

```bash
make install-dev
```

## 🧪 Testing

Run tests with:

```bash
make test
```

## 📚 Documentation

Full documentation is available at [docs/](./docs).

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.
