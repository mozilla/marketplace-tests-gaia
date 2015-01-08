# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from fxapom.fxapom import FxATestAccount

from marketplacetests.payment.app import Payment
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceLoginDuringPurchase(MarketplaceGaiaTestCase):

    def test_login_during_purchase(self):

        APP_NAME = 'Test Zippy With Me'
        PIN = '1234'
        acct = FxATestAccount(use_prod=False).create_account()

        if self.apps.is_app_installed(APP_NAME):
            self.apps.uninstall(APP_NAME)

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        marketplace.launch()

        marketplace.set_region('United States')

        details_page = marketplace.navigate_to_app(APP_NAME)
        ff_accounts = details_page.tap_purchase_button(is_logged_in=False)
        ff_accounts.login(acct.email, acct.password)

        payment = Payment(self.marionette)
        payment.create_pin(PIN)

        # Wait and check if confirm payment window appears
        payment.wait_for_buy_app_section_displayed()
        self.assertIn(APP_NAME, payment.app_name)
