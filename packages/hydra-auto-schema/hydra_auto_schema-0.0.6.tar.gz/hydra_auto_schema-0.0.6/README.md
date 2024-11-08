# hydra-auto-schema

[![codecov](https://codecov.io/gh/lebrice/hydra-auto-schema/graph/badge.svg?token=13DH8R352T)](https://codecov.io/gh/lebrice/hydra-auto-schema)

This tool greatly improves the experience of developing a project with [Hydra](https://hydra.cc) by enabling rich IDE support for Hydra config files.

> 📢 If you are thinking of using Hydra for a PyTorch or Jax-based ML project, you might want to take a look at the [Research Project Template](https://github.com/mila-iqia/ResearchTemplate/) where this plugin was originally created. This is also where this plugin is best integrated!

With this, you'll now get to see:

- the list of available configuration options in a given config
- the default values for each entry
- the documentation associated with each entry (taken from the source code of the `_target_` callable!)
    Additionally
- A warning is displayed when a value is unexpected, or of the wrong type.

All-in-all, this helps to prevent errors, and gives your codebase the same kind of neatness and safety that type hints do.

## Demo

https://github.com/user-attachments/assets/08f52d47-ebba-456d-95ef-ac9525d8e983

## Installation

### Requirements

At the moment, we assume that you are using VSCode as your code editor. We use the yaml extension by RedHat, and install it for you if it isn't already. However any IDE with a YAML language server should be fairly easy to make work. Please make an issue if this doesn't work with your IDE.

### uv (recommended)

```console
uv add hydra-auto-schema
```

> Note: This plugin needs to be installed in your project's virtual environment. It should not be installed as an isolated tool using `uv tool`.
> This is because the plugin needs to import the modules where the `_target_`s are defined in order to inspect their signature.

### pip

```console
pip install hydra-auto-schema
```

### Usage (CLI)

Generate the yaml schemas for all the configs in the current folder:

```console
hydra-auto-schema
```

Watch for changes in the `configs` folder and update the schemas as needed:

```console
hydra-auto-schema configs --watch
```

### Usage (Hydra)

This package includes a Hydra plugin. By default, it will try to update all the schema files
in your project's config directory when Hydra's main function is called.

You don't really need to call anything for this to happen! Just keep using Hydra like you used to, and hopefully your config files will just feel much better to use! 😁

To configure how the auto schema plugin is called by Hydra, you can add the following block somwehere before your main Hydra function:

```python3
from hydra_plugins.auto_schema import auto_schema_plugin

auto_schema_plugin.config = auto_schema_plugin.AutoSchemaPluginConfig(
    schemas_dir=... # Path where you want the schema files to be saved. Defaults to ".schemas",
    regen_schemas=False,  # Whether to regenerate schemas even if the config did not change.
    stop_on_error=False,
    quiet=True,
    add_headers=False,  # controls whether to add headers, use vscode settings, or either.
)
```

## How to Contribute

This is a very new tool, and we'd love to get your feedback!
Please feel free to make an Issue if you have any questions or feedback. We'll be happy to assist you.
