# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from marketplacetests.marketplace.pages.base import BasePage


class Details(BasePage):

    _page_loaded_locator = (By.CSS_SELECTOR, 'section.app-reviews')

    _write_review_locator = (By.CSS_SELECTOR, 'a.review-button')
    _app_info_locator = (By.CSS_SELECTOR, '.detail .info')
    _first_review_locator = (By.CSS_SELECTOR, '.reviews-wrapper li:first-child')
    _first_review_body_locator = (By.CSS_SELECTOR, '.reviews-wrapper .review-body')
    _install_button_locator = (By.CSS_SELECTOR, '.detail .info button.mkt-app-button.install')

    @property
    def is_app_details_displayed(self):
        return self.is_element_displayed(*self._app_info_locator)

    @property
    def install_button_text(self):
        self.wait_for_element_displayed(*self._install_button_locator)
        return self.marionette.find_element(*self._install_button_locator).text

    @property
    def first_review_body(self):
        return self.marionette.find_element(*self._first_review_body_locator).text

    @property
    def first_review_rating(self):
        return int(self.marionette.find_element(*self._first_review_locator).get_attribute('data-rating'))

    def tap_write_review(self, logged_in=True):
        self.wait_for_element_displayed(*self._write_review_locator)
        self.marionette.find_element(*self._write_review_locator).tap()
        if not logged_in:
            from marketplacetests.firefox_accounts.app import FirefoxAccounts
            return FirefoxAccounts(self.marionette)
        else:
            from marketplacetests.marketplace.pages.add_review import AddReview
            return AddReview(self.marionette)

    def tap_install_button(self):
        self.wait_for_element_displayed(*self._install_button_locator)
        self.marionette.find_element(*self._install_button_locator).tap()

    def wait_for_payment_cancelled_notification(self):
        self.wait_for_notification_message('Payment cancelled.')

    def wait_for_review_posted_notification(self):
        self.wait_for_notification_message('Your review was successfully posted. Thanks!')
