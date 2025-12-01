package com.thirstysgame.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Insights
import androidx.compose.material.icons.filled.Policy
import androidx.compose.material.icons.filled.ShoppingCart
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.thirstysgame.ui.screens.F2PPolicyScreen
import com.thirstysgame.ui.screens.HomeScreen
import com.thirstysgame.ui.screens.ProposalsScreen
import com.thirstysgame.ui.screens.StorefrontScreen
import com.thirstysgame.ui.viewmodel.MainViewModel

/**
 * Navigation destinations for the app.
 */
sealed class Screen(val route: String, val title: String, val icon: ImageVector) {
    object Home : Screen("home", "Home", Icons.Filled.Home)
    object Proposals : Screen("proposals", "Proposals", Icons.Filled.Insights)
    object Storefront : Screen("storefront", "Store", Icons.Filled.ShoppingCart)
    object F2PPolicy : Screen("f2p_policy", "F2P Policy", Icons.Filled.Policy)
}

val bottomNavItems = listOf(
    Screen.Home,
    Screen.Proposals,
    Screen.Storefront,
    Screen.F2PPolicy
)

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ThirstysGameNavigation() {
    val navController = rememberNavController()
    val viewModel: MainViewModel = viewModel()
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Thirsty's Game") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        },
        bottomBar = {
            NavigationBar {
                val navBackStackEntry by navController.currentBackStackEntryAsState()
                val currentDestination = navBackStackEntry?.destination
                
                bottomNavItems.forEach { screen ->
                    NavigationBarItem(
                        icon = { Icon(screen.icon, contentDescription = screen.title) },
                        label = { Text(screen.title) },
                        selected = currentDestination?.hierarchy?.any { it.route == screen.route } == true,
                        onClick = {
                            navController.navigate(screen.route) {
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    )
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Home.route,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(Screen.Home.route) {
                HomeScreen(viewModel = viewModel)
            }
            composable(Screen.Proposals.route) {
                ProposalsScreen(viewModel = viewModel)
            }
            composable(Screen.Storefront.route) {
                StorefrontScreen(viewModel = viewModel)
            }
            composable(Screen.F2PPolicy.route) {
                F2PPolicyScreen(viewModel = viewModel)
            }
        }
    }
}
