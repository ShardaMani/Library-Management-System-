<template>
  <div class="container mt-5">
    <div class="col-md-6 mb-3">
          <button v-if="isAuthenticated" @click="logout" class="btn btn-secondary btn-block">Logout</button>
    </div>
    <div v-if="isLibrarian">Librarian-only content</div>
  </div>
  
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole']),
    isLibrarian() {
      return this.userRole && this.userRole.includes('librarian');
    },
  },
  methods: {
    ...mapActions(['logout']),
  },
};
</script>