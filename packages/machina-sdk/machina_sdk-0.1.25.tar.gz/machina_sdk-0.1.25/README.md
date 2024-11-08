## Installation

```
python3.11 -m venv venv

source venv/bin/activate

pip install pdm

pip install build

pdm install

python -m build

pip install ~/machina/machina-core-sdk/dist/machina_sdk-0.1.21-py3-none-any.whl --force-reinstall

```


## Publication

pip install twine

twine upload dist/*


## Publish Via git workflow

git tag v0.1.16

git push origin v0.1.16
