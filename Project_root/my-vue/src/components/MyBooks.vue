<template>
  <div class="container">
    <h2 class="my-4">My Issued Books</h2>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Book Name</th>
          <th>Author</th>
          <th>Date of Return</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in books" :key="book.id">
          <td>{{ book.ebook_name }}</td>
          <td>{{ book.author }}</td>
          <td>{{ formatDate(book.date_of_return) }}</td>
          <td>
            <button class="btn btn-primary" @click="openFeedbackBox(book)">
              Return Book
            </button>
            <button class="btn btn-info" @click="goToContentPage(book.id)">
              Read Book
            </button>
            <div v-if="book.feedback">
              <strong>Feedback:</strong> {{ book.feedback.feedback }}
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Feedback Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h5 class="modal-title">Submit Feedback</h5>
          <button type="button" class="close" @click="closeModal">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <textarea
            v-model="feedback"
            class="form-control"
            rows="4"
            placeholder="Write your feedback"
          ></textarea>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">
            Close
          </button>
          <button type="button" class="btn btn-primary" @click="submitFeedback">
            Submit Feedback
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      books: [],
      selectedBook: null,
      feedback: "",
      showModal: false,
    };
  },
  mounted() {
    this.fetchMyBooks();
  },
  methods: {
    fetchMyBooks() {
      axios
        .get("http://127.0.0.1:5000/mybooks", {
          headers: {
            'Content-Type': 'application/json',
            "Authentication-Token": localStorage.getItem("authToken"),
          },
        })
        .then((response) => {
          this.books = response.data.books;
          console.log('Fetched books:', this.books);
        })
        .catch((error) => {
          console.error("Error fetching issued books:", error);
        });
    },
    formatDate(date) {
      if (!date) return "";
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    openFeedbackBox(book) {
      this.selectedBook = book;
      this.feedback = "";
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
    },
    submitFeedback() {
      axios
        .post(
          `http://127.0.0.1:5000/ebooks/${this.selectedBook.id}/review`,
          {
            feedback: this.feedback,
          },
          {
            headers: {
              "Authentication-Token": localStorage.getItem("authToken"),
            },
          }
        )
        .then((response) => {
          alert("Feedback submitted successfully!");

          // Remove the returned book from the list
          this.books = this.books.filter(book => book.id !== this.selectedBook.id);

          this.closeModal();
        })
        .catch((error) => {
          console.error("Error submitting feedback:", error);
        });
    },
    goToContentPage(ebookId) {
  console.log('Navigating to ebook content with ID:', ebookId);  // Add this line for debugging
  this.$router.push({ name: 'Content', params: { ebookId: ebookId } });
}
  },
    
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
