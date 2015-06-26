# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from gaiatest.apps.browser.app import Browser

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestOpenWebsite(MarketplaceGaiaTestCase):

    def test_open_website(self):

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        new_apps = home_page.show_menu().tap_new()
        new_apps.select_content('websites')

        details_page = new_apps.app_list[0].tap_app()

        result_href = details_page.website_href
        details_page.tap_open_website_button()

        browser = Browser(self.marionette)
        browser.apps.switch_to_displayed_app()
        self.assertEqual(result_href, browser.url)
