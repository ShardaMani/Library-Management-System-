<template>
  <div class="container mt-5">
    <h2>User Dashboard</h2>
    <!-- Profile Button -->
    <div class="mt-5">
      <button @click="goToProfile" class="btn btn-info">Go to Profile</button>
    </div>
    <div class="mt-5">
      <button @click="goToMyBooks" class="btn btn-info">My Books</button>
    </div>

    <!-- Search Bar -->
    <div class="input-group mb-3">
      <input v-model="searchQuery" type="text" class="form-control" placeholder="Search for e-books or sections...">
      <div class="input-group-append">
        <button @click="search" class="btn btn-primary" type="button">Search</button>
      </div>
    </div>

    <!-- No Results Found Message -->
    <div v-if="sections.length === 0 && selectedSection == null" class="mt-4">
      <p>No results found.</p>
    </div>

    <!-- Sections List -->
    <div v-if="sections.length > 0" class="mt-4">
      <h3>Sections</h3>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Date Created</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="section in sections" :key="section.id">
            <td>{{ section.id }}</td>
            <td>{{ section.name }}</td>
            <td>{{ section.description }}</td>
            <td>{{ section.date_created }}</td>
            <td>
              <button @click="viewEbooks(section.id)" class="btn btn-primary btn-sm">View E-books</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Ebooks List -->
    <div v-if="selectedSection && selectedSection.ebooks.length > 0" class="mt-4">
      <h3>Ebooks in {{ selectedSection.name }}</h3>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Author</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ebook in selectedSection.ebooks" :key="ebook.id">
            <td>{{ ebook.id }}</td>
            <td>{{ ebook.name }}</td>
            <td>{{ ebook.author }}</td>
            <td>
              <button @click="openRequestModal(ebook)" class="btn btn-success btn-sm">Request</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Request Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h5 class="modal-title">Request Ebook</h5>
          <button type="button" class="close" @click="closeModal">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <label for="days">Number of days:</label>
          <input type="number" id="days" v-model="requestDays" min="1" class="form-control" placeholder="Enter number of days">
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
          <button type="button" class="btn btn-primary" @click="submitRequest">Request</button>
        </div>
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
      searchQuery: '',
      showModal: false,
      requestDays: 1,
      selectedEbook: null,
    };
  },
  methods: {
    async fetchSections() {
      const response = await axios.get('http://127.0.0.1:5000/sections', {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken'),
        },
      });
      this.sections = response.data.sections;
    },
    async viewEbooks(sectionId) {
      const response = await axios.get(`http://127.0.0.1:5000/sections/${sectionId}/ebooks`, {
        headers: {
          'Authentication-Token': localStorage.getItem('authToken'),
        },
      });
      this.selectedSection = response.data;
    },
    openRequestModal(ebook) {
      this.selectedEbook = ebook;
      this.requestDays = 1;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedEbook = null;
    },
    async submitRequest() {
      const returnDate = new Date();
      returnDate.setDate(returnDate.getDate() + this.requestDays);

      try {
        await axios.post(`http://127.0.0.1:5000/ebooks/${this.selectedEbook.id}/request`, {
          return_date: returnDate.toISOString().split('T')[0],
        }, {
          headers: {
            'Authentication-Token': localStorage.getItem('authToken'),
          },
        });

        alert('Ebook requested successfully!');
        // Remove the requested book from the list
        this.selectedSection.ebooks = this.selectedSection.ebooks.filter(
          ebook => ebook.id !== this.selectedEbook.id
        );
        this.closeModal();
      } catch (error) {
        console.error('Error requesting ebook:', error);
        alert('An error occurred while requesting the ebook.');
      }
    },
    async search() {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/ebooks/search?query=${this.searchQuery}`, {
          headers: {
            'Authentication-Token': localStorage.getItem('authToken'),
          },
        });

        const ebooks = response.data.ebooks;
        const sections = response.data.sections;

        if (ebooks.length > 0) {
          let ebooksGroupedBySection = {};
          ebooks.forEach(ebook => {
            if (!ebooksGroupedBySection[ebook.section_id]) {
              ebooksGroupedBySection[ebook.section_id] = [];
            }
            ebooksGroupedBySection[ebook.section_id].push(ebook);
          });

          this.sections = sections.map(section => {
            if (ebooksGroupedBySection[section.id]) {
              section.ebooks = ebooksGroupedBySection[section.id];
            }
            return section;
          });

          if (sections.length === 0) {
            this.sections = Object.keys(ebooksGroupedBySection).map(section_id => ({
              id: section_id,
              name: 'Searched EBOOKS',
              description: 'Click on View E-Book to display the book you searched for',
              ebooks: ebooksGroupedBySection[section_id],
            }));
          }
        } else {
          if (sections.length === 0) {
            alert("No results found.");
          } else {
            this.sections = sections;
          }
        }

        if (sections.length > 0 && ebooks.length === 0) {
          this.selectedSection = null;
        }
      } catch (error) {
        console.error('Search error:', error);
        alert('An error occurred while searching.');
      }
    },
    goToProfile() {
      this.$router.push('/profile');
    },
    goToMyBooks(){
      this.$router.push('/MyBooks');
    }
  },
  async mounted() {
    this.fetchSections();
  },
};
</script>

<style scoped>
/* Add custom styles if necessary */
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

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
