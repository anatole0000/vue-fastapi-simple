<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Items</h1>
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>
    <div v-else>
      <ul class="list-group">
        <li v-for="item in items" :key="item.id" class="list-group-item d-flex justify-content-between align-items-center">
          {{ item.name }}
          <div>
            <button @click="editItem(item)" class="btn btn-warning btn-sm mr-2">Edit</button>
            <button @click="deleteItem(item.id)" class="btn btn-danger btn-sm">Delete</button>
          </div>
        </li>
      </ul>
    </div>
    <div class="mt-3">
      <input v-model="newItemName" class="form-control" placeholder="Add new item" />
      <button @click="addItem" class="btn btn-primary mt-2">Add Item</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      items: [],
      newItemName: '',
      loading: false,  // Loading state to show spinner
    };
  },
  mounted() {
    this.fetchItems();
  },
  methods: {
    async fetchItems() {
      this.loading = true;
      try {
        const response = await axios.get('http://127.0.0.1:5000/items');
        this.items = response.data;
      } catch (error) {
        console.error('Error fetching items:', error);
      } finally {
        this.loading = false;
      }
    },
    async addItem() {
      if (this.newItemName.trim()) {
        this.loading = true;
        try {
          const response = await axios.post('http://127.0.0.1:5000/items', { name: this.newItemName });
          this.items.push(response.data);
          this.newItemName = '';
        } catch (error) {
          console.error('Error adding item:', error);
        } finally {
          this.loading = false;
        }
      }
    },
    async editItem(item) {
      const newName = prompt('Enter the new name for this item:', item.name);
      if (newName && newName !== item.name) {
        this.loading = true;
        try {
          const response = await axios.put(`http://127.0.0.1:5000/items/${item.id}`, { name: newName });
          item.name = response.data.name;
        } catch (error) {
          console.error('Error updating item:', error);
        } finally {
          this.loading = false;
        }
      }
    },
    async deleteItem(id) {
      if (confirm('Are you sure you want to delete this item?')) {
        this.loading = true;
        try {
          await axios.delete(`http://127.0.0.1:5000/items/${id}`);
          this.items = this.items.filter(item => item.id !== id);
        } catch (error) {
          console.error('Error deleting item:', error);
        } finally {
          this.loading = false;
        }
      }
    },
  },
};
</script>
