# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette import By
from gaiatest.apps.base import Base


class Marketplace(Base):

    # Default to the Dev app
    name = 'Marketplace'

    _marketplace_frame_locator = (By.CSS_SELECTOR, 'iframe[src*="marketplace"]')
    _loading_fragment_locator = (By.CSS_SELECTOR, 'div.loading-fragment')
    _offline_message_locator = (By.CSS_SELECTOR, 'div.error-message[data-l10n="offline-error-message"]')

    def __init__(self, marionette, app_name=False):
        Base.__init__(self, marionette)
        if app_name:
            self.name = app_name
        self.manifest_url = "https://marketplace.firefox.com/app/965bbfd7-936d-451d-bebf-fafdc7ce8d9e/manifest.webapp"

    def launch(self, expect_success=True):
        Base.launch(self, launch_timeout=120000)
        self.wait_for_element_not_displayed(*self._loading_fragment_locator)
        if expect_success:
            self.switch_to_marketplace_frame()
            from marketplacetests.marketplace.pages.home import Home
            return Home(self.marionette)

    def switch_to_marketplace_frame(self):
        self.marionette.switch_to_frame()
        self.wait_for_element_present(*self._marketplace_frame_locator)
        marketplace_frame = self.marionette.find_element(*self._marketplace_frame_locator)
        self.marionette.switch_to_frame(marketplace_frame)
        self.wait_for_element_present(*self._marketplace_frame_locator)
        marketplace_frame = self.marionette.find_element(*self._marketplace_frame_locator)
        self.marionette.switch_to_frame(marketplace_frame)

    @property
    def offline_message_text(self):
        self.wait_for_element_displayed(*self._offline_message_locator)
        return self.marionette.find_element(*self._offline_message_locator).text
