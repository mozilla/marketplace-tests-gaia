# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By

from marketplacetests.marketplace.pages.search_results import Result, SearchResults


class NewAppsPage(SearchResults):

    _content_select_locator = (By.CSS_SELECTOR, 'mkt-select.content-filter')
    _content_options_locator = (By.TAG_NAME, 'mkt-option')

    _app_locator = (By.CSS_SELECTOR, 'ul.app-list li')

    @property
    def app_list(self):
        self.wait_for_element_displayed(*self._app_locator)
        apps = self.marionette.find_elements(*self._app_locator)
        return [Result(self.marionette, app) for app in apps]

    def select_content(self, content_type):
        self.marionette.find_element(*self._content_select_locator).click()
        options = self.marionette.find_elements(*self._content_options_locator)
        for option in options:
            if option.text == content_type:
                option.click()
                return
        raise Exception('The content type %s cannot be found.' % content_type)
