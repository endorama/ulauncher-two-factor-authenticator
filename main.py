from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction

import subprocess
import logging

logger = logging.getLogger()

generateCommand = "two-factor-authenticator generate %s --clip"
listCommand = "two-factor-authenticator list"

class TwoFactorAuthenticatorExtension(Extension):

    def __init__(self):
        super(TwoFactorAuthenticatorExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        logger.info("Initialized extension")

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        logger.info("Generating token for %s" % data)
        subprocess.Popen(generateCommand % data, shell=True)
        return HideWindowAction()

from ulauncher.util.fuzzy_search import get_score
from operator import itemgetter
class KeywordQueryEventListener(EventListener):
    def __init__(self):
        proc = subprocess.Popen(listCommand, shell=True, stdout=subprocess.PIPE)
        profile_list = proc.stdout.read()
        self.available_profiles = [x for x in profile_list.split("\n") if x != ""]
        logger.debug("Loaded 2fa profile list")

    def on_event(self, event, extension):
        items = []
        data = event.get_argument()
        available_profiles = [{'name': x, 'score': 0} for x in self.available_profiles]

        for d in available_profiles:
            d['score'] = get_score(data, d['name'])
        logger.debug(available_profiles)

        if data:
            available_profiles = sorted(available_profiles, key=itemgetter('score'),
                                            reverse=True)
            logger.debug(available_profiles)

            available_profiles = [x for x in available_profiles if x['score'] >= 50.0]
            logger.debug(available_profiles)

        for i in available_profiles:
            logger.info(i)
            items.append(ExtensionResultItem(icon='images/icon.png',
                                             name='%s' % i['name'],
                                             description='Generate token for %s' % i['name'],
                                             on_enter=ExtensionCustomAction(i['name'], keep_app_open=True)))

        return RenderResultListAction(items)

if __name__ == '__main__':
    TwoFactorAuthenticatorExtension().run()
