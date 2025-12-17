package com.thirstysgame.ui.theme

import android.app.Activity
import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

// Game-themed colors
val GamePrimary = Color(0xFF6200EE)
val GameSecondary = Color(0xFF03DAC6)
val GameAccent = Color(0xFFFFD700)
val GameBackground = Color(0xFF121212)
val GameSurface = Color(0xFF1E1E1E)
val GameError = Color(0xFFCF6679)
val GameOnPrimary = Color.White
val GameOnSecondary = Color.Black
val GameOnBackground = Color.White
val GameOnSurface = Color.White
val GameOnError = Color.Black

// F2P-friendly green for compliant items
val F2PCompliant = Color(0xFF4CAF50)
val F2PWarning = Color(0xFFFFC107)

private val DarkColorScheme = darkColorScheme(
    primary = GamePrimary,
    secondary = GameSecondary,
    tertiary = GameAccent,
    background = GameBackground,
    surface = GameSurface,
    error = GameError,
    onPrimary = GameOnPrimary,
    onSecondary = GameOnSecondary,
    onBackground = GameOnBackground,
    onSurface = GameOnSurface,
    onError = GameOnError
)

private val LightColorScheme = lightColorScheme(
    primary = GamePrimary,
    secondary = GameSecondary,
    tertiary = GameAccent,
    background = Color(0xFFFFFBFE),
    surface = Color(0xFFFFFBFE),
    error = GameError,
    onPrimary = Color.White,
    onSecondary = Color.Black,
    onBackground = Color(0xFF1C1B1F),
    onSurface = Color(0xFF1C1B1F),
    onError = Color.Black
)

@Composable
fun ThirstysGameTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }
    
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = colorScheme.primary.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme
        }
    }

    MaterialTheme(
        colorScheme = colorScheme,
        content = content
    )
}
