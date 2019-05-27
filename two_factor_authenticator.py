import os
from subprocess import Popen, PIPE

command = "two-factor-authenticator"
requiredVersion = "v0.3.0"

extDir = os.path.dirname(os.path.realpath(__file__))
localCommandPath = '{}/{}'.format(extDir, command)

downloadURL = "https://github.com/endorama/two-factor-authenticator/releases/download/%s/two-factor-authenticator-%s-linux-amd64" % (
    requiredVersion, requiredVersion)

generateCommand = localCommandPath + " generate %s --clip"
listCommand = localCommandPath + " list"
versionCommand = localCommandPath + " --version"


def generate(data):
    Popen(generateCommand % data, shell=True).decode("utf-8").rstrip("\r\n")


def list():
    proc = Popen(listCommand, shell=True,
                 stdout=PIPE)
    profile_list = proc.stdout.read().decode("utf-8").rstrip("\r\n")
    return profile_list


def version():
    proc = Popen(versionCommand, shell=True, stdout=PIPE)
    return proc.stdout.read().decode("utf-8").rstrip("\r\n")
