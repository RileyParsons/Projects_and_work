package com.example.collection_manager.data.db

import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import android.content.Context
import CollectionDao
import androidx.sqlite.db.SupportSQLiteDatabase
import com.example.collection_manager.data.model.Collection
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlin.String

@Database(entities = [Collection::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun collectionDao(): CollectionDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "collection"  // database file name
                )
                    // this callback is somthing thst is only called when the database is first created
                    .addCallback(object: Callback(){
                        override fun onCreate(db: SupportSQLiteDatabase){
                            super.onCreate(db) // so this on create will only ever run once in the app

                            // as part of this initial on create a coroutine is used to insert data into the db
                            CoroutineScope(Dispatchers.IO).launch {
                                val dao = getDatabase(context).collectionDao()
                                // how to call an insert into the db
                                dao.insert(
                                    // note item is of type collection so it needs to be filled in as such.
                                    // this is how to insert an item into the collection database
                                    Collection(
                                        name ="1914 Christmas Tin",
                                        category = "Other",
                                        era = "WW1",
                                        yearPurchased = 2019,
                                        pricePurchased = 100,
                                        provenance = "Purchased from australian antique store at Philip Island.",
                                        description = "WW1 christmas tin with no contents. Does not fully lose without force."
                                    )
                                )

                            }
                        }
                    })
                    .build()
                INSTANCE = instance
                instance
            }
        }
    }
}
