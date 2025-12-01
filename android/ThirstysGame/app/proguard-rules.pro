# Add project specific ProGuard rules here.
# By default, the flags in this file are appended to flags specified
# in /sdk/tools/proguard/proguard-android.txt

# Keep Retrofit models
-keep class com.thirstysgame.data.model.** { *; }

# Keep Gson annotations
-keepattributes Signature
-keepattributes *Annotation*

# Keep Retrofit
-dontwarn retrofit2.**
-keep class retrofit2.** { *; }

# Keep OkHttp
-dontwarn okhttp3.**
-keep class okhttp3.** { *; }
-dontwarn okio.**

# Keep Kotlin metadata
-keep class kotlin.Metadata { *; }
