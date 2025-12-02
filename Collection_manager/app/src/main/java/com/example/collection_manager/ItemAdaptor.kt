package com.example.collection_manager
import  android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import  androidx.recyclerview.widget.RecyclerView
import com.example.collection_manager.data.model.Collection
import com.example.collection_manager.databinding.ItemRowBinding

class ItemAdaptor : ListAdapter<Collection, ItemAdaptor.ViewHolder>(CollectionDiffCallback()) {

    private var onClickListener: OnClickListener? =null
    private var onLongClickListener: OnItemLongClickListener? =null

    // returns a vie holder
    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ViewHolder {
        val binding = ItemRowBinding.inflate(LayoutInflater.from(parent.context), parent, false)
        return ViewHolder(binding)
    }

    // bind data to a view holder and set the on click listener
    override fun onBindViewHolder(holder: ViewHolder, position: Int) {
        val collectionItem = getItem(position)
        holder.binding.textViewId.text = collectionItem.era
        holder.binding.textViewName.text = collectionItem.name

        holder.itemView.setOnClickListener {
            onClickListener?.onClick(position, collectionItem)
        }

        holder.itemView.setOnLongClickListener {
            onLongClickListener?.onLongClick(position, collectionItem)
            true
        }
    }

    // sets click listener for the adapter
    fun setOnClickListener(listener: OnClickListener?){
        this.onClickListener = listener
    }

    // interfaces contain declarations of abstract methods as well as implementations.
    // cannot store state
    interface OnClickListener{
        fun onClick(position: Int, model: Collection)
    }

    // create function with interface as the method
    fun setOnLongClickListener(listener: OnItemLongClickListener?){
        this.onLongClickListener = listener
    }

    interface OnItemLongClickListener{
        fun onLongClick(position: Int, model: Collection)
    }

    // for comparing collection data making use of diffUtil to calculate differences between 2 lists
    class CollectionDiffCallback : DiffUtil.ItemCallback<Collection>() {
        override fun areItemsTheSame(oldItem: Collection, newItem: Collection): Boolean =
            oldItem.id == newItem.id

        override fun areContentsTheSame(oldItem: Collection, newItem: Collection): Boolean =
            oldItem == newItem
    }
    // view holder class which is responsible for holding the views by item row
    class ViewHolder(val binding: ItemRowBinding): RecyclerView.ViewHolder(binding.root)
}