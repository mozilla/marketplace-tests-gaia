# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from fxapom.fxapom import FxATestAccount

from marketplacetests.payment.app import Payment
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace
from marketplacetests.firefox_accounts.app import FirefoxAccounts


class TestMarketplaceLoginDuringPurchase(MarketplaceGaiaTestCase):

    def test_login_during_purchase(self):

        pin = '1234'
        acct = FxATestAccount(base_url=self.base_url).create_account()

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        marketplace.launch()

        self.tap_install_button_of_first_paid_app()

        ff_accounts = FirefoxAccounts(self.marionette)
        ff_accounts.login(acct.email, acct.password)

        payment = Payment(self.marionette)
        payment.create_pin(pin)

        # Wait and check if confirm payment window appears
        payment.wait_for_buy_app_section_displayed()
        self.assertIn(self.app_name, payment.app_name)
