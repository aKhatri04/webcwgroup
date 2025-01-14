<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">Users with Shared Hobbies</h1>

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

    <!-- User List -->
    <div class="list-group mb-4">
      <div
        v-for="user in users"
        :key="user.id"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <div>
          <strong>{{ user.name }}</strong>
        </div>
        <span class="badge bg-primary rounded-pill">
          {{ user.shared_hobbies }} shared hobbies
        </span>
      </div>
    </div>

    <!-- Pagination Controls -->
    <div class="d-flex justify-content-between">
      <button
        class="btn btn-secondary"
        :disabled="currentPage <= 1"
        @click="fetchUsers(currentPage - 1)"
      >
        Previous
      </button>
      <button
        class="btn btn-secondary"
        :disabled="currentPage >= totalPages"
        @click="fetchUsers(currentPage + 1)"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useUserStore } from "@/store/userStore";

export default {
  setup() {
    const userStore = useUserStore();

    const users = ref([]);
    const ageMin = ref(0);
    const ageMax = ref(120);
    const currentPage = ref(1);
    const totalPages = ref(1);

    const fetchUsers = async (page = 1) => {
      try {
        if (!userStore.currentUserId) {
          console.error("Error: currentUserId is not set in the Pinia store.");
          return;
        }

        const response = await fetch(
          `http://127.0.0.1:8000/users/?age_min=${ageMin.value}&age_max=${ageMax.value}&page=${page}&current_user_id=${userStore.currentUserId}`
        );

        if (!response.ok) {
          throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        users.value = data.users;
        currentPage.value = data.current_page;
        totalPages.value = data.total_pages;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    const applyFilters = () => {
      currentPage.value = 1;
      fetchUsers();
    };

    fetchUsers();

    return { users, ageMin, ageMax, currentPage, totalPages, fetchUsers, applyFilters };
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
}
</style>
