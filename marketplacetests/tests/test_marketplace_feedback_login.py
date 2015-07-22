# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marketplacetests.marketplace_gaia_test import MarketplaceGaiaTestCase
from marketplacetests.marketplace.app import Marketplace


class TestMarketplaceFeedback(MarketplaceGaiaTestCase):

    def test_marketplace_feedback_user(self):
        test_comment = 'This is a test comment.'

        account = self.create_firefox_account()

        marketplace = Marketplace(self.marionette, self.MARKETPLACE_DEV_NAME)
        home_page = marketplace.launch()
        home_page.login(account.email, account.password)

        feedback = home_page.show_menu().tap_feedback()
        feedback.enter_feedback(test_comment)
        feedback.submit_feedback()

        feedback.wait_for_feedback_submitted_notification()
