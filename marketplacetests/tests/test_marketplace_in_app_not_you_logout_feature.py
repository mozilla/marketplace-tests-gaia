# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import Wait

from marketplacetests.payment.app import InAppPayment
from marketplacetests.in_app_payments.in_app import InAppPaymentTester
from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase


class TestNotYouLogoutFromInAppPayment(MarketplaceGaiaTestCase):

    test_data = {
        'app_name': 'Testing In-App-Payments',
        'app_title': 'In-App-Payments',
        'product': 'test 0.99 USD'}

    def test_not_you_logout_from_in_app_payment(self):

        account = self.create_firefox_account()
        homescreen = self.install_in_app_payments_test_app(self.test_data['app_name'])

        # Verify that the app icon is visible on one of the homescreen pages
        self.assertTrue(
            homescreen.is_app_installed(self.test_data['app_name']),
            'App %s not found on homescreen' % self.test_data['app_name'])

        self.tester_app = InAppPaymentTester(self.marionette, self.test_data['app_name'])
        self.tester_app.launch()
        Wait(self.marionette).until(lambda m: m.title == self.test_data['app_title'])

        fxa = self.tester_app.tap_buy_product(self.test_data['product'])
        fxa.login(account.email, account.password)

        payment = InAppPayment(self.marionette)
        payment.tap_cancel_pin()

        fxa = self.tester_app.tap_buy_product(self.test_data['product'])
        self.assertTrue(fxa.is_not_you_logout_link_visible)
        self.assertEqual('You are signed in as: %s' % account.email, 'You are signed in as: %s' % fxa.email_text)

        fxa.tap_not_you()
        fxa.wait_for_password_field_visible()

    def tearDown(self):
        self.apps.uninstall(self.test_data['app_name'])
        MarketplaceGaiaTestCase.tearDown(self)
