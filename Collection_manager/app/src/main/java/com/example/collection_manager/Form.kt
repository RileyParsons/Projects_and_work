package com.example.collection_manager

import android.graphics.BitmapFactory
import java.util.UUID
import android.net.Uri
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Spinner
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.PickVisualMediaRequest
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Observer
import com.example.collection_manager.data.db.AppDatabase
import com.example.collection_manager.data.model.Collection
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlin.getValue

class Form : AppCompatActivity() {
    private lateinit var backButton: Button
    private lateinit var saveButton: Button
    private lateinit var pageName: TextView

    private lateinit var itemName: EditText
    private lateinit var itemCategory: Spinner
    private lateinit var itemEra: Spinner
    private lateinit var yearPurchased: EditText
    private lateinit var pricePurchased: EditText
    private lateinit var provenance: EditText
    private lateinit var description: EditText
    private lateinit var image: ImageView
    private var idData: Int? = -1
    // default value
    private var dataImageFileName: String = "No Image"
    private var oldImage: String = ""

    // Registers a photo picker activity launcher in single-select mode.
    private val pickMedia = registerForActivityResult(ActivityResultContracts.PickVisualMedia()) { uri ->
        // Callback is invoked after the user selects a media item or closes the
        // photo picker.
        if (uri != null) {
            Log.d("PhotoPicker", "Selected URI: $uri")
            saveImage(uri)
        } else {
            Log.d("PhotoPicker", "No media selected")
        }
    }

    private val collectionViewModel: CollectionViewModel by viewModels {
        CollectionViewModelFactory((application as CollectionApplication).repository)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_add_form)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        val pageTitle = intent.getStringExtra("page_title")
        // if accessed via viewItem for editing prefill form data with existing
        pageName = findViewById(R.id.heading)
        pageName.text = pageTitle

        image = findViewById(R.id.uploadImage)
        itemName = findViewById(R.id.item_name)
        itemCategory = findViewById(R.id.category)
        itemEra = findViewById(R.id.era)
        yearPurchased = findViewById(R.id.year_purchased)
        pricePurchased = findViewById(R.id.price_purchased)
        provenance = findViewById(R.id.provenance)
        description = findViewById(R.id.description)

