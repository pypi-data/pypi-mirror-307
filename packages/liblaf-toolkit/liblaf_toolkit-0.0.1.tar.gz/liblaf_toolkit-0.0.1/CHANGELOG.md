# Changelog

## [0.0.1](https://github.com/liblaf/python-toolkit/compare/v0.0.0...v0.0.1) (2024-11-11)


### ✨ Features

* add logging functionality for additional experiment data ([b0ea8fb](https://github.com/liblaf/python-toolkit/commit/b0ea8fb1e4845e9f198d365c5226fd0777ebfcd2))


### ♻ Code Refactoring

* **exp:** reorganize experiment module for clarity and maintainability ([24373c0](https://github.com/liblaf/python-toolkit/commit/24373c03cefa8743d9e52f2e6389bff18238879d))


### 🔧 Continuous Integration

* enable write permissions for GitHub Actions OIDC tokens ([0d5a367](https://github.com/liblaf/python-toolkit/commit/0d5a3671b291f9de61f1c2bbdb5807d518681964))

## 0.0.0 (2024-11-11)


### ✨ Features

* add support for Nx4 array types across all array libraries ([47dbb2c](https://github.com/liblaf/python-toolkit/commit/47dbb2c222a4e0225e5a6a5d7aad091f4db253d3))
* enhance experiment logging and configuration ([6865d76](https://github.com/liblaf/python-toolkit/commit/6865d769c9e0ea5a8dd0d49ea65820c4ab8530ff))
* implement array type handling for JAX, NumPy, and PyTorch ([fd7d97a](https://github.com/liblaf/python-toolkit/commit/fd7d97a43f68be0a8364a9e533b524a1094c9949))
* integrate comet-ml for experiment tracking and add environment variable utilities ([96ddd0e](https://github.com/liblaf/python-toolkit/commit/96ddd0ee332f903478deef1dc8b254fbb4334ece))
* introduce base parameters for experiments ([a12d637](https://github.com/liblaf/python-toolkit/commit/a12d637d9fe599708e158a1e870bdd367d78e9e8))
* introduce new utility modules and enhance logging ([38bf1b4](https://github.com/liblaf/python-toolkit/commit/38bf1b4a57594b156a0c10947723df00411c669a))


### 🐛 Bug Fixes

* correct tqdm dependency version to avoid bug ([6cc811c](https://github.com/liblaf/python-toolkit/commit/6cc811c62e2eb4bcab64d63d2b4cd5d61385f940))


### ♻ Code Refactoring

* enhance array type handling by adding conversion utilities ([ce1f8ee](https://github.com/liblaf/python-toolkit/commit/ce1f8eebf31a0a55ae0fffe301dfb151bfba039d))
* **exp:** rename BaseParams to BaseConfig for clarity and consistency ([c54bab2](https://github.com/liblaf/python-toolkit/commit/c54bab290601373d1b8d3c453468acd2242c816c))
* reorganize imports and update log file names ([cec13d5](https://github.com/liblaf/python-toolkit/commit/cec13d519fea056be48dcf29639637dcb12c074e))
* standardize array shape notation in type annotations ([24d3011](https://github.com/liblaf/python-toolkit/commit/24d30119ba119ae1972b4c852f018ffc29ca1e0d))


### 🔧 Continuous Integration

* configure default settings for Python linter ([0441145](https://github.com/liblaf/python-toolkit/commit/0441145ad1cda5e557451446e336c083cf15b394))
* enable concurrency control to cancel in-progress workflows ([bd4f084](https://github.com/liblaf/python-toolkit/commit/bd4f084d7fcbe7de7b0569e4c1a81b4894cd2aae))
* ensure build job completion before release and pre-release jobs ([747f356](https://github.com/liblaf/python-toolkit/commit/747f35656630516e2e2cc9170e010bd5900586fc))
* remove uv.lock to prevent CI failure due to unavailable PyPI mirror ([a7f28af](https://github.com/liblaf/python-toolkit/commit/a7f28af6806663ccd6412952dbb3940b224e8d1b))
* set up continuous integration and release workflows ([e34cf2a](https://github.com/liblaf/python-toolkit/commit/e34cf2ae0213c532353cfabe62ecafa4104910a0))
