package com.thirstysgame.data.repository

import android.util.Log
import com.google.gson.Gson
import com.thirstysgame.data.model.AppDataBundle
import com.thirstysgame.data.model.FeatureProposal
import com.thirstysgame.data.model.InsightsSummary
import com.thirstysgame.data.model.StorefrontItem
import com.thirstysgame.data.model.F2PPolicySummary
import com.thirstysgame.data.network.NetworkClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Repository for fetching and managing app data.
 * 
 * This repository handles loading data from the agent pipeline JSON artifacts,
 * either from a remote URL or from bundled assets.
 */
class AppDataRepository {
    
    private val apiService = NetworkClient.apiService
    private val gson = Gson()
    
    private var cachedData: AppDataBundle? = null
    
    companion object {
        private const val TAG = "AppDataRepository"
        
        // Default data URL - can be overridden
        private const val DEFAULT_DATA_URL = 
            "https://raw.githubusercontent.com/IAmSoThirsty/Thirstys_Game-Studio/main/output/app_data.json"
    }
    
    /**
     * Load app data from remote URL or use fallback.
     */
    suspend fun loadAppData(url: String = DEFAULT_DATA_URL): Result<AppDataBundle> {
        return withContext(Dispatchers.IO) {
            try {
                val response = apiService.getAppData(url)
                if (response.isSuccessful && response.body() != null) {
                    cachedData = response.body()
                    Result.success(cachedData!!)
                } else {
                    Log.w(TAG, "Failed to load remote data, using fallback")
                    Result.success(getFallbackData())
                }
            } catch (e: Exception) {
                Log.e(TAG, "Error loading app data: ${e.message}")
                // Return fallback data on error
                Result.success(getFallbackData())
            }
        }
    }
    
    /**
     * Get cached data or load if not available.
     */
    suspend fun getData(): AppDataBundle {
        return cachedData ?: loadAppData().getOrElse { getFallbackData() }
    }
    
    /**
     * Get proposals list.
     */
    suspend fun getProposals(): List<FeatureProposal> {
        return getData().proposals
    }
    
    /**
     * Get storefront items.
     */
    suspend fun getStorefrontItems(): List<StorefrontItem> {
        return getData().storefrontItems
    }
    
    /**
     * Get insights summary.
     */
    suspend fun getInsightsSummary(): InsightsSummary {
        return getData().insightsSummary
    }
    
    /**
     * Get F2P policy summary.
     */
    suspend fun getF2PPolicy(): F2PPolicySummary {
        return getData().f2pPolicySummary
    }
    
    /**
     * Fallback data when remote fetch fails.
     */
    private fun getFallbackData(): AppDataBundle {
        return AppDataBundle(
            version = "1.0.0",
            generatedAt = "2024-01-01T00:00:00Z",
            insightsSummary = InsightsSummary(
                totalCount = 15,
                avgSentiment = 0.72f,
                topTopics = listOf(
                    listOf("customization", 5),
                    listOf("cosmetics", 4),
                    listOf("social", 3)
                ),
                sources = listOf("reddit", "discord", "steam")
            ),
            proposals = listOf(
                FeatureProposal(
                    title = "Enhanced Character Customization",
                    description = "Add more cosmetic options for character personalization based on community feedback.",
                    sourceInsights = listOf(),
                    category = "customization",
                    monetizationType = "cosmetic",
                    priority = 0.85f,
                    f2pCompliant = true,
                    guardrailNotes = listOf(),
                    comparativeNotes = listOf("Inspired by community requests for more visual options"),
                    createdAt = "2024-01-01T00:00:00Z"
                ),
                FeatureProposal(
                    title = "Guild/Clan System",
                    description = "Implement social guild features for cooperative gameplay without pay-to-win elements.",
                    sourceInsights = listOf(),
                    category = "social",
                    monetizationType = "free",
                    priority = 0.80f,
                    f2pCompliant = true,
                    guardrailNotes = listOf(),
                    comparativeNotes = listOf("Social features drive engagement"),
                    createdAt = "2024-01-01T00:00:00Z"
                ),
                FeatureProposal(
                    title = "Seasonal Event System",
                    description = "Regular seasonal events with cosmetic rewards earnable through gameplay.",
                    sourceInsights = listOf(),
                    category = "events",
                    monetizationType = "cosmetic",
                    priority = 0.75f,
                    f2pCompliant = true,
                    guardrailNotes = listOf(),
                    comparativeNotes = listOf("Events keep the game fresh"),
                    createdAt = "2024-01-01T00:00:00Z"
                )
            ),
            f2pPolicySummary = F2PPolicySummary(
                corePrinciples = listOf(
                    "No pay-to-win mechanics",
                    "Cosmetic-only purchases",
                    "Fair progression for all",
                    "No predatory mechanics"
                ),
                whatWeOffer = listOf(
                    "Cosmetic items (skins, outfits, effects)",
                    "Quality of life features",
                    "Battle pass with cosmetic rewards"
                ),
                whatWeNeverDo = listOf(
                    "Sell gameplay advantages",
                    "Use loot boxes with valuable items",
                    "Create artificial time pressure"
                )
            ),
            storefrontItems = listOf(
                StorefrontItem(
                    id = "skin_001",
                    name = "Golden Knight Armor",
                    type = "cosmetic",
                    price = 500,
                    currency = "gems",
                    description = "A dazzling golden armor set. Purely cosmetic."
                ),
                StorefrontItem(
                    id = "emote_001",
                    name = "Victory Dance",
                    type = "emote",
                    price = 200,
                    currency = "gems",
                    description = "Celebrate your wins in style!"
                ),
                StorefrontItem(
                    id = "bundle_001",
                    name = "Starter Cosmetic Bundle",
                    type = "bundle",
                    price = 1000,
                    currency = "gems",
                    description = "3 skins + 2 emotes. Great value!"
                )
            )
        )
    }
}
