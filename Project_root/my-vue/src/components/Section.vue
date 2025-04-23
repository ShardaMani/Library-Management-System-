<template>
  <div class="container">
    <h2 class="my-4">Section Management</h2>
    
    <!-- Button to open the create section modal -->
    <button class="btn btn-success mb-4" @click="showCreateSectionModal">Add Section</button>
    
    <!-- Section Cards -->
    <div class="row">
      <div class="col-md-4 mb-3" v-for="section in sections" :key="section.id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ section.name }}</h5>
            <p class="card-text">{{ section.description }}</p>
            <p class="card-text"><small class="text-muted">Created on {{ formatDate(section.date_created) }}</small></p>
            <button class="btn btn-primary btn-sm" @click="viewBooks(section)">View Books</button>
            <button class="btn btn-warning btn-sm" @click="showEditSectionModal(section)">Edit Section</button>
            <button class="btn btn-danger btn-sm" @click="deleteSection(section.id)">Delete Section</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Book Cards -->
    <div v-if="selectedSection" class="my-4">
      <h3>Books in {{ selectedSection.name }}</h3>
      <button class="btn btn-success mb-4" @click="showCreateBookModal">Add Book</button>
      
      <div class="row">
        <div class="col-md-4 mb-3" v-for="book in selectedSection.ebooks" :key="book.id">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{{ book.name }}</h5>
              <p class="card-text">Author: {{ book.author }}</p>
              <button class="btn btn-primary btn-sm" @click="viewBookContent(book)">View Content</button>
              <button class="btn btn-warning btn-sm" @click="showEditBookModal(book)">Edit</button>
              <button class="btn btn-danger btn-sm" @click="deleteBook(book.id)">Delete</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Create Section Modal -->
    <div v-if="showSectionModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h5>{{ isEditMode ? 'Edit Section' : 'Create Section' }}</h5>
        <input v-model="sectionForm.name" type="text" class="form-control mb-3" placeholder="Section Name" />
        <textarea v-model="sectionForm.description" class="form-control mb-3" rows="4" placeholder="Section Description"></textarea>
        <button class="btn btn-primary" @click="isEditMode ? updateSection() : createSection()">Submit</button>
        <button class="btn btn-secondary" @click="closeModal">Cancel</button>
      </div>
    </div>

    <!-- Create Book Modal -->
    <div v-if="showBookModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <h5>{{ isEditMode ? 'Edit Book' : 'Create Book' }}</h5>
        <input v-model="bookForm.name" type="text" class="form-control mb-3" placeholder="Book Name" />
        <input v-model="bookForm.author" type="text" class="form-control mb-3" placeholder="Author" />
        <textarea v-model="bookForm.content" class="form-control mb-3" rows="4" placeholder="Book Content"></textarea>
        <button class="btn btn-primary" @click="isEditMode ? updateBook() : createBook()">Submit</button>
        <button class="btn btn-secondary" @click="closeModal">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      sections: [],
      selectedSection: null,
      sectionForm: {
        id: null,
        name: '',
        description: ''
      },
      bookForm: {
        id: null,
        name: '',
        author: '',
        content: ''
      },
      showSectionModal: false,
      showBookModal: false,
      isEditMode: false,
    };
  },
  mounted() {
    this.fetchSections();
  },
  methods: {
    fetchSections() {
      axios.get('http://127.0.0.1:5000/sections', {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.sections = response.data.sections;
      })
      .catch(error => {
        console.error('Error fetching sections:', error);
      });
    },
    formatDate(date) {
      if (!date) return '';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    showCreateSectionModal() {
      this.isEditMode = false;
      this.sectionForm = { id: null, name: '', description: '' };
      this.showSectionModal = true;
    },
    showEditSectionModal(section) {
      this.isEditMode = true;
      this.sectionForm = { ...section };
      this.showSectionModal = true;
    },
    createSection() {
      axios.post('http://127.0.0.1:5000/sections', this.sectionForm, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.fetchSections();
        this.closeModal();
      })
      .catch(error => {
        console.error('Error creating section:', error);
      });
    },
    updateSection() {
      axios.put(`http://127.0.0.1:5000/sections/${this.sectionForm.id}`, this.sectionForm, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.fetchSections();
        this.closeModal();
      })
      .catch(error => {
        console.error('Error updating section:', error);
      });
    },
    deleteSection(id) {
      if (!confirm('Are you sure you want to delete this section?')) return;
      axios.delete(`http://127.0.0.1:5000/sections/${id}`, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.fetchSections();
      })
      .catch(error => {
        console.error('Error deleting section:', error);
      });
    },
    showCreateBookModal() {
      this.isEditMode = false;
      this.bookForm = { id: null, name: '', author: '', content: '' };
      this.showBookModal = true;
    },
    showEditBookModal(book) {
      this.isEditMode = true;
      this.bookForm = { ...book };
      this.showBookModal = true;
    },
    createBook() {
      axios.post(`http://127.0.0.1:5000/sections/${this.selectedSection.id}/ebooks`, this.bookForm, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.fetchSections();  // Refresh sections to include new book
        this.closeModal();
      })
      .catch(error => {
        console.error('Error creating book:', error);
      });
    },
    updateBook() {
      axios.put(`http://127.0.0.1:5000/ebooks/${this.bookForm.id}`, this.bookForm, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.fetchSections();  // Refresh sections to include updated book
        this.closeModal();
      })
      .catch(error => {
        console.error('Error updating book:', error);
      });
    },
    deleteBook(id) {
      if (!confirm('Are you sure you want to delete this book?')) return;
      axios.delete(`http://127.0.0.1:5000/ebooks/${id}`, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        this.fetchSections();  // Refresh sections to remove deleted book
      })
      .catch(error => {
        console.error('Error deleting book:', error);
      });
    },
    viewBooks(section) {
      this.selectedSection = section;
    },
    viewBookContent(book) {
      // Navigate to book content page (assuming a route is set up)
      this.$router.push({ name: 'BookContent', params: { id: book.id } });
    },
    closeModal() {
      this.showSectionModal = false;
      this.showBookModal = false;
    }
  }
};
</script>

<style>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  width: 500px;
  max-width: 90%;
}
</style>
