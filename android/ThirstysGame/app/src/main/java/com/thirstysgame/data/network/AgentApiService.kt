package com.thirstysgame.data.network

import com.thirstysgame.data.model.AppDataBundle
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Url

/**
 * Retrofit API service for fetching app data from the agent pipeline.
 */
interface AgentApiService {
    
    /**
     * Fetch app data bundle from a URL.
     * The URL can be a remote endpoint or a raw GitHub URL.
     */
    @GET
    suspend fun getAppData(@Url url: String): Response<AppDataBundle>
}
