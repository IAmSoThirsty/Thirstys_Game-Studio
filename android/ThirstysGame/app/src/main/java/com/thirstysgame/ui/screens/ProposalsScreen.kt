package com.thirstysgame.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.thirstysgame.data.model.FeatureProposal
import com.thirstysgame.ui.theme.F2PCompliant
import com.thirstysgame.ui.theme.F2PWarning
import com.thirstysgame.ui.viewmodel.MainViewModel

/**
 * Screen displaying feature proposals generated from community feedback.
 */
@Composable
fun ProposalsScreen(viewModel: MainViewModel) {
    val proposals by viewModel.proposals.collectAsState()
    
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp)
    ) {
        item {
            Text(
                text = "Feature Proposals",
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "Community-driven features based on player feedback",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.height(16.dp))
        }
        
        if (proposals.isEmpty()) {
            item {
                Card(
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(32.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "No proposals available yet",
                            style = MaterialTheme.typography.bodyLarge
                        )
                    }
                }
            }
        } else {
            items(proposals) { proposal ->
                ProposalCard(proposal = proposal)
            }
        }
    }
}

@Composable
private fun ProposalCard(proposal: FeatureProposal) {
    Card(
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            // Header with title and F2P status
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = proposal.title,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.weight(1f)
                )
                
                Spacer(modifier = Modifier.width(8.dp))
                
                // F2P compliance badge
                if (proposal.f2pCompliant) {
                    Icon(
                        Icons.Filled.CheckCircle,
                        contentDescription = "F2P Compliant",
                        tint = F2PCompliant,
                        modifier = Modifier.size(24.dp)
                    )
                } else {
                    Icon(
                        Icons.Filled.Warning,
                        contentDescription = "Needs Review",
                        tint = F2PWarning,
                        modifier = Modifier.size(24.dp)
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Description
            Text(
                text = proposal.description,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(12.dp))
            
            // Category and monetization chips
            Row(
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                AssistChip(
                    onClick = { },
                    label = { Text(proposal.category.replaceFirstChar { it.uppercase() }) }
                )
                
                AssistChip(
                    onClick = { },
                    label = { 
                        Text(
                            when (proposal.monetizationType) {
                                "cosmetic" -> "💎 Cosmetic"
                                "free" -> "🆓 Free"
                                "qol" -> "✨ QoL"
                                else -> proposal.monetizationType
                            }
                        )
                    }
                )
            }
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Priority bar
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "Priority:",
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Spacer(modifier = Modifier.width(8.dp))
                LinearProgressIndicator(
                    progress = { proposal.priority },
                    modifier = Modifier
                        .weight(1f)
                        .height(8.dp),
                    color = when {
                        proposal.priority >= 0.8f -> F2PCompliant
                        proposal.priority >= 0.5f -> MaterialTheme.colorScheme.primary
                        else -> MaterialTheme.colorScheme.tertiary
                    }
                )
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = "${(proposal.priority * 100).toInt()}%",
                    style = MaterialTheme.typography.labelMedium,
                    fontWeight = FontWeight.Bold
                )
            }
            
            // Comparative notes if any
            if (proposal.comparativeNotes.isNotEmpty()) {
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "💡 ${proposal.comparativeNotes.first()}",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.tertiary
                )
            }
        }
    }
}
