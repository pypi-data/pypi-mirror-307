import importlib
import subprocess
import sys
import logging
import pkg_resources

logger = logging.getLogger(__name__)


def ensure_package(package_name, import_name=None, min_version=None):
    if import_name is None:
        import_name = package_name.split('-')[0]

    logger.debug(f"Ensuring package: {package_name}, import name: {import_name}, min version: {min_version}")

    try:
        logger.debug(f"Attempting to import {import_name}")
        module = importlib.import_module(import_name)
        if min_version:
            installed_version = pkg_resources.get_distribution(package_name).version
            logger.debug(f"Installed version: {installed_version}, required min version: {min_version}")
            if pkg_resources.parse_version(installed_version) < pkg_resources.parse_version(min_version):
                logger.info(f"Updating {package_name} to version {min_version}")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", f"{package_name}=={min_version}"])
                importlib.reload(module)
    except (ImportError, pkg_resources.DistributionNotFound) as e:
        logger.debug(f"Error occurred: {str(e)}")
        logger.info(f"Installing {package_name}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        module = importlib.import_module(import_name)

    logger.debug(f"Successfully imported {import_name}")
    return module
