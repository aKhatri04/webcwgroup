<template>
    <div class="container pt-3">
      <div class="h1 text-center border rounded bg-light p-2 mb-3">
        Profile Page
      </div>
  
      <pre> {{ }}</pre>
      <!-- User Profile Table -->
      <ProfileTable
        :user="user"
        @update="fetchUser"
      />
    </div>
  </template>
  
  <script>
  import ProfileTable from './profile.vue';
  
  const baseUrl = 'http://localhost:8000';
  
  export default {
    components: {
      ProfileTable,
    },
    data() {
      return {
        user: {},
      };
    },
    /**
     * Lifecycle hook that fetches the user profile data
     * after the component is mounted.
     */
    async mounted() {
      await this.fetchUser();
    },
    methods: {
      async fetchUser() {
        const response = await fetch(`${baseUrl}/api/user/`);
        if (response.ok) {
          this.user = await response.json();
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
    margin: auto;
  }
  </style>
  