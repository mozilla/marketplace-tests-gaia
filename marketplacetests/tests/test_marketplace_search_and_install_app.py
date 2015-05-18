# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.homescreen.app import Homescreen
from gaiatest.apps.homescreen.regions.confirm_install import ConfirmInstall

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestSearchMarketplaceAndInstallApp(MarketplaceGaiaTestCase):

    def test_search_and_install_app(self):

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        # Find a free app to install
        results = home_page.search(':free').search_results
        app = results[0]
        self.app_name = app.name
        app_author = app.author

        if self.apps.is_app_installed(self.app_name):
            raise Exception('The app %s is already installed.' % self.app_name)

        marketplace.switch_to_marketplace_frame()

        results_page = home_page.search(self.app_name)
        results = results_page.search_results

        self.assertGreater(len(results), 0, 'No results found.')

        first_result = results[0]

        self.assertEquals(first_result.name, self.app_name, 'First app has the wrong name.')
        self.assertEquals(first_result.author, app_author, 'First app has the wrong author.')

        # Find and click the install button to the install the web app
        self.assertEquals(first_result.install_button_text, 'Install for free', 'Incorrect button label.')

        first_result.tap_install_button()
        self.wait_for_downloads_to_finish()

        # Confirm the installation and wait for the app icon to be present
        confirm_install = ConfirmInstall(self.marionette)
        confirm_install.tap_confirm()

        self.assertEqual('%s installed' % self.app_name, results_page.install_notification_message)

        # Press Home button
        self.device.touch_home_button()

        # Check that the icon of the app is on the homescreen
        homescreen = Homescreen(self.marionette)
        self.apps.switch_to_displayed_app()

        self.assertTrue(homescreen.is_app_installed(self.app_name))

    def tearDown(self):
        self.apps.uninstall(self.app_name)
        MarketplaceGaiaTestCase.tearDown(self)
