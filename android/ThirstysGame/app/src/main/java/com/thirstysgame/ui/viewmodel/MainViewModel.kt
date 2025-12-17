package com.thirstysgame.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.thirstysgame.data.model.AppDataBundle
import com.thirstysgame.data.model.FeatureProposal
import com.thirstysgame.data.model.InsightsSummary
import com.thirstysgame.data.model.StorefrontItem
import com.thirstysgame.data.model.F2PPolicySummary
import com.thirstysgame.data.repository.AppDataRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * UI state for the main app data.
 */
sealed class UiState<out T> {
    object Loading : UiState<Nothing>()
    data class Success<T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}

/**
 * ViewModel for the main app screen.
 * Manages loading and displaying app data from the agent pipeline.
 */
class MainViewModel(
    private val repository: AppDataRepository = AppDataRepository()
) : ViewModel() {
    
    private val _appDataState = MutableStateFlow<UiState<AppDataBundle>>(UiState.Loading)
    val appDataState: StateFlow<UiState<AppDataBundle>> = _appDataState.asStateFlow()
    
    private val _insightsSummary = MutableStateFlow<InsightsSummary?>(null)
    val insightsSummary: StateFlow<InsightsSummary?> = _insightsSummary.asStateFlow()
    
    private val _proposals = MutableStateFlow<List<FeatureProposal>>(emptyList())
    val proposals: StateFlow<List<FeatureProposal>> = _proposals.asStateFlow()
    
    private val _storefrontItems = MutableStateFlow<List<StorefrontItem>>(emptyList())
    val storefrontItems: StateFlow<List<StorefrontItem>> = _storefrontItems.asStateFlow()
    
    private val _f2pPolicy = MutableStateFlow<F2PPolicySummary?>(null)
    val f2pPolicy: StateFlow<F2PPolicySummary?> = _f2pPolicy.asStateFlow()
    
    init {
        loadData()
    }
    
    /**
     * Load all app data from repository.
     */
    fun loadData() {
        viewModelScope.launch {
            _appDataState.value = UiState.Loading
            
            repository.loadAppData().fold(
                onSuccess = { data ->
                    _appDataState.value = UiState.Success(data)
                    _insightsSummary.value = data.insightsSummary
                    _proposals.value = data.proposals
                    _storefrontItems.value = data.storefrontItems
                    _f2pPolicy.value = data.f2pPolicySummary
                },
                onFailure = { error ->
                    _appDataState.value = UiState.Error(error.message ?: "Unknown error")
                }
            )
        }
    }
    
    /**
     * Refresh data from remote source.
     */
    fun refresh() {
        loadData()
    }
    
    /**
     * Get proposal count.
     */
    fun getProposalCount(): Int = _proposals.value.size
    
    /**
     * Get compliant proposal count.
     */
    fun getCompliantProposalCount(): Int = _proposals.value.count { it.f2pCompliant }
}
