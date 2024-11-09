# Class Instance Configurator

A simple configuration library allowing instantiation of classes from config. files.

Configuration files are in JSON format and simply specify the type of the created object
and keyword arguments for its construction.
The library also supports free-form config. objects for which respective dataclass-like
types are automatically created from a meta-class (so that the programmer doesn’t even
have to declare them).

Support for remote config. is provided by (optional) use of `smart-open`.

The library also provides dot-path syntax access to configuration object hierarchy.

## Examples

### Instantiation of a class from config. file

Assuming you have the following general class:

**my\_module.py**

    from confcls import Configurable

    class MyClass(Configurable):
        def __init__(self, arg1: str, arg2: int, arg3: list[str], arg4: dict[str, float]):
            self.foo = arg1
            self.bar = arg2
            self.baz = [arg4[name] for name in arg3 if name in arg4]

You can now store its instance configuration in a JSON file:

**my\_obj.json**

    {
        "__type__" : "my_module::MyClass",
        "arg1" : "Hello world!",
        "arg2" : 123,
        "arg3" : ["abc", "ghi"],
        "arg4" : {
            "abc" : 0.123,
            "def" : 0.987
        }
    }

And instantiate the configured instance, thus:

    from my_module import MyClass

    my_obj = MyClass.from_config("my_obj.json")

(You may also call `confcls.Configurable.from_config` directly if you don’t wish
to specify and/or import the type.)

In `confcls` v2, the common plain dot notation of `type` values changed
to the following: `my.module.path::My.Class.Path`; that is to say, class specification
are separated from module specification by `::`.
This is necessary to support nested classes.

The instantiation does support nesting; your constructor arguments may indeed be other
class instances:

**my\_obj.json**

    {
        "__type__" : "my_module::Class1",
        "foo" : 123,
        "bar" : {
            "__type__" : "my_module::Class2",
            "arg1" : 345,
            "arg2" : "whatever"
        },
        "baz" : {
            "__type__" : "my_module::Class3",
            "arg" : {
                "__type__" : "my_module::Class2",
                "arg1" : 567,
                "arg2" : "something else"
            }
        }
    }

The above configuration instantiates the same object as the following code:

    my_obj = Class1(
        foo=123,
        bar=Class2(arg1=345, arg2="whatever"),
        baz=Class3(arg=Class2(arg1=567, arg2="something else)),
    )

### Dataclass config

You may want to create a (nested) dataclass configuration.
The principle is exactly the same as above; you simply define your configuration
data classes and instantiate them from configuration:

**my\_config.py**

    from dataclasses import dataclass
    from confcls import Configurable

    @dataclass
    class Configuration(Configurable):
        number: int
        fpnum: float = 0.0  # number with default
        item1: Item1
        opt_item2: Item2 = None  # optional instance

    @dataclass
    class Item1:  # note that nested dataclasses don't even need to be Configurable
        foo: int
        bar: float = 1.0

    @dataclass Item2:
        baz: str

Now, your configuration may look like this:

    {
        "__type__" : "my_config::Configuration",
        "number" : 123,
        "item1" : {
            "__type__" : "my_config::Item1",
            "foo" : 345,
            "bar" : 0.5
        }
    }

### Automatic dataclass-like instances

If you’re very lazy, you don’t even have to declare your config. dataclasses.
Just let `confcls` create the types for you, on demand:

**my\_config.json**

    {
        "__type__" : "confcls::Configuration",
        "myarg1" : "whatever you like",
        "myarg2" : {
            "__type__" : "confcls::Object",
            "absolutely" : "anything",
            "really" : 123
        }
    }

`confcls.Object` is a free-form class which can be instantiated with any keyword
arguments (and the instance contains them as members).
So now, you can access your configuration e.g. like this:

    from confcls import Configuration  # Configurable extension of confcls.Object

    config = Configuration.from_config("my_config.json")
    assert config.myarg2.absolutely == "anything"

Note that this sort of configuration doesn’t support defaults as there’s nowhere
to define them (if you want defaults, just declare your (data)classes with them).
Also note that you may combine the declared/free-form approaches (if it makes sense).

Finally, observe that the `Configurable.from_config` member function has `auto_obj`
parameter (with `False` default).
Setting that parameter to `True` allows you to omit the `type` specification
in your configuration.
In that case, the library will automatically treat all JSON objects in the config.
file as if the `confcls.Object` type was specified.

### Dot-path Syntax Access

`confcls.DotPath` allows `config["dot.path.to.attr"]` style access to configuration
objects hierarchy.
Each node on the (dot-separated) path represents object specification; be it by:
\* Attribute name
\* `dict` key
\* `list`, `tuple` or `string` index or slice
\* Regular expression matching attribute name or dict key

It is enough to derive the top-level config. object from `DotPath.Accessible`
and the following will be possible (note that `confcls.Configuration` is of course
derived from `DotPath.Accessible`):

    my_val = config["foo.bar.baz"]              # same as config.foo.bar.baz
    my_val = config["items.3.foo"]              # same as config.items[3].foo
    my_val = config.get("foo.bar")              # on key miss, None is returned
    my_val = config.get("foo.bar", 123)         # on key miss, the default is returned
    my_val = config.items("foo.bar.*")          # iterator of all config.foo.bar attributes
    my_val = config.items("foo.r'ba.*'.2:-2")   # config.foo.(all matching attrs).slice(2,-2)

1.  and so on…​

## Development

To develop `confcls`, you shall need make, pyenv and poetry installed.
Then, setup and initialise your development environment:

    $ make setup
    $ make init

To run mypy type checks, unit tests, and the linter use the `mypy`, `test` and `lint`
make targets, respectively.
Alternatively, use the `check` target to do all that.

    $ make check

The Python package is built by the `build` target.
The package may be published using the `publish` target.

    $ make build
    $ make publish

## Author

Václav Krpec &lt;<vencik@razdva.cz>&gt;
