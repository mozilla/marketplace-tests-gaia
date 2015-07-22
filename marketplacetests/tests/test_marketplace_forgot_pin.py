# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.firefox_accounts.app import FirefoxAccounts
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace
from marketplacetests.payment.app import Payment


class TestMarketplaceForgotPin(MarketplaceGaiaTestCase):

    def test_forgot_pin(self):

        old_pin = '1234'
        new_pin = '1111'
        account = self.create_firefox_account()

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()

        home_page.login(account.email, account.password)
        search_results_page = self.tap_install_button_of_first_paid_app()

        payment = Payment(self.marionette)
        payment.create_pin(old_pin)
        payment.wait_for_buy_app_section_displayed()
        self.assertIn(self.app_name, payment.app_name)
        payment.tap_cancel_button()

        search_results_page.wait_for_payment_cancelled_notification()
        search_results_page.search_results[0].tap_install_button()

        payment.switch_to_payment_frame()
        payment.tap_forgot_pin()
        payment.tap_reset_button()

        ff_accounts = FirefoxAccounts(self.marionette)
        ff_accounts.login(account.email, account.password)

        payment.switch_to_payment_frame()
        payment.enter_pin(new_pin)
        payment.confirm_pin(new_pin)

        payment.wait_for_buy_app_section_displayed()
        self.assertIn(self.app_name, payment.app_name)
