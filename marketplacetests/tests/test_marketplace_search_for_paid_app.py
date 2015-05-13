# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestSearchMarketplacePaidApp(MarketplaceGaiaTestCase):

    def test_search_paid_app(self):

        app_name = 'Test Zippy With Me'
        if self.apps.is_app_installed(app_name):
            raise Exception('The app %s is already installed.' % app_name)

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        home_page.set_region('us')

        search_results = home_page.search(app_name).search_results

        self.assertGreater(len(search_results), 0, 'No results found.')

        for result in search_results:
            if result.name == app_name:
                saved_price = result.install_button_text
                details_page = result.tap_app()
                self.assertEqual(saved_price, details_page.install_button_text)
                return True

        # app not found
        self.fail('The app: %s was not found.' % app_name)
