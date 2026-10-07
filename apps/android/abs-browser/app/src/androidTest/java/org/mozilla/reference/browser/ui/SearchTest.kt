/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

package org.projetoabsoluto.abs.browser.ui

import mockwebserver3.MockWebServer
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.projetoabsoluto.abs.browser.helpers.AndroidAssetDispatcher
import org.projetoabsoluto.abs.browser.helpers.BrowserActivityTestRule
import org.projetoabsoluto.abs.browser.helpers.RetryTestRule
import org.projetoabsoluto.abs.browser.helpers.TestAssetHelper
import org.projetoabsoluto.abs.browser.ui.robots.navigationToolbar

class SearchTest {
    private lateinit var mockWebServer: MockWebServer

    @get:Rule val activityTestRule = BrowserActivityTestRule()

    @Rule @JvmField val retryTestRule = RetryTestRule(3)

    @Before
    fun setUp() {
        mockWebServer =
            MockWebServer().apply {
                dispatcher = AndroidAssetDispatcher()
                start()
            }
    }

    @After
    fun tearDown() {
        runCatching { mockWebServer.close() }
    }

    @Test
    fun siteSearchSuggestionTest() {
        val defaultWebPage = TestAssetHelper.getGenericAsset(mockWebServer, 1)

        navigationToolbar {}.enterUrlAndEnterToBrowser(defaultWebPage.url) {}
        navigationToolbar {}
            .openTabTrayMenu {}
            .openNewTab {}
            .clickToolbar {
                typeText("generic1.html")
                verifySearchSuggestion(defaultWebPage.title)
            }
            .clickSearchSuggestion(defaultWebPage.title) {
                verifyUrl(defaultWebPage.url.toString())
            }
    }
}
