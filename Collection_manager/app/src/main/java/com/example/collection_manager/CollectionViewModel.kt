package com.example.collection_manager
import androidx.lifecycle.switchMap
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.collection_manager.data.model.Collection
import com.example.collection_manager.data.repository.CollectionRepository
import kotlinx.coroutines.launch
// for own reference
// https://developer.android.com/codelabs/android-room-with-a-view-kotlin#11
class CollectionViewModel(private val repository: CollectionRepository): ViewModel() {

//    private val _listCollection = MutableLiveData<LiveData<List<Collection>>>()
//    val allItems: LiveData<List<Collection>> = repository.getAllItems()
    enum class SortType { AZ, ZA, WW1WW2, WW2WW1 }

    private val sortType = MutableLiveData(SortType.AZ)

    // swithcmaps enable updating of recylcer view for live data stuff
    val allItems: LiveData<List<Collection>> = sortType.switchMap { sort ->
        when (sort) {
            SortType.AZ -> repository.sortAZ()
            SortType.ZA -> repository.sortZA()
            SortType.WW1WW2 -> repository.sort12()
            SortType.WW2WW1 -> repository.sort21()
        }
    }
    // wrapper method that calls repositroy method. this uses the viewmodels coroutinescope

    fun insert(item: Collection) = viewModelScope.launch{
        repository.insert(item)
    }

    fun update(item: Collection) = viewModelScope.launch{
        repository.update(item)
    }

    fun delete(item: Collection) = viewModelScope.launch{
        repository.delete(item)
    }

    fun getOneItem(id:Int): LiveData<Collection>{
        return repository.getOneItem(id)
    }

    fun sortAZ() {
        sortType.value = SortType.AZ
    }
    fun sortZA() {
        sortType.value = SortType.ZA
    }
    fun sort12() {
        sortType.value = SortType.WW1WW2
    }
    fun sort21() {
        sortType.value = SortType.WW2WW1
    }
}
// maintains on configuration change and if activity is recreated it will maintian the most recent instance of view model
class CollectionViewModelFactory(private val repository: CollectionRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(CollectionViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return CollectionViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}