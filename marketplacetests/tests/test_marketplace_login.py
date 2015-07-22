# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceLogin(MarketplaceGaiaTestCase):

    def test_login_marketplace(self):
        # https://moztrap.mozilla.org/manage/case/4134/
        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        account = self.create_firefox_account()

        home_page.login(account.email, account.password)

        # switch back to Marketplace
        marketplace.switch_to_marketplace_frame()

        # wait for the expected notification, and for user to be signed in
        home_page.wait_for_login_success_notification()
        settings = home_page.show_menu().tap_settings()
        settings.wait_for_sign_out_button()

        # Verify that user is logged in
        self.assertEqual(account.email, settings.email)

        # Sign out, which should return to the Marketplace home screen
        settings.tap_sign_out()

        # Verify that user is signed out
        settings.wait_for_sign_in_displayed()
