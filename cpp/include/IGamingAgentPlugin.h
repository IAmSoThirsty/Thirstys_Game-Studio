/**
 * IGamingAgentPlugin.h
 * 
 * Cross-language interface for integrating with the Gaming Agent system.
 * This header provides C++ interfaces for game engines (Unreal, custom engines)
 * to interact with the agent platform.
 * 
 * Copyright (c) 2024 Thirsty's Game Studio
 */

#ifndef IGAMING_AGENT_PLUGIN_H
#define IGAMING_AGENT_PLUGIN_H

#include <string>
#include <vector>
#include <map>
#include <memory>
#include <chrono>
#include <functional>

namespace ThirstysGameStudio {
namespace Agent {

/**
 * @brief Represents a community insight from various sources
 */
struct CommunityInsight {
    std::string source;
    std::string content;
    float sentiment = 0.0f;
    std::vector<std::string> topics;
    std::string author;
    std::chrono::system_clock::time_point timestamp;
    std::map<std::string, int> engagement;
    std::string category;
    float priority = 0.5f;
};

/**
 * @brief Represents a feature proposal derived from community insights
 */
struct FeatureProposal {
    std::string title;
    std::string description;
    std::vector<std::string> sourceInsights;
    std::string category;
    std::string monetizationType;
    float priority = 0.5f;
    bool f2pCompliant = true;
    std::vector<std::string> guardrailNotes;
    std::vector<std::string> comparativeNotes;
    std::chrono::system_clock::time_point createdAt;
};

/**
 * @brief Monetization guardrail types for F2P compliance
 */
enum class MonetizationGuardrail {
    NoPayToWin,
    CosmeticOnly,
    NoGameplayAdvantage,
    FairProgression,
    TransparentOdds,
    NoLootBoxes,
    AccessibleContent
};

/**
 * @brief Result of a guardrail check
 */
struct GuardrailResult {
    bool passed = false;
    MonetizationGuardrail guardrail;
    std::string message;
    std::vector<std::string> suggestions;
};

/**
 * @brief Result of running the agent pipeline
 */
struct AgentPipelineResult {
    bool success = false;
    std::chrono::system_clock::time_point timestamp;
    int totalInsights = 0;
    int totalProposals = 0;
    int compliantProposals = 0;
    float executionTimeSeconds = 0.0f;
    std::vector<CommunityInsight> insights;
    std::vector<FeatureProposal> proposals;
    std::string errorMessage;
};

/**
 * @brief Configuration for the plugin
 */
struct PluginConfiguration {
    std::string redditClientId;
    std::string redditClientSecret;
    std::string discordBotToken;
    std::string discordGuildId;
    std::string steamApiKey;
    std::string steamAppId;
    std::string outputDirectory = "output";
    std::string logLevel = "INFO";
    
    /**
     * @brief Load configuration from environment variables
     */
    static PluginConfiguration fromEnvironment();
};

/**
 * @brief Callback type for async operations
 */
template<typename T>
using AsyncCallback = std::function<void(bool success, T result, std::string error)>;

/**
 * @brief Main interface for the Gaming Agent Plugin
 * 
 * Implement this interface to integrate the agent system with your game engine.
 * This interface provides both synchronous and asynchronous methods for
 * flexibility in different game architectures.
 */
class IGamingAgentPlugin {
public:
    virtual ~IGamingAgentPlugin() = default;

    /**
     * @brief Get the plugin version string
     */
    virtual std::string getVersion() const = 0;

    /**
     * @brief Check if the plugin is properly initialized
     */
    virtual bool isInitialized() const = 0;

    /**
     * @brief Initialize the plugin with configuration
     * @param config Plugin configuration
     * @return True if initialization successful
     */
    virtual bool initialize(const PluginConfiguration& config) = 0;

    /**
     * @brief Initialize the plugin asynchronously
     * @param config Plugin configuration
     * @param callback Callback with result
     */
    virtual void initializeAsync(const PluginConfiguration& config,
                                  AsyncCallback<bool> callback) = 0;

    /**
     * @brief Fetch community insights from configured sources
     * @param limit Maximum insights to fetch per source
     * @return List of community insights
     */
    virtual std::vector<CommunityInsight> fetchInsights(int limit = 50) = 0;

    /**
     * @brief Fetch community insights asynchronously
     * @param limit Maximum insights to fetch per source
     * @param callback Callback with results
     */
    virtual void fetchInsightsAsync(int limit, 
                                     AsyncCallback<std::vector<CommunityInsight>> callback) = 0;

    /**
     * @brief Generate feature proposals from insights
     * @param insights Input insights to process
     * @return Generated feature proposals
     */
    virtual std::vector<FeatureProposal> generateProposals(
        const std::vector<CommunityInsight>& insights) = 0;

    /**
     * @brief Validate proposals against monetization guardrails
     * @param proposals Proposals to validate
     * @return Map of proposal index to validation results
     */
    virtual std::map<size_t, std::vector<GuardrailResult>> validateProposals(
        const std::vector<FeatureProposal>& proposals) = 0;

    /**
     * @brief Get the F2P policy document
     * @return F2P policy as markdown string
     */
    virtual std::string getF2PPolicy() const = 0;

    /**
     * @brief Run the complete agent pipeline
     * @return Pipeline run result
     */
    virtual AgentPipelineResult runPipeline() = 0;

    /**
     * @brief Run the complete agent pipeline asynchronously
     * @param callback Callback with result
     */
    virtual void runPipelineAsync(AsyncCallback<AgentPipelineResult> callback) = 0;

    /**
     * @brief Shutdown the plugin and release resources
     */
    virtual void shutdown() = 0;
};

/**
 * @brief Factory function to create a plugin instance
 * 
 * Implement this function in your plugin implementation to create instances.
 */
extern "C" {
    std::unique_ptr<IGamingAgentPlugin> createGamingAgentPlugin();
    void destroyGamingAgentPlugin(IGamingAgentPlugin* plugin);
}

/**
 * @brief RAII wrapper for plugin lifecycle management
 */
class PluginHandle {
public:
    PluginHandle() : plugin_(createGamingAgentPlugin()) {}
    ~PluginHandle() { if (plugin_) plugin_->shutdown(); }
    
    // Non-copyable
    PluginHandle(const PluginHandle&) = delete;
    PluginHandle& operator=(const PluginHandle&) = delete;
    
    // Movable
    PluginHandle(PluginHandle&& other) noexcept : plugin_(std::move(other.plugin_)) {}
    PluginHandle& operator=(PluginHandle&& other) noexcept {
        plugin_ = std::move(other.plugin_);
        return *this;
    }
    
    IGamingAgentPlugin* operator->() { return plugin_.get(); }
    IGamingAgentPlugin& operator*() { return *plugin_; }
    explicit operator bool() const { return plugin_ != nullptr; }
    
private:
    std::unique_ptr<IGamingAgentPlugin> plugin_;
};

} // namespace Agent
} // namespace ThirstysGameStudio

#endif // IGAMING_AGENT_PLUGIN_H
