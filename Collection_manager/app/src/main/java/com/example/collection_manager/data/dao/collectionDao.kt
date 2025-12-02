import androidx.lifecycle.LiveData
import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.Query

import androidx.room.*
import com.example.collection_manager.data.model.Collection

@Dao
interface CollectionDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(item: Collection)

    @Update
    suspend fun update(item: Collection)

    @Delete
    suspend fun delete(item: Collection)

    @Query("SELECT * FROM Collection")
    fun getAllItems(): LiveData<List<Collection>>
//live data should not be suspend funcitons
    @Query("SELECT * FROM Collection WHERE id = :id ")
    fun getOneItem(id:Int): LiveData<Collection>

    @Query("SELECT * FROM collection ORDER BY name ASC")
    fun sortAZ(): LiveData<List<Collection>>

    @Query("SELECT * FROM collection ORDER BY name DESC")
    fun sortZA(): LiveData<List<Collection>>

    @Query("SELECT * FROM collection ORDER BY CASE WHEN era = 'WW1' THEN 1 WHEN era = 'WW1-WW2' THEN 2 WHEN era = 'Interwar' THEN 3 WHEN era = 'WW2' THEN 4 ELSE 5 END, name ASC")
    fun sort12(): LiveData<List<Collection>>

    @Query("SELECT * FROM collection ORDER BY CASE WHEN era = 'WW2' THEN 1 WHEN era = 'Interwar' THEN 2 WHEN era = 'WW1-WW2' THEN 3 WHEN era = 'WW1' THEN 4 ELSE 5 END, name ASC")
    fun sort21(): LiveData<List<Collection>>

    @Query ("SELECT COUNT(*) FROM collection")
    fun getSize(): Int
}

