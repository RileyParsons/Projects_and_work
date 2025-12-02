package com.example.collection_manager

import android.content.Intent
import android.graphics.BitmapFactory
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.lifecycle.Observer
import kotlin.getValue

class ViewItem : AppCompatActivity() {
    private lateinit var backButton: Button
    private lateinit var editButton: Button
    private lateinit var itemDetails: TextView
    private lateinit var viewImage: ImageView

    private val collectionViewModel: CollectionViewModel by viewModels {
        CollectionViewModelFactory((application as CollectionApplication).repository)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_view_item)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        // adjust to work better with observer and go to add form with data
        val itemID = intent.getIntExtra("data", 0)

        Log.i("Intent", "Item acquired: $itemID")

        viewImage = findViewById(R.id.viewImage)

        itemDetails = findViewById(R.id.itemDetails)

        backButton = findViewById(R.id.back)
        backButton.setOnClickListener {
            finish()
        }

        editButton = findViewById(R.id.edit)
        editButton.setOnClickListener {
            goToAddFormWithData(itemID)
            // create an intent to move to the form page
        }

        // query form database with the viewmodel. apply observer
        collectionViewModel.getOneItem(itemID).observe(this, Observer{ collections -> collections?.let{
            // update UI from the query that is being observer
            val observableText = getString(R.string.item_details,it.name, it.category,
                it.era, it.yearPurchased, it.pricePurchased,
                it.provenance, it.description)
            // insert observable data
            itemDetails.text = observableText

            // assign image if one exists otherwise the default icon will be used.
            if(it.imageFileName != "No Image"){
                try {
                    val inputStream = openFileInput(it.imageFileName)
                    val getImage = BitmapFactory.decodeStream(inputStream)
                    viewImage.setImageBitmap(getImage)
                    inputStream.close()
                }catch (e: Exception){
                    Toast.makeText(this, "Error accessing saved image: $e", Toast.LENGTH_SHORT).show()
                }

            }
        }})
    }

    // adjust this to work with observer data
    fun goToAddFormWithData(itemID: Int){
        val intent = Intent(this, Form::class.java)
        // add passing of data for prefill
        intent.putExtra("page_title","Edit Item Info")
        intent.putExtra("data", itemID)
        startActivity(intent)
    }
}