package com.thirstysgame

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.thirstysgame.navigation.ThirstysGameNavigation
import com.thirstysgame.ui.theme.ThirstysGameTheme

/**
 * Main entry point for Thirsty's Game.
 * 
 * This activity hosts the Compose navigation and UI for the game's
 * community features, proposals, and cosmetic storefront.
 */
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            ThirstysGameTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    ThirstysGameNavigation()
                }
            }
        }
    }
}
