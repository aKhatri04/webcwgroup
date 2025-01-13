<template>
    <div class="container mt-5">
      <h1 class="text-center mb-4">User List</h1>
  
      <!-- Filters -->
      <div class="row mb-4">
        <div class="col-md-4">
          <label for="minAge" class="form-label">Min Age:</label>
          <input
            id="minAge"
            v-model.number="ageMin"
            type="number"
            class="form-control"
            placeholder="Min Age"
          />
        </div>
        <div class="col-md-4">
          <label for="maxAge" class="form-label">Max Age:</label>
          <input
            id="maxAge"
            v-model.number="ageMax"
            type="number"
            class="form-control"
            placeholder="Max Age"
          />
        </div>
        <div class="col-md-4 d-flex align-items-end">
          <button class="btn btn-primary w-100" @click="applyFilters">Filter</button>
        </div>
      </div>
  
      <!-- Tabs -->
      <ul class="nav nav-tabs">
        <li class="nav-item">
          <a
            class="nav-link"
            :class="{ active: activeTab === 'all' }"
            href="#"
            @click="setActiveTab('all')"
          >
            All Users
          </a>
        </li>
        <li
          class="nav-item"
          v-for="hobby in Object.keys(groupedByHobby)"
          :key="hobby"
        >
          <a
            class="nav-link"
            :class="{ active: activeTab === hobby }"
            href="#"
            @click="setActiveTab(hobby)"
          >
            {{ hobby }}
          </a>
        </li>
      </ul>
  
      <!-- Tab Content -->
      <div class="tab-content mt-4">
        <div v-if="activeTab === 'all'">
          <!-- All Users -->
          <ul class="list-group mb-4">
            <li
              v-for="user in allUsers"
              :key="user.id"
              class="list-group-item"
            >
              <strong>{{ user.name }}</strong>
              <ul>
                <li v-for="hobby in user.hobbies" :key="hobby">{{ hobby }}</li>
              </ul>
            </li>
          </ul>
  
          <!-- Pagination Controls -->
          <div class="d-flex justify-content-between">
            <button
              class="btn btn-secondary"
              :disabled="currentPage <= 1"
              @click="fetchData(currentPage - 1)"
            >
              Previous
            </button>
            <button
              class="btn btn-secondary"
              :disabled="currentPage >= totalPages"
              @click="fetchData(currentPage + 1)"
            >
              Next
            </button>
          </div>
        </div>
        <div v-else>
          <!-- Hobby-Specific Tab -->
          <ul class="list-group">
            <li
              v-for="user in groupedByHobby[activeTab]"
              :key="user.id"
              class="list-group-item"
            >
              <strong>{{ user.name }}</strong>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref } from "vue";
  
  export default {
    setup() {
      const allUsers = ref([]);
      const groupedByHobby = ref({});
      const activeTab = ref("all");
      const ageMin = ref(0);
      const ageMax = ref(120);
      const currentPage = ref(1);
      const totalPages = ref(1);
  
      // Fetch data from the API
      const fetchData = async (page = 1) => {
        try {
          const response = await fetch(
            `http://127.0.0.1:8000/users/?age_min=${ageMin.value}&age_max=${ageMax.value}&page=${page}`
          );
          const data = await response.json();
          allUsers.value = data.all_users;
          groupedByHobby.value = data.grouped_by_hobby;
          currentPage.value = data.current_page;
          totalPages.value = data.total_pages;
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      };
  
      const applyFilters = () => {
        currentPage.value = 1; // Reset to the first page
        fetchData(); // Fetch data with updated filters
      };
  
      const setActiveTab = (tab) => {
        activeTab.value = tab;
      };
  
      // Fetch initial data
      fetchData();
  
      return {
        allUsers,
        groupedByHobby,
        activeTab,
        ageMin,
        ageMax,
        currentPage,
        totalPages,
        fetchData,
        applyFilters,
        setActiveTab,
      };
    },
  };
  </script>
  
  <style scoped>
  .nav-link {
    cursor: pointer;
  }
  </style>
  