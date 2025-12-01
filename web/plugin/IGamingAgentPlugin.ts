/**
 * IGamingAgentPlugin.ts
 * 
 * Cross-language interface for integrating with the Gaming Agent system.
 * This TypeScript module provides interfaces for web-based games and
 * JavaScript/TypeScript game engines to interact with the agent platform.
 * 
 * Copyright (c) 2024 Thirsty's Game Studio
 */

/**
 * Represents a community insight from various sources
 */
export interface CommunityInsight {
    source: string;
    content: string;
    sentiment: number;
    topics: string[];
    author: string;
    timestamp: Date;
    engagement: Record<string, number>;
    category: string;
    priority: number;
}

/**
 * Represents a feature proposal derived from community insights
 */
export interface FeatureProposal {
    title: string;
    description: string;
    sourceInsights: string[];
    category: string;
    monetizationType: string;
    priority: number;
    f2pCompliant: boolean;
    guardrailNotes: string[];
    comparativeNotes: string[];
    createdAt: Date;
}

/**
 * Monetization guardrail types for F2P compliance
 */
export enum MonetizationGuardrail {
    NoPayToWin = 'no_pay_to_win',
    CosmeticOnly = 'cosmetic_only',
    NoGameplayAdvantage = 'no_gameplay_advantage',
    FairProgression = 'fair_progression',
    TransparentOdds = 'transparent_odds',
    NoLootBoxes = 'no_loot_boxes',
    AccessibleContent = 'accessible_content'
}

/**
 * Result of a guardrail check
 */
export interface GuardrailResult {
    passed: boolean;
    guardrail: MonetizationGuardrail;
    message: string;
    suggestions: string[];
}

/**
 * Result of running the agent pipeline
 */
export interface AgentPipelineResult {
    success: boolean;
    timestamp: Date;
    totalInsights: number;
    totalProposals: number;
    compliantProposals: number;
    executionTimeSeconds: number;
    insights: CommunityInsight[];
    proposals: FeatureProposal[];
    errorMessage?: string;
}

/**
 * Configuration for the plugin
 */
export interface PluginConfiguration {
    redditClientId?: string;
    redditClientSecret?: string;
    discordBotToken?: string;
    discordGuildId?: string;
    steamApiKey?: string;
    steamAppId?: string;
    outputDirectory?: string;
    logLevel?: 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR';
    apiBaseUrl?: string;
}

/**
 * Summary of community insights
 */
export interface InsightsSummary {
    totalCount: number;
    avgSentiment: number;
    topTopics: [string, number][];
    sources: string[];
}

/**
 * F2P policy summary for display
 */
export interface F2PPolicySummary {
    corePrinciples: string[];
    whatWeOffer: string[];
    whatWeNeverDo: string[];
}

/**
 * Storefront item for cosmetic purchases
 */
export interface StorefrontItem {
    id: string;
    name: string;
    type: 'cosmetic' | 'emote' | 'bundle' | 'battle_pass';
    price: number;
    currency: string;
    description: string;
}

/**
 * App data bundle from agent pipeline
 */
export interface AppDataBundle {
    version: string;
    generatedAt: Date;
    insightsSummary: InsightsSummary;
    proposals: FeatureProposal[];
    f2pPolicySummary: F2PPolicySummary;
    storefrontItems: StorefrontItem[];
}

/**
 * Event types emitted by the plugin
 */
export type PluginEventType = 
    | 'initialized'
    | 'insights_fetched'
    | 'proposals_generated'
    | 'pipeline_complete'
    | 'error';

/**
 * Event payload type map
 */
export interface PluginEventPayloads {
    initialized: { success: boolean };
    insights_fetched: { insights: CommunityInsight[] };
    proposals_generated: { proposals: FeatureProposal[] };
    pipeline_complete: { result: AgentPipelineResult };
    error: { message: string; code?: string };
}

/**
 * Event listener callback type
 */
export type PluginEventListener<T extends PluginEventType> = (
    payload: PluginEventPayloads[T]
) => void;

/**
 * Main interface for the Gaming Agent Plugin
 * 
 * Implement this interface to integrate the agent system with your web game.
 */
