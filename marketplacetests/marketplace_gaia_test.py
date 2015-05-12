# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from gaiatest.gaia_test import GaiaTestCase
from marionette.by import By

from gaiatest.apps.homescreen.regions.confirm_install import ConfirmInstall
from gaiatest.apps.homescreen.app import Homescreen
from marketplacetests.marketplace.app import Marketplace


class MarketplaceGaiaTestCase(GaiaTestCase):

    _statusbar_downloads_icon_locator = (By.ID, 'statusbar-system-downloads')

    def setUp(self):
        GaiaTestCase.setUp(self)
        self.install_certs()
        self.connect_to_local_area_network()
        self.wait_for_element_not_displayed('id', 'os-logo')

        # Use this to override the Marketplace app version
        self.MARKETPLACE_DEV_NAME = 'Marketplace'

        # This is used to tell FxA whether to create a dev or prod account
        self.base_url = 'https://marketplace-dev.allizom.org'

    def install_in_app_payments_test_app(self, app_name):

        homescreen = Homescreen(self.marionette)

        # Remove the app if already installed
        if self.apps.is_app_installed(app_name):
            raise Exception('The app %s is already installed.' % app_name)

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()
        details_page = home_page.navigate_to_app(app_name)
        details_page.tap_install_button()
        self.wait_for_downloads_to_finish()

        # Confirm the installation and wait for the app icon to be present
        confirm_install = ConfirmInstall(self.marionette)
        confirm_install.tap_confirm()

        self.device.touch_home_button()
        self.apps.switch_to_displayed_app()
        homescreen.wait_for_app_icon_present(app_name)
        return homescreen

    @property
    def email(self):
        return self.acct.email

    @property
    def password(self):
        return self.acct.password

    def install_certs(self):
        """ Install the marketplace-dev certs and set the pref required """
        certs_folder = os.path.join('marketplacetests', 'certs')
        for file_name in self.device.manager.listFiles('/data/b2g/mozilla/'):
            if file_name.endswith('.default'):
                profile_folder = file_name
                break
        for file_name in os.listdir(certs_folder):
            self.device.push_file(os.path.join(certs_folder, file_name),
                                  destination='data/b2g/mozilla/%s/%s' % (profile_folder, file_name))
        self.data_layer.set_char_pref('dom.mozApps.signed_apps_installable_from',
                                      'https://marketplace-dev.allizom.org,https://marketplace.firefox.com')
        self.data_layer.set_bool_pref('dom.mozApps.use_reviewer_certs', True)

    def wait_for_downloads_to_finish(self):
        self.marionette.switch_to_frame()
        self.wait_for_element_not_displayed(*self._statusbar_downloads_icon_locator)
