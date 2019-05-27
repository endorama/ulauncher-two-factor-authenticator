import os
import logging
import urllib.request, urllib.parse, urllib.error

from two_factor_authenticator import command, version, requiredVersion, downloadURL, localCommandPath

logger = logging.getLogger("cli_dep")


def download():
    logger.debug(downloadURL)

    result = urllib.request.urlretrieve(downloadURL, localCommandPath)

    if "status" in list(result[1].keys()) and not "200" in result[1]['Status']:
        logger.error("command download failed")
        os.remove(command)
        raise Exception(
            "Command download failed. The command does not exist and it's download failed")


def checkVersion():
    v = version()
    rv = requiredVersion
    logger.info("cli version: %s" % v)
    logger.info("required version: %s" % rv)


def ensure():
    if not os.path.isfile(localCommandPath):
        logger.debug("downloading cli")
        download()

    logger.debug("local cli installed")

    if not os.access(localCommandPath, os.X_OK):
        logger.debug("setting command executable permissions")
        os.chmod(localCommandPath, 0o755)

    checkVersion()
