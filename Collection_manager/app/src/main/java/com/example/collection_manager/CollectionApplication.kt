package com.example.collection_manager

import android.app.Application
import com.example.collection_manager.data.db.AppDatabase
import com.example.collection_manager.data.repository.CollectionRepository

class CollectionApplication: Application() {

    val database by lazy { AppDatabase.getDatabase(this) }
    val repository by lazy { CollectionRepository(database.collectionDao()) }
}