package com.thirstysgame.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Diamond
import androidx.compose.material.icons.filled.EmojiEmotions
import androidx.compose.material.icons.filled.Inventory
import androidx.compose.material.icons.filled.ShoppingBag
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.thirstysgame.data.model.StorefrontItem
import com.thirstysgame.ui.theme.F2PCompliant
import com.thirstysgame.ui.theme.GameAccent
import com.thirstysgame.ui.viewmodel.MainViewModel

/**
 * Storefront screen showing cosmetic items for purchase.
 * All items are purely cosmetic with no gameplay advantages.
 */
@Composable
fun StorefrontScreen(viewModel: MainViewModel) {
    val storefrontItems by viewModel.storefrontItems.collectAsState()
    
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            Text(
                text = "Cosmetic Store",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(4.dp))
            CosmeticOnlyBanner()
            Spacer(modifier = Modifier.height(16.dp))
        }
        
        items(storefrontItems) { item ->
            StorefrontItemCard(item = item)
        }
        
        item {
            Spacer(modifier = Modifier.height(8.dp))
            DisclaimerCard()
        }
    }
}

@Composable
private fun CosmeticOnlyBanner() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = F2PCompliant.copy(alpha = 0.15f)
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(
                Icons.Filled.ShoppingBag,
                contentDescription = null,
                tint = F2PCompliant
            )
            Spacer(modifier = Modifier.width(12.dp))
            Column {
                Text(
                    text = "Cosmetics Only - No Pay-to-Win!",
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.Bold,
                    color = F2PCompliant
                )
                Text(
                    text = "All purchases are purely visual. No gameplay advantages.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}

@Composable
private fun StorefrontItemCard(item: StorefrontItem) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Item icon based on type
            Box(
                modifier = Modifier
                    .size(64.dp),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    getItemIcon(item.type),
                    contentDescription = null,
                    modifier = Modifier.size(40.dp),
                    tint = when (item.type) {
                        "cosmetic" -> GameAccent
                        "emote" -> MaterialTheme.colorScheme.tertiary
                        "bundle" -> MaterialTheme.colorScheme.primary
                        else -> MaterialTheme.colorScheme.secondary
                    }
                )
            }
            
            Spacer(modifier = Modifier.width(16.dp))
            
            // Item details
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = item.name,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    text = item.description,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.height(4.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Icon(
                        Icons.Filled.Diamond,
                        contentDescription = null,
                        modifier = Modifier.size(16.dp),
                        tint = GameAccent
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = "${item.price}",
                        style = MaterialTheme.typography.titleSmall,
                        fontWeight = FontWeight.Bold,
                        color = GameAccent
                    )
                }
            }
            
            // Purchase button
            FilledTonalButton(
                onClick = { /* Purchase action */ },
                modifier = Modifier.padding(start = 8.dp)
            ) {
                Text("Buy")
            }
        }
    }
}

private fun getItemIcon(type: String): ImageVector {
    return when (type) {
        "cosmetic" -> Icons.Filled.Diamond
        "emote" -> Icons.Filled.EmojiEmotions
        "bundle" -> Icons.Filled.Inventory
        else -> Icons.Filled.ShoppingBag
    }
}

@Composable
private fun DisclaimerCard() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        )
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "Our Promise",
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "• All items are purely cosmetic\n" +
                       "• No stat boosts or gameplay advantages\n" +
                       "• No loot boxes or hidden odds\n" +
                       "• Fair prices, no manipulation",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
