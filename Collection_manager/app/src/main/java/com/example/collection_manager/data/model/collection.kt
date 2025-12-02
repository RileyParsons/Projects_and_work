package com.example.collection_manager.data.model
import android.os.Parcelable
import kotlinx.parcelize.Parcelize

import androidx.room.ColumnInfo
import androidx.room.Entity
import androidx.room.PrimaryKey

@Parcelize
@Entity(tableName = "collection")
data class Collection(
    @PrimaryKey(autoGenerate = true) val id: Int? = null,
    @ColumnInfo val name: String,
    @ColumnInfo val category: String,
    @ColumnInfo val era: String,
    @ColumnInfo val yearPurchased: Int? = null,
    @ColumnInfo val pricePurchased: Int? = null,
    @ColumnInfo val provenance: String? = "Unknown",
    @ColumnInfo val description: String? ="No description",
    @ColumnInfo val imageFileName: String = "No Image"
) : Parcelable