        // set up spinners with adapters
        val catList = resources.getStringArray(R.array.category_list)
        val catAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, catList)
        itemCategory.adapter = catAdapter
        itemCategory.onItemSelectedListener = object :
            AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>,
                                        view: View, position: Int, id: Long) {
            }
            override fun onNothingSelected(parent: AdapterView<*>) {
                // write code to perform some action
            }
        }

        val eraList = resources.getStringArray(R.array.era_list)
        val eraAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, eraList)
        itemEra.adapter = eraAdapter
        itemEra.onItemSelectedListener = object :
            AdapterView.OnItemSelectedListener {
            override fun onItemSelected(
                parent: AdapterView<*>,
                view: View, position: Int, id: Long
            ) {

            }
            override fun onNothingSelected(parent: AdapterView<*>) {

            }
        }

        if(pageTitle =="Edit Item Info"){

            idData = intent.getIntExtra("data", 0)
            collectionViewModel.getOneItem(idData!!).observe(this, Observer{collections -> collections?.let{
                // update UI from the database through viewModel
                itemName.setText(it.name)
                itemCategory.setSelection(catList.indexOf(it.category))
                itemEra.setSelection(eraList.indexOf(it.era))
                yearPurchased.setText(it.yearPurchased.toString())
                pricePurchased.setText( it.pricePurchased.toString())
                provenance.setText(it.provenance)
                description.setText(it.description)
                dataImageFileName = it.imageFileName
                oldImage = it.imageFileName

                if (it.imageFileName != "No Image"){
                    try {
                        val inputStream = openFileInput(dataImageFileName)
                        val getImage = BitmapFactory.decodeStream(inputStream)
                        image.setImageBitmap(getImage)
                        inputStream.close()
                    }catch (e: Exception){
                        Toast.makeText(this, "Error accessing saved image: $e", Toast.LENGTH_SHORT).show()
                    }
                }

            }})
        }

        image.setOnClickListener {
            uploadImage()
        }

        backButton = findViewById(R.id.back)
        backButton.setOnClickListener {
            finish()
        }
        saveButton = findViewById(R.id.save)
        saveButton.setOnClickListener {
            // if val idData is negative one then insert.
            query()
        }
    }

    fun uploadImage(){
// Launch the photo picker and let the user choose only images.
        pickMedia.launch(PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
    }

    fun saveImage(uriImage: Uri){
        try{
            // saves to apps internal storage
            val inputSteam = contentResolver.openInputStream(uriImage)
            // generate unique random name for file
            val fileName = "user_image_${UUID.randomUUID()}.jpg"
            dataImageFileName = fileName
            // save file name for database inserting
            val outputStream = openFileOutput(fileName, MODE_PRIVATE)
            inputSteam?.copyTo(outputStream)
            inputSteam?.close()
            outputStream.close()
        } catch (e: Exception){
            Toast.makeText(this, "Error uploading image to application: $e", Toast.LENGTH_SHORT).show()
        }

        try {
            val inputStream = openFileInput(dataImageFileName)
            val getImage = BitmapFactory.decodeStream(inputStream)
            image.setImageBitmap(getImage)
        inputStream.close()
        }catch (e: Exception){
            Toast.makeText(this, "Error accessing saved image: $e", Toast.LENGTH_SHORT).show()
        }
        // when this is done change image icon
//        image.setImageResource(R.drawable.baseline_check_24)

        // to find saved image in app. view --> tools window --> device explorer
        // data --> data --> find app name and browse files

        // to retrieve in program
//        val inputStream = openFileInput(dataImageFileName)
//        val getImage = BitmapFactory.decodeStream(inputStream)
//        inputStream.close()
        // assign getImage to view id desired

    }

    fun query(){
        val queryName = itemName.text.toString()
        val queryCategory = itemCategory.selectedItem.toString()
        val queryEra = itemEra.selectedItem.toString()
        val queryYear = yearPurchased.text.toString().toIntOrNull() ?: 0
        val queryPrice = pricePurchased.text.toString().toIntOrNull() ?: 0
        val queryProv = provenance.text.toString()
        val queryDesc = description.text.toString()
        // data base access stuff
        val db = AppDatabase.getDatabase(context = this)
        // operator stuff
        val dao = db.collectionDao()

        if (idData == -1){
            // for adding new
            val collectionItem = Collection(name = queryName, category = queryCategory,
                era = queryEra, yearPurchased = queryYear, pricePurchased = queryPrice,
                provenance = queryProv , description = queryDesc, imageFileName = dataImageFileName)

            Log.i("SQLite Database", "Adding item: $collectionItem")

            // add with
            // start coroutine
            CoroutineScope(Dispatchers.IO).launch {
                dao.insert(collectionItem)
                runOnUiThread {
                    Toast.makeText(this@Form, "Item added", Toast.LENGTH_SHORT).show()
                    finish()
                }
            }
        }
        else{
            val collectionItem = Collection(id=idData,name = queryName, category = queryCategory,
                era = queryEra, yearPurchased = queryYear, pricePurchased = queryPrice,
                provenance = queryProv , description = queryDesc, imageFileName = dataImageFileName)

            if(oldImage != dataImageFileName && oldImage != "No Image"){
                try {
                    val delete = deleteFile(oldImage)
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

            Log.i("SQLite Database", "updating item: $collectionItem")
            // start coroutine
            CoroutineScope(Dispatchers.IO).launch {
                dao.update(collectionItem)
                runOnUiThread {
                    Toast.makeText(this@Form, "Item Updated", Toast.LENGTH_SHORT).show()
                    finish()
                }
            }
        }
    }

    // outside of in create
    // for saving instance and restoring
    override fun onSaveInstanceState(outState: Bundle) {
        // values that need to be saved
        super.onSaveInstanceState(outState)
        Log.i("APP_STATE", "App Instance state save called.")
        // key value pairs
        outState.putString("Item_name", itemName.text.toString())
        outState.putString("Item_image", dataImageFileName)

        outState.putInt("Item_cat", itemCategory.selectedItemPosition)
        outState.putInt("Item_era", itemEra.selectedItemPosition)

        outState.putString("Item_year", yearPurchased.toString())
        outState.putString("Item_price", pricePurchased.toString())
        outState.putString("Item_prov", provenance.text.toString())
        outState.putString("Item_desc", description.text.toString())

        Log.i("APP_STATE", "App Instance state save complete.")
    }

    // retrieve values
    // currently not accessed on phone rotation
    override fun onRestoreInstanceState(savedInstanceState: Bundle) {
        Log.i("APP_STATE", "App Restore called.")
        super.onRestoreInstanceState(savedInstanceState)

        itemName.setText(savedInstanceState.getString("Item_name"))
        dataImageFileName = savedInstanceState.getString("Item_image")!!
        yearPurchased.setText(savedInstanceState.getString("Item_year"))
        pricePurchased.setText(savedInstanceState.getString("Item_price"))
        provenance.setText(savedInstanceState.getString("Item_prov"))
        description.setText(savedInstanceState.getString("Item_desc"))

        if (dataImageFileName != "No Image"){
            try {
                val inputStream = openFileInput(dataImageFileName)
                val getImage = BitmapFactory.decodeStream(inputStream)
                image.setImageBitmap(getImage)
                inputStream.close()
            }catch (e: Exception){
                Toast.makeText(this, "Error accessing saved image: $e", Toast.LENGTH_SHORT).show()
            }
        }

        // spinner restoration
        val catList = resources.getStringArray(R.array.category_list)
        val catAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, catList)
        itemCategory.adapter = catAdapter
        itemCategory.onItemSelectedListener = object :
            AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>,
                                        view: View, position: Int, id: Long) {
            }
            override fun onNothingSelected(parent: AdapterView<*>) {
                // write code to perform some action
            }
        }

        itemCategory.setSelection(savedInstanceState.getInt("Item_cat"))

        val eraList = resources.getStringArray(R.array.era_list)
        val eraAdapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, eraList)
        itemEra.adapter = eraAdapter
        itemEra.onItemSelectedListener = object :
            AdapterView.OnItemSelectedListener {
            override fun onItemSelected(
                parent: AdapterView<*>,
                view: View, position: Int, id: Long
            ) {

            }
            override fun onNothingSelected(parent: AdapterView<*>) {
            }
        }
        itemEra.setSelection(savedInstanceState.getInt("Item_era"))

        Log.i("APP_STATE", "App Restore Complete.")
    }
}