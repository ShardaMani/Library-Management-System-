<template>
  <div class="container mt-5">
    <h2>{{ ebook.name }}</h2>
    <p><strong>Author: </strong>{{ ebook.author }}</p>
    <hr>
    <div v-html="ebook.content"></div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      ebook: {},
    };
  },
  methods: {
    fetchEbookContent() {
    const ebookId = this.$route.params.ebookId;
    console.log(`Fetching content for ebook ID: ${ebookId}`);
    axios
        .get(`http://127.0.0.1:5000/content/${ebookId}`, {
        headers: {
            'Authentication-Token': localStorage.getItem('authToken'),
        },
        })
        .then((response) => {
        this.ebook = response.data.ebook;
        })
        .catch((error) => {
        console.error('Error fetching ebook content:', error);
        });
    },

  },
  mounted() {
    this.fetchEbookContent();
  },
};
</script>
