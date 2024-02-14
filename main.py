from operator import itemgetter
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.utils.fuzzy_search import get_score

import subprocess
import logging

logger = logging.getLogger()

twoFactorAuthenticatorCommand = "2ami"
generateCommand = twoFactorAuthenticatorCommand + " generate %s --clip"
listCommand = twoFactorAuthenticatorCommand + " list"


def which(program):
    import os

    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, _ = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def checkForCommand(command):
    commandFound = which(command)
    if commandFound:
        logger.debug("command found: %s" % commandFound)
        return True
    logger.error("%s command not found" % command)
    return False


class TwoFactorAuthenticatorExtension(Extension):

    def __init__(self):
        super(TwoFactorAuthenticatorExtension, self).__init__()
        if not checkForCommand(twoFactorAuthenticatorCommand):
            logger.warn(
                "two-factor-authenticator command not found or not executable, extension halted")
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        logger.info("Initialized extension")


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        logger.info("Generating token for %s" % data)
        subprocess.Popen(generateCommand % data, shell=True)
        return HideWindowAction()


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        if not checkForCommand(twoFactorAuthenticatorCommand):
            logger.warn(
                "two-factor-authenticator command not found or not executable, extension halted")
            return RenderResultListAction([ExtensionResultItem(
                icon=None, name='two-factor-autenticator command not found')])

        proc = subprocess.Popen(listCommand, shell=True,
                                stdout=subprocess.PIPE)
        profile_list = proc.stdout.read().decode("utf-8")
        available_profiles = [
            x for x in profile_list.split("\n") if x != ""]
        logger.debug("Loaded 2fa profile list")

        items = []
        data = event.get_argument()
        available_profiles = [{'name': x, 'score': 0}
                              for x in available_profiles]

        for d in available_profiles:
            d['score'] = get_score(data, d['name'])
        logger.debug(available_profiles)

        if data:
            available_profiles = sorted(available_profiles, key=itemgetter('score'),
                                        reverse=True)
            logger.debug(available_profiles)

            fuzzy_threshold = float(
                extension.preferences['2fa_fuzzy_threshold'])
            logger.debug(fuzzy_threshold)
            available_profiles = [
                x for x in available_profiles if x['score'] > fuzzy_threshold]
            logger.debug(available_profiles)

        if len(available_profiles) == 0:
            items.append(ExtensionResultItem(
                icon=None, name='No available items'))

        for i in available_profiles:
            logger.info(i)
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='%s' % i['name'],
                                             description='Generate token and copy to clipboard',
                                             on_enter=ExtensionCustomAction(i['name'], keep_app_open=True)))

        return RenderResultListAction(items)


if __name__ == '__main__':
    TwoFactorAuthenticatorExtension().run()
