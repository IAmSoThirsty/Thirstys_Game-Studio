package com.thirstysgame.ui.viewmodel

import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import com.thirstysgame.data.model.*
import com.thirstysgame.data.repository.AppDataRepository
import io.mockk.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.*
import org.junit.*
import org.junit.Assert.*

/**
 * Unit tests for MainViewModel.
 */
@OptIn(ExperimentalCoroutinesApi::class)
class MainViewModelTest {
    
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()
    
    private val testDispatcher = StandardTestDispatcher()
    
    private lateinit var repository: AppDataRepository
    private lateinit var viewModel: MainViewModel
    
    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        repository = mockk()
    }
    
    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }
    
    @Test
    fun `initial state is loading`() = runTest {
        coEvery { repository.loadAppData(any()) } returns Result.success(createTestAppData())
        
        viewModel = MainViewModel(repository)
        
        assertTrue(viewModel.appDataState.value is UiState.Loading)
    }
    
    @Test
    fun `loadData success updates state`() = runTest {
        val testData = createTestAppData()
        coEvery { repository.loadAppData(any()) } returns Result.success(testData)
        
        viewModel = MainViewModel(repository)
        advanceUntilIdle()
        
        assertTrue(viewModel.appDataState.value is UiState.Success)
        assertEquals(testData.proposals.size, viewModel.proposals.value.size)
        assertEquals(testData.storefrontItems.size, viewModel.storefrontItems.value.size)
    }
    
    @Test
    fun `getProposalCount returns correct count`() = runTest {
        val testData = createTestAppData()
        coEvery { repository.loadAppData(any()) } returns Result.success(testData)
        
        viewModel = MainViewModel(repository)
        advanceUntilIdle()
        
        assertEquals(2, viewModel.getProposalCount())
    }
    
    @Test
    fun `getCompliantProposalCount returns correct count`() = runTest {
        val testData = createTestAppData()
        coEvery { repository.loadAppData(any()) } returns Result.success(testData)
        
        viewModel = MainViewModel(repository)
        advanceUntilIdle()
        
        assertEquals(1, viewModel.getCompliantProposalCount())
    }
    
    @Test
    fun `refresh reloads data`() = runTest {
        val testData = createTestAppData()
        coEvery { repository.loadAppData(any()) } returns Result.success(testData)
        
        viewModel = MainViewModel(repository)
        advanceUntilIdle()
        
        viewModel.refresh()
        advanceUntilIdle()
        
        coVerify(exactly = 2) { repository.loadAppData(any()) }
    }
    
    private fun createTestAppData(): AppDataBundle {
        return AppDataBundle(
            version = "1.0.0",
            generatedAt = "2024-01-01T00:00:00Z",
            insightsSummary = InsightsSummary(
                totalCount = 10,
                avgSentiment = 0.75f,
                topTopics = listOf(listOf("customization", 5)),
                sources = listOf("reddit", "discord")
            ),
            proposals = listOf(
                FeatureProposal(
                    title = "Test Proposal 1",
                    description = "Description 1",
                    sourceInsights = listOf(),
                    category = "customization",
                    monetizationType = "cosmetic",
                    priority = 0.8f,
                    f2pCompliant = true,
                    guardrailNotes = listOf(),
                    comparativeNotes = listOf(),
                    createdAt = "2024-01-01T00:00:00Z"
                ),
                FeatureProposal(
                    title = "Test Proposal 2",
                    description = "Description 2",
                    sourceInsights = listOf(),
                    category = "gameplay",
                    monetizationType = "free",
                    priority = 0.5f,
                    f2pCompliant = false,
                    guardrailNotes = listOf("Needs review"),
                    comparativeNotes = listOf(),
                    createdAt = "2024-01-01T00:00:00Z"
                )
            ),
            f2pPolicySummary = F2PPolicySummary(
                corePrinciples = listOf("No P2W"),
                whatWeOffer = listOf("Cosmetics"),
                whatWeNeverDo = listOf("Sell advantages")
            ),
            storefrontItems = listOf(
                StorefrontItem(
                    id = "item_001",
                    name = "Test Skin",
                    type = "cosmetic",
                    price = 500,
                    currency = "gems",
                    description = "A test cosmetic"
                )
            )
        )
    }
}
