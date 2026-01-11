package com.thirstysgame

import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithText
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Instrumented test for MainActivity.
 * 
 * Tests the main activity launches correctly and displays expected UI elements.
 */
@RunWith(AndroidJUnit4::class)
class MainActivityTest {
    
    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()
    
    @Test
    fun mainActivityLaunches() {
        // Verify that the app launches and the main content is displayed
        composeTestRule.waitForIdle()
        
        // Check for welcome text on home screen
        composeTestRule.onNodeWithText("Welcome to Thirsty's Game!", substring = true).assertExists()
    }
    
    @Test
    fun homeScreenDisplaysWelcomeCard() {
        composeTestRule.waitForIdle()
        
        // Verify welcome card is displayed
        composeTestRule.onNodeWithText("Welcome to Thirsty's Game!").assertExists()
        composeTestRule.onNodeWithText("A community-driven gaming experience", substring = true).assertExists()
    }
    
    @Test
    fun f2pBadgeIsDisplayed() {
        composeTestRule.waitForIdle()
        
        // Verify F2P badge is visible
        composeTestRule.onNodeWithText("100% F2P Friendly").assertExists()
        composeTestRule.onNodeWithText("No pay-to-win", substring = true).assertExists()
    }
}
