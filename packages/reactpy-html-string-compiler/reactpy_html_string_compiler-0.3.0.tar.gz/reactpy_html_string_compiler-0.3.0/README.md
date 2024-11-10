# Reactpy Html String Compiler #

compiles ReactPy Components into a HTML String

## Why would you use this? ##

you could use the converted html string in flask or other templating engines

## How to use this? ##

this module has only 1 function, ``` compiler(component : Reactpy.Types.Component) -> str ```, which takes in a reactpy component and returns a string

```python
    from reactpy import component, html
    from reactpy_html_string_compiler import compiler
    from flask import Flask # or any other backend

    @component
    def header():
        return html.h1("Hello, World", {"id": "header"})

    # utilizing component

    app = Flask(__name__)

    @app.route("/")
    def index():
        return compiler(header()) # -> <h1 id="header">Hello, World</h1>

    app.run('0.0.0.0', 3000)
```

# dependencies #
 * [[reactpy logo](https://raw.githubusercontent.com/reactive-python/reactpy/refs/heads/main/branding/png/reactpy-logo-landscape.png)](https://reactpy.dev)