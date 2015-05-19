# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from marionette.by import By
from gaiatest.apps.base import PageRegion

from marketplacetests.marketplace.pages.base import BasePage


class SearchResults(BasePage):

    _page_loaded_locator = (By.CSS_SELECTOR, 'ul.app-list')

    _search_results_area_locator = (By.ID, 'search-results')
    _search_result_locator = (By.CSS_SELECTOR, '#search-results li.item')

    @property
    def search_results(self):
        self.wait_for_element_displayed(*self._search_result_locator)
        search_results = self.marionette.find_elements(*self._search_result_locator)
        return [Result(self.marionette, result) for result in search_results]


class Result(PageRegion):

    _name_locator = (By.CSS_SELECTOR, '.info > h3')
    _author_locator = (By.CSS_SELECTOR, '.info .author')
    _install_button_locator = (By.CSS_SELECTOR, '.button.mkt-app-button.install')

    @property
    def name(self):
        return self.root_element.find_element(*self._name_locator).text

    @property
    def author(self):
        return self.root_element.find_element(*self._author_locator).text

    @property
    def install_button_text(self):
        return self.root_element.find_element(*self._install_button_locator).text

    def tap_install_button(self):
        self.root_element.find_element(*self._install_button_locator).tap()

    def tap_app(self):
        app_name = self.root_element.find_element(*self._name_locator)
        app_name.tap()
        from marketplacetests.marketplace.pages.app_details import Details
        return Details(self.marionette)
