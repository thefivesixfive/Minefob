# Minefob

Minefob is a Python module that provides full control
over any Minehut server by utilizing the Minehut API

## Installation

Use the package manager [pip](https://pypi.org/project/minefob) to install Minefob.

```bash
pip install minefob
```

## Usage

```python
from minefob import Minefob

# Instantiate a new instance of the Minefob class and provide it with
# Minehut account email, password, and server name
m = Minefob("foo_foo@example.domain", "123456789", "my_server")
m.awaken() # starts server
m.say("Hello Word") # says "Hello World" in server chat
m.slumber(10) # gives a ten second countdown before kicking players,
			  # saving the world, and shutting down the server
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)