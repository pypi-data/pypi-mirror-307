import site
import subprocess
import sys
from typing import Optional

from ..utils import logging
from .discovery import loader_list, plugins_package_names, viewer_list

print = logging.invalidPrint
logger = logging.getLogger()


def reset_plugins():
    module_to_delete = []

    for module in sys.modules:
        for plugin_package_name in plugins_package_names:
            if module.startswith(plugin_package_name):
                module_to_delete.append(module)

    for module in module_to_delete:
        del sys.modules[module]

    plugins_package_names.reset()
    site.main()  # Update sys.path for plugins installed in editable mode
    loader_list.reset()
    viewer_list.reset()
    logger.debug("Plugins reset")


def install_plugin(plugin_url: str, index_url: Optional[str] = None, editable: bool = False):
    logger.debug(f"Installing plugin {plugin_url}{f' from {index_url}' if index_url else ''}")

    command = [
        "pip",
        "install",
    ]

    if index_url:
        command.extend(["--index-url", index_url])

    if editable:
        command.append("-e")

    command.append(plugin_url)

    try:
        logger.debug(f"Running command: {' '.join(command)}")
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.debug(f"Plugin {plugin_url} installed successfully")
        reset_plugins()

    except subprocess.CalledProcessError as e:
        message = f"Error installing plugin {plugin_url}"
        if e.stderr:
            message += f"\n{e.stderr.decode()}"

        raise RuntimeError(message) from e


def remove_plugin(package_name: str):
    logger.debug(f"Removing plugin {package_name}")

    command = [
        "pip",
        "uninstall",
        "-y",
        package_name,
    ]

    try:
        logger.debug(f"Running command: {' '.join(command)}")
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        logger.debug(f"Plugin {package_name} removed successfully")
        reset_plugins()

    except subprocess.CalledProcessError as e:
        message = f"Error removing plugin {package_name}"
        if e.stderr:
            message += f"\n{e.stderr.decode()}"

        raise RuntimeError(message) from e
