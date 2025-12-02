package com.example.collection_manager.data.repository

import CollectionDao
import androidx.lifecycle.LiveData
import com.example.collection_manager.data.model.Collection
// repository absracts access to multiple dat sources. best practice for code seperation
// provides clean api for data access
// manages queries and allows multiple backends
// implements logic for deciding whether to getch data or use results in local db
// initilise repositry for managing queries. initilize with DAO

// passing dao into rep con because it only needs access to DAO as it has all read write methods
class CollectionRepository(private val dao: CollectionDao) {

    // create livedata of all items in colleciton
    val allCollectionItems: LiveData<List<Collection>> = dao.getAllItems()

    suspend fun insert(item: Collection){
        dao.insert(item)
    }

    suspend fun update(item: Collection){
        dao.update(item)
    }

    suspend fun delete(item: Collection){
        dao.delete(item)
    }

    fun getAllItems(): LiveData<List<Collection>> {
        return dao.getAllItems()
    }

    fun getOneItem(id: Int): LiveData<Collection> {
        return dao.getOneItem(id)
    }

    fun sortAZ(): LiveData<List<Collection>>{
        return dao.sortAZ()
    }

    fun sortZA(): LiveData<List<Collection>>{
        return dao.sortZA()
    }

    fun sort12(): LiveData<List<Collection>>{
        return dao.sort12()
    }

    fun sort21(): LiveData<List<Collection>>{
        return dao.sort21()
    }
}