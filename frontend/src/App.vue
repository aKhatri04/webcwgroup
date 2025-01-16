<template>
    <div>
      <!-- Navbar at the Top -->
      <div class="navbar-container">
        <div class="title-container">
          <h1 class="app-title">Hobbies App</h1>
        </div>
        <div class="nav-links">
          
          <router-link
            class="nav-link"
            active-class="active"
            :to="{ name: 'Profile Page' }"
          >
            Profile Page
          </router-link>
          <router-link
            class="nav-link"
            active-class="active"
            :to="{ name: 'Send Request Page' }"
          >
            Send Request
          </router-link>
          <router-link
            class="nav-link"
            active-class="active"
            :to="{ name: 'Pending Requests Page' }"
          >
            Pending Requests
          </router-link>
        </div>
      </div>
  
      <!-- Page Content -->
      <main class="container pt-5">
        <RouterView class="flex-shrink-0" />
      </main>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import { RouterView } from "vue-router";
  
  export default defineComponent({
    components: { RouterView },
  });
  </script>
  
  <style scoped>
  /* Styling for Navbar */
  .navbar-container {
    background-color: #ffffff;
    border-bottom: 2px solid #ddd;
    padding: 15px 0;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1030;
  }
  
  /* Title Section */
  .title-container {
    text-align: center;
    margin-bottom: 10px;
  }
  
  .app-title {
    font-size: 2rem;
    color: #007bff;
    font-family: "Poppins", sans-serif;
    font-weight: 600;
    margin: 0;
  }
  
  /* Navigation Links */
  .nav-links {
    display: flex;
    justify-content: center;
    gap: 20px;
  }
  
  .nav-link {
    font-family: "Poppins", sans-serif;
    font-size: 1rem;
    font-weight: 500;
    color: #333;
    text-decoration: none;
    transition: color 0.3s ease-in-out;
  }
  
  .nav-link:hover {
    color: #007bff;
  }
  
  .active {
    color: #007bff !important;
    font-weight: 600;
    text-decoration: underline;
  }
  
  /* Main Content */
  .container {
    margin-top: 120px; /* Adjust for the fixed navbar */
  }
  
  /* Responsiveness */
  @media (max-width: 768px) {
    .app-title {
      font-size: 1.75rem;
    }
  
    .nav-link {
      font-size: 0.9rem;
    }
  
    .nav-links {
      flex-wrap: wrap;
      gap: 10px;
    }
  }
  </style>
  