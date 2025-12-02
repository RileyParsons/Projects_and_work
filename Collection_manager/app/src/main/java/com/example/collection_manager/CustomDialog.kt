package com.example.collection_manager

import android.content.Context
import androidx.appcompat.app.AlertDialog

class CustomDialog(context: Context): AlertDialog.Builder(context) {
    //declare a function as a variable
    lateinit var onResponse: (r: ResponseType) -> Unit
    enum class ResponseType{
        YES, NO
    }
    // here the listener is a lambda function
    fun customShow(title: String, message: String, listener: (r: ResponseType)-> Unit){
        val builder = AlertDialog.Builder(context)
        builder.setTitle(title)
        builder.setMessage(message)
        builder.setIcon(android.R.drawable.ic_dialog_info)

        onResponse = listener

        // on object creation pass in response lambda for these functions
        builder.setPositiveButton("Yes")
        // lambda function, first _ is dialog interface, second is the button id. here _ is for ignoring so it can be passed
        // for onResponse listener response value yes.
        {_,_-> onResponse(ResponseType.YES)}

        builder.setNegativeButton("No")
        {_,_-> onResponse(ResponseType.NO)}

        val alertDialog: AlertDialog = builder.create()

        alertDialog.setCancelable(false)
        alertDialog.show()
    }
}