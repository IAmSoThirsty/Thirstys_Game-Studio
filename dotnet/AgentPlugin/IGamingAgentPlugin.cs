// IGamingAgentPlugin.cs
// Cross-language interface for integrating with the Gaming Agent system
// This interface allows .NET/C# game engines to interact with the agent platform

using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace AgentPlugin
{
    /// <summary>
    /// Represents a community insight from various sources
    /// </summary>
    public class CommunityInsight
    {
        public string Source { get; set; }
        public string Content { get; set; }
        public float Sentiment { get; set; }
        public List<string> Topics { get; set; }
        public string Author { get; set; }
        public DateTime Timestamp { get; set; }
        public Dictionary<string, int> Engagement { get; set; }
        public string Category { get; set; }
        public float Priority { get; set; }

        public CommunityInsight()
        {
            Topics = new List<string>();
            Engagement = new Dictionary<string, int>();
        }
    }

    /// <summary>
    /// Represents a feature proposal derived from community insights
    /// </summary>
    public class FeatureProposal
    {
        public string Title { get; set; }
        public string Description { get; set; }
        public List<string> SourceInsights { get; set; }
        public string Category { get; set; }
        public string MonetizationType { get; set; }
        public float Priority { get; set; }
        public bool F2PCompliant { get; set; }
        public List<string> GuardrailNotes { get; set; }
        public List<string> ComparativeNotes { get; set; }
        public DateTime CreatedAt { get; set; }

        public FeatureProposal()
        {
            SourceInsights = new List<string>();
            GuardrailNotes = new List<string>();
            ComparativeNotes = new List<string>();
        }
    }

    /// <summary>
    /// Monetization guardrail types for F2P compliance
    /// </summary>
    public enum MonetizationGuardrail
    {
        NoPayToWin,
        CosmeticOnly,
        NoGameplayAdvantage,
        FairProgression,
        TransparentOdds,
        NoLootBoxes,
        AccessibleContent
    }

    /// <summary>
    /// Result of a guardrail check
    /// </summary>
    public class GuardrailResult
    {
        public bool Passed { get; set; }
        public MonetizationGuardrail Guardrail { get; set; }
        public string Message { get; set; }
        public List<string> Suggestions { get; set; }

        public GuardrailResult()
        {
            Suggestions = new List<string>();
        }
    }

    /// <summary>
    /// Main interface for the Gaming Agent Plugin
    /// Implement this interface to integrate the agent system with your game
    /// </summary>
    public interface IGamingAgentPlugin
    {
        /// <summary>
        /// Gets the plugin version
        /// </summary>
        string Version { get; }

        /// <summary>
        /// Gets whether the plugin is properly initialized
        /// </summary>
        bool IsInitialized { get; }

        /// <summary>
        /// Initialize the plugin with configuration
        /// </summary>
        /// <param name="config">Configuration dictionary</param>
        /// <returns>True if initialization successful</returns>
        Task<bool> InitializeAsync(Dictionary<string, string> config);

        /// <summary>
        /// Fetch community insights from configured sources
        /// </summary>
        /// <param name="limit">Maximum insights to fetch per source</param>
        /// <returns>List of community insights</returns>
        Task<List<CommunityInsight>> FetchInsightsAsync(int limit = 50);

        /// <summary>
        /// Generate feature proposals from insights
        /// </summary>
        /// <param name="insights">Input insights</param>
        /// <returns>Generated feature proposals</returns>
        Task<List<FeatureProposal>> GenerateProposalsAsync(List<CommunityInsight> insights);

        /// <summary>
        /// Validate proposals against monetization guardrails
        /// </summary>
        /// <param name="proposals">Proposals to validate</param>
        /// <returns>Validation results for each proposal</returns>
        Task<Dictionary<FeatureProposal, List<GuardrailResult>>> ValidateProposalsAsync(
            List<FeatureProposal> proposals);

        /// <summary>
        /// Get the F2P policy document
        /// </summary>
        /// <returns>F2P policy as markdown string</returns>
        string GetF2PPolicy();

        /// <summary>
        /// Run the complete agent pipeline
        /// </summary>
        /// <returns>Pipeline run result</returns>
        Task<AgentPipelineResult> RunPipelineAsync();

        /// <summary>
        /// Shutdown the plugin and release resources
        /// </summary>
        Task ShutdownAsync();
    }

    /// <summary>
    /// Result of running the agent pipeline
    /// </summary>
    public class AgentPipelineResult
    {
        public bool Success { get; set; }
        public DateTime Timestamp { get; set; }
        public int TotalInsights { get; set; }
        public int TotalProposals { get; set; }
        public int CompliantProposals { get; set; }
        public float ExecutionTimeSeconds { get; set; }
        public List<CommunityInsight> Insights { get; set; }
        public List<FeatureProposal> Proposals { get; set; }
        public string ErrorMessage { get; set; }

        public AgentPipelineResult()
        {
            Insights = new List<CommunityInsight>();
            Proposals = new List<FeatureProposal>();
        }
    }

    /// <summary>
    /// Configuration helper for the plugin
    /// </summary>
    public static class PluginConfiguration
    {
        public const string RedditClientId = "REDDIT_CLIENT_ID";
        public const string RedditClientSecret = "REDDIT_CLIENT_SECRET";
        public const string DiscordBotToken = "DISCORD_BOT_TOKEN";
        public const string DiscordGuildId = "DISCORD_GUILD_ID";
        public const string SteamApiKey = "STEAM_API_KEY";
        public const string SteamAppId = "STEAM_APP_ID";
        public const string OutputDirectory = "OUTPUT_DIR";
        public const string LogLevel = "LOG_LEVEL";

        /// <summary>
        /// Create default configuration from environment variables
        /// </summary>
        public static Dictionary<string, string> FromEnvironment()
        {
            return new Dictionary<string, string>
            {
                { RedditClientId, Environment.GetEnvironmentVariable("REDDIT_CLIENT_ID") ?? "" },
                { RedditClientSecret, Environment.GetEnvironmentVariable("REDDIT_CLIENT_SECRET") ?? "" },
                { DiscordBotToken, Environment.GetEnvironmentVariable("DISCORD_BOT_TOKEN") ?? "" },
                { DiscordGuildId, Environment.GetEnvironmentVariable("DISCORD_GUILD_ID") ?? "" },
                { SteamApiKey, Environment.GetEnvironmentVariable("STEAM_API_KEY") ?? "" },
                { SteamAppId, Environment.GetEnvironmentVariable("STEAM_APP_ID") ?? "" },
                { OutputDirectory, "output" },
                { LogLevel, "INFO" }
            };
        }
    }
}
