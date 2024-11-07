# Toycode

A simple project to experiment with building python wheels.

## Description

Using pyproject.toml to build is very simple. I'm using this project to further my understanding to build complete python wheels.

## Getting Started

### Dependencies

* This project needs at least a Linux operating system, but should work with Windows or Mac (Not tested).

### Building Steps

* It's recommend to build a virtual environment.
```
$ cd toycode
$ python3 -m venv toycode
$ . toycode/bin/activate
(toycode) $ python -m build
```

### Install Wheel

* The build wheel is located in the **dist** directory.
```
(toycode) $ cd dist
(toycode) $ python install toycode-0.0.1-*.whl
```

### [OPTIONAL] Package Upload to Pypi.org

* Make sure $HOME/.pypirc has been setup with `__token__` and `password` for twine.

```
(toycode) $ python -m twine upload dist/*
```

### Executing program

* How to run the program
```
(toycode)$ toycode-cli
```

## Authors

Contributors names and contact info

Juan Antonio Sauceda [@skibur](https://x.com/skibur)

## Version History

* 0.0.1
    * Initial Release

## License

This project is licensed under the GPL 2.0 License - see the LICENSE.txt file for details