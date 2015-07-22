# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace
from marketplacetests.payment.app import Payment


class TestMarketplaceCreateConfirmPin(MarketplaceGaiaTestCase):

    def test_create_confirm_pin(self):

        pin = '1234'
        account = self.create_firefox_account()

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        home_page.login(account.email, account.password)
        self.tap_install_button_of_first_paid_app()

        payment = Payment(self.marionette)
        payment.create_pin(pin)
        payment.wait_for_buy_app_section_displayed()
        self.assertIn(self.app_name, payment.app_name)
