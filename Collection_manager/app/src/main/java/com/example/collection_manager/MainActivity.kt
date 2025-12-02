package com.example.collection_manager

import android.os.Bundle
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import com.example.collection_manager.data.db.AppDatabase
import com.example.collection_manager.data.model.Collection
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import android.util.Log
import android.content.Intent
import android.view.Menu
import android.view.MenuInflater
import android.view.MenuItem
import androidx.recyclerview.widget.LinearLayoutManager
import com.example.collection_manager.databinding.ActivityMainBinding
import android.widget.Button
import android.widget.Toast
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatDelegate
import androidx.lifecycle.Observer

class MainActivity : AppCompatActivity() {

    private lateinit var addNewItemButton: Button
    //set up view binding thing
    private val binding: ActivityMainBinding by lazy {
        ActivityMainBinding.inflate(layoutInflater)
    }
    // create view model for data. basically an invisible layer
    private val collectionViewModel: CollectionViewModel by viewModels {
        CollectionViewModelFactory((application as CollectionApplication).repository)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        enableEdgeToEdge()
//        setContentView(R.layout.activity_main)
        // allows for recycler view to find and access I think
        setContentView(binding.root)
        // The Toolbar defined in the layout has the id "my_toolbar".
        setSupportActionBar(findViewById(R.id.toolbar_main))
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        addNewItemButton = findViewById<Button>(R.id.AddNewItem)
        addNewItemButton.setOnClickListener {
            goToAddForm()
        }
        // create an instance of the adaptor
        val adaptor = ItemAdaptor()
        binding.rvItemsList.layoutManager = LinearLayoutManager(this@MainActivity)
        binding.rvItemsList.setHasFixedSize(true)
        binding.rvItemsList.adapter = adaptor


        // implement adaptor functionality from class for clicking on item
        adaptor.setOnClickListener (object: ItemAdaptor.OnClickListener {
            override fun onClick(position: Int, model: Collection) {
                // pass all data from collection item into the intent
                val intent = Intent(this@MainActivity, ViewItem::class.java)
                intent.putExtra("data",model.id)
                startActivity(intent)
            }
        })
        adaptor.setOnLongClickListener (object: ItemAdaptor.OnItemLongClickListener {
            override fun onLongClick(position: Int, model: Collection)
             {
                 Toast.makeText(this@MainActivity, "Item Selected: ${model.name}", Toast.LENGTH_SHORT).show()
                 deleteItem(model)
            }
        })
        // create observer that is observing all items within the
        collectionViewModel.allItems.observe(this, Observer{collections -> collections?.let{adaptor.submitList(it)}})
    }


    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        val inflater: MenuInflater = menuInflater
        inflater.inflate(R.menu.custom_menu,menu)
        // how go find and assign items in menu.
        // 1. find in menu
        // 2. find id by generated widget in layout
        val switchy = menu?.findItem(R.id.app_bar_switch)
        val toggleMode = switchy?.actionView?.findViewById<androidx.appcompat.widget.SwitchCompat>(R.id.toggle_mode)

        // if currently in night mode return true. tis is a boolean value
        val currentNightMode = AppCompatDelegate.getDefaultNightMode()
        // move the switch position on reload of application if current night mode is true. so toggle mode is true if current night mode int value equals the app int night mode value
        // this works because if the override
        toggleMode?.isChecked = currentNightMode == AppCompatDelegate.MODE_NIGHT_YES

        toggleMode?.setOnCheckedChangeListener { buttonView, isChecked: Boolean ->
            if (isChecked) {
                Toast.makeText(this, "Dark Mode", Toast.LENGTH_SHORT).show()
                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES)
            } else {
                Toast.makeText(this, "Light Mode", Toast.LENGTH_SHORT).show()
                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO)
            }
        }
        return super.onCreateOptionsMenu(menu)
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Switching on the item id of the menu item
        when (item.itemId) {
            R.id.sort_name_a_z -> {
                // Code to be executed when the add button is clicked
                Toast.makeText(this, "Pressed A-Z sort", Toast.LENGTH_SHORT).show()
                collectionViewModel.sortAZ()
                return true
            }
            R.id.sort_name_z_a ->{// Code to be executed when the add button is clicked
                Toast.makeText(this, "Pressed Z-A sort", Toast.LENGTH_SHORT).show()
                collectionViewModel.sortZA()
                return true
            }
            R.id.ww1_sort -> {
                // Code to be executed when the add button is clicked
                Toast.makeText(this, "Pressed WW1 - WW2 sort", Toast.LENGTH_SHORT).show()
                collectionViewModel.sort12()
                return true
            }
            R.id.ww2_sort ->{// Code to be executed when the add button is clicked
                Toast.makeText(this, "Pressed WW2 - WW1 sort", Toast.LENGTH_SHORT).show()
                collectionViewModel.sort21()
                return true
            }
        }
        return super.onOptionsItemSelected(item)
    }
    fun goToAddForm(){
        val intent = Intent(this@MainActivity, Form::class.java)
        intent.putExtra("page_title","Add New Item")
        startActivity(intent)
    }

    fun deleteItem(item: Collection){
        val popUp = CustomDialog(this@MainActivity)
        // note responseType needs a lambda function to work
        popUp.customShow("Delete Item", "Are you sure you want to delete ${item.name}?"
        ) { responseType ->
            when (responseType) {
                // when the user input is yes to delete start a coroutine to query database to delete item
                CustomDialog.ResponseType.YES -> CoroutineScope(Dispatchers.IO).launch {
                    // data base access stuff
                    val db = AppDatabase.getDatabase(context = this@MainActivity)
                    // operator stuff
                    val dao = db.collectionDao()
                    // delete item from internal storage if picture exists
                    val imageName = item.imageFileName
                    if(imageName != "No Image"){
                        try {
                            val delete = deleteFile(imageName)
                            if (delete){
                                Log.i("App Storage", "Image deleted.")
                            }else{
                                Log.w("App Storage","Image failed to delete.")
                            }
                        }catch (e: Exception){
                            runOnUiThread {
                                Log.e("App Storage","Error deleting image file from internal storage: ${e}.")
                            }
                        }
                    }
                    dao.delete(item)
                    runOnUiThread {
                        Toast.makeText(this@MainActivity, "Item deleted: ${item.name}", Toast.LENGTH_SHORT).show()
                    }
                }
                CustomDialog.ResponseType.NO -> Toast.makeText(this@MainActivity, "Item deletion Canceled", Toast.LENGTH_SHORT).show()
            }
        }
    }
}