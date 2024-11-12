# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

## Project-structure, Installing Dependencies and PYTHONPATH configuration.

This Project houses it's sources below the `src/{projectname}` directory. You have
to have this directory in your module-searchpath to execute the project. It should also
be present in the module-searchpath of your IDE.

If using pycharm or any other Jetbrains-based IDE, use 
`Settings->Project->Project Structure`
to `mark as sourcefolder` the `src`-folder of this.

The Project requirements, as well as the dev-requirements are intended to be listed in the 
`pyproject.toml`-file (see there)

By issuing:

```shell
pip install -e .
```

you add all the project dependencies as well as the projects sourcefolder to your 
[hopefully virtual!] environment, relieving you of the burden of having to manually 
installing anything or having to configure your python path by other means.

Likewise you can install all the dev-dependencies by:

```shell
pip install -e .'[dev]'
```

