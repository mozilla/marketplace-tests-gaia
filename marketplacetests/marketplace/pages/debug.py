# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from marketplacetests.marketplace.pages.base import BasePage


class Debug(BasePage):

    _page_loaded_locator = (By.CSS_SELECTOR, 'section.debug')

    _region_select_locator = (By.ID, 'debug-region')
    _back_button_locator = (By.CSS_SELECTOR, 'mkt-nav-toggle button')

    def select_region(self, region):
        element = self.marionette.find_element(*self._region_select_locator)
        # This workaround is required for gaia v2.0, but can be removed in later versions
        # as the bug has been fixed
        # Bug 937053 - tap() method should calculate elementInView from the coordinates of the tap
        self.marionette.execute_script('arguments[0].scrollIntoView(false);', [element])
        element.tap()
        self.select(region)
        self.switch_to_marketplace_frame()

    def tap_back(self):
        back_button = self.marionette.find_element(*self._nav_menu_toggle_locator)
        # This workaround is required for gaia v2.0, but can be removed in later versions
        # as the bug has been fixed
        # Bug 937053 - tap() method should calculate elementInView from the coordinates of the tap
        self.marionette.execute_script('arguments[0].scrollIntoView(false);', [back_button])
        back_button.tap()