export interface IGamingAgentPlugin {
    /**
     * Get the plugin version
     */
    readonly version: string;

    /**
     * Check if the plugin is properly initialized
     */
    readonly isInitialized: boolean;

    /**
     * Initialize the plugin with configuration
     */
    initialize(config: PluginConfiguration): Promise<boolean>;

    /**
     * Fetch community insights from configured sources
     */
    fetchInsights(limit?: number): Promise<CommunityInsight[]>;

    /**
     * Generate feature proposals from insights
     */
    generateProposals(insights: CommunityInsight[]): Promise<FeatureProposal[]>;

    /**
     * Validate proposals against monetization guardrails
     */
    validateProposals(proposals: FeatureProposal[]): Promise<Map<FeatureProposal, GuardrailResult[]>>;

    /**
     * Get the F2P policy document
     */
    getF2PPolicy(): string;

    /**
     * Get the F2P policy summary
     */
    getF2PPolicySummary(): F2PPolicySummary;

    /**
     * Run the complete agent pipeline
     */
    runPipeline(): Promise<AgentPipelineResult>;

    /**
     * Load app data from JSON artifact
     */
    loadAppData(url: string): Promise<AppDataBundle>;

    /**
     * Get storefront items (cosmetic only)
     */
    getStorefrontItems(): Promise<StorefrontItem[]>;

    /**
     * Add event listener
     */
    addEventListener<T extends PluginEventType>(
        event: T,
        listener: PluginEventListener<T>
    ): void;

    /**
     * Remove event listener
     */
    removeEventListener<T extends PluginEventType>(
        event: T,
        listener: PluginEventListener<T>
    ): void;

    /**
     * Shutdown the plugin and release resources
     */
    shutdown(): Promise<void>;
}

/**
 * Default F2P policy document
 */
export const F2P_POLICY = `
# Thirsty's Game Studio F2P Policy

We believe games should be fun for everyone, regardless of how much they spend.
Our monetization philosophy is built on these core principles:

## ✅ What We DO Offer

### Cosmetic Items
- Character skins and outfits
- Weapon skins and visual effects
- Emotes and animations
- Profile customization (banners, borders, titles)
- Visual-only pets and companions

### Quality of Life Features
- Additional cosmetic loadout slots
- Extended profile customization options
- Social features and emotes

### Battle Pass (Seasonal)
- Purely cosmetic rewards
- All gameplay-relevant content available for free
- Reasonable progression achievable through normal play

## ❌ What We NEVER Do

### No Pay-to-Win
- No stat boosts or gameplay advantages for purchase
- No exclusive weapons or abilities behind paywalls
- No faster progression through purchases

### No Predatory Mechanics
- No loot boxes with random valuable items
- No hidden odds or manipulative pricing
- No artificial time-gates that can be skipped with money

### No FOMO Tactics
- No countdown timers on purchase decisions
- Seasonal items return in future seasons
- No pressure sales or manipulation

## Our Commitment

Every player, free or paying, has the same gameplay experience.
Paying supports development and gets you cool cosmetics - nothing more.
`;

/**
 * Factory function type for creating plugin instances
 */
export type PluginFactory = () => IGamingAgentPlugin;

/**
 * Default configuration loader from environment
 */
export function loadConfigFromEnv(): PluginConfiguration {
    if (typeof process === 'undefined') {
        // Browser environment
        return {
            apiBaseUrl: '/api/agent',
            outputDirectory: 'output',
            logLevel: 'INFO'
        };
    }

    // Node.js environment
    return {
        redditClientId: process.env.REDDIT_CLIENT_ID,
        redditClientSecret: process.env.REDDIT_CLIENT_SECRET,
        discordBotToken: process.env.DISCORD_BOT_TOKEN,
        discordGuildId: process.env.DISCORD_GUILD_ID,
        steamApiKey: process.env.STEAM_API_KEY,
        steamAppId: process.env.STEAM_APP_ID,
        outputDirectory: process.env.OUTPUT_DIR || 'output',
        logLevel: (process.env.LOG_LEVEL as PluginConfiguration['logLevel']) || 'INFO'
    };
}
