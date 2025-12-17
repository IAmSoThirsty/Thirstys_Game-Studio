package com.thirstysgame.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Block
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Shield
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.thirstysgame.data.model.F2PPolicySummary
import com.thirstysgame.ui.theme.F2PCompliant
import com.thirstysgame.ui.viewmodel.MainViewModel

/**
 * Screen displaying the F2P (Free-to-Play) policy and commitments.
 */
@Composable
fun F2PPolicyScreen(viewModel: MainViewModel) {
    val f2pPolicy by viewModel.f2pPolicy.collectAsState()
    
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            PolicyHeader()
        }
        
        f2pPolicy?.let { policy ->
            item {
                PolicySection(
                    title = "Our Core Principles",
                    icon = Icons.Filled.Shield,
                    items = policy.corePrinciples,
                    iconColor = F2PCompliant
                )
            }
            
            item {
                PolicySection(
                    title = "What We Offer",
                    icon = Icons.Filled.Check,
                    items = policy.whatWeOffer,
                    iconColor = MaterialTheme.colorScheme.primary
                )
            }
            
            item {
                PolicySection(
                    title = "What We Never Do",
                    icon = Icons.Filled.Block,
                    items = policy.whatWeNeverDo,
                    iconColor = MaterialTheme.colorScheme.error
                )
            }
        }
        
        item {
            CommitmentCard()
        }
    }
}

@Composable
private fun PolicyHeader() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer
        )
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Icon(
                Icons.Filled.Favorite,
                contentDescription = null,
                modifier = Modifier.size(48.dp),
                tint = F2PCompliant
            )
            Spacer(modifier = Modifier.height(12.dp))
            Text(
                text = "Our F2P Promise",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold,
                color = MaterialTheme.colorScheme.onPrimaryContainer
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "We believe games should be fun for everyone, " +
                       "regardless of how much they spend.",
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onPrimaryContainer,
                modifier = Modifier.fillMaxWidth()
            )
        }
    }
}

@Composable
private fun PolicySection(
    title: String,
    icon: ImageVector,
    items: List<String>,
    iconColor: androidx.compose.ui.graphics.Color
) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(
                    icon,
                    contentDescription = null,
                    tint = iconColor
                )
                Spacer(modifier = Modifier.width(12.dp))
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold
                )
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            
            items.forEach { item ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 6.dp),
                    verticalAlignment = Alignment.Top
                ) {
                    Icon(
                        Icons.Filled.Check,
                        contentDescription = null,
                        modifier = Modifier.size(20.dp),
                        tint = iconColor
                    )
                    Spacer(modifier = Modifier.width(12.dp))
                    Text(
                        text = item,
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            }
        }
    }
}

@Composable
private fun CommitmentCard() {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = F2PCompliant.copy(alpha = 0.1f)
        )
    ) {
        Column(
            modifier = Modifier.padding(20.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(
                text = "Our Commitment",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = F2PCompliant
            )
            Spacer(modifier = Modifier.height(12.dp))
            Text(
                text = "Every player, free or paying, has the same gameplay experience. " +
                       "Paying supports development and gets you cool cosmetics - nothing more.",
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(16.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center
            ) {
                AssistChip(
                    onClick = { },
                    label = { Text("Fair Play") }
                )
                Spacer(modifier = Modifier.width(8.dp))
                AssistChip(
                    onClick = { },
                    label = { Text("No P2W") }
                )
                Spacer(modifier = Modifier.width(8.dp))
                AssistChip(
                    onClick = { },
                    label = { Text("Community First") }
                )
            }
        }
    }
}
