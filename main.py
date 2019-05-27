import gi
gi.require_version('Gtk', '3.0')

import cli_dep
import two_factor_authenticator

from ulauncher.utils.fuzzy_search import get_score
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from operator import itemgetter

import logging

logger = logging.getLogger()


class TwoFactorAuthenticatorExtension(Extension):

    def __init__(self):
        super(TwoFactorAuthenticatorExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())
        cli_dep.ensure()
        logger.info("Initialized extension")


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        data = event.get_data()
        logger.info("Generating token for %s" % data)
        two_factor_authenticator.generate(data)
        return HideWindowAction()


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        profile_list = two_factor_authenticator.list()
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
