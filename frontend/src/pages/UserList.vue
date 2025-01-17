<template>
    <div class="container mt-5">
      <div class="alert alert-info text-center" v-if="loggedInUser">
        Logged in as: <strong>{{ loggedInUser.name }}</strong> ({{ loggedInUser.email }})
      </div>
  
      <h1 class="text-center mb-4">User List</h1>
  
      <!-- Filters -->
      <div class="row mb-4">
        <div class="col-md-4">
          <label for="minAge" class="form-label">Min Age:</label>
          <input
            id="minAge"
            v-model.number="filters.ageMin"
            type="number"
            class="form-control"
            placeholder="Enter Min Age"
          />
        </div>
        <div class="col-md-4">
          <label for="maxAge" class="form-label">Max Age:</label>
          <input
            id="maxAge"
            v-model.number="filters.ageMax"
            type="number"
            class="form-control"
            placeholder="Enter Max Age"
          />
        </div>
        <div class="col-md-4 d-flex align-items-end">
          <button class="btn btn-primary w-100" @click="applyFilters">Apply Filters</button>
        </div>
      </div>
  
      <!-- User List -->
      <div class="table-responsive">
        <table class="table table-bordered">
          <thead class="table-dark">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Age</th>
              <th>Hobbies</th>
              <th>Shared Hobbies</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.name }}</td>
              <td>{{ user.email }}</td>
              <td>{{ calculateAge(user.date_of_birth) }}</td>
              <td>
                <ul>
                  <li v-for="hobby in user.hobbies" :key="hobby.id">{{ hobby.name }}</li>
                </ul>
              </td>
              <td>
                <ul>
                  <li v-for="shared in user.shared_hobbies" :key="shared.id">
                    {{ shared.name }}: {{ shared.shared_count }} hobbies
                    <ul>
                      <li v-for="hobby in shared.shared_hobbies" :key="hobby.id">
                        {{ hobby.name }}
                      </li>
                    </ul>
                  </li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Pagination Controls -->
      <div class="d-flex justify-content-between mt-4">
        <button
          class="btn btn-secondary"
          :disabled="pagination.current_page === 1"
          @click="fetchUsers(pagination.current_page - 1)"
        >
          Previous
        </button>
        <button
          class="btn btn-secondary"
          :disabled="pagination.current_page === pagination.total_pages"
          @click="fetchUsers(pagination.current_page + 1)"
        >
          Next
        </button>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from "vue";
  
  // Define TypeScript interfaces for your data
  interface Hobby {
    id: number;
    name: string;
  }
  
  interface SharedHobby {
    id: number;
    name: string;
    shared_count: number;
    shared_hobbies: Hobby[];
  }
  
  interface User {
    id: number;
    name: string;
    email: string;
    date_of_birth: string;
    hobbies: Hobby[];
    shared_hobbies: SharedHobby[];
  }
  
  interface LoggedInUser {
    name: string;
    email: string;
  }
  
  export default defineComponent({
    name: "UserList",
    setup() {
      // Properly type and initialize the data properties
      const users = ref<User[]>([]);
      const loggedInUser = ref<LoggedInUser | null>(null);
      const pagination = ref({ total_pages: 1, current_page: 1 });
      const filters = ref({ ageMin: 0, ageMax: 100 });
  
      const fetchLoggedInUser = async () => {
        try {
          const response = await fetch("http://localhost:8000/user/current/", { credentials: "include" });
          if (!response.ok) throw new Error("Failed to fetch logged-in user");
          loggedInUser.value = (await response.json()) as LoggedInUser;
        } catch (error) {
          console.error("Error fetching logged-in user:", error);
        }
      };
  
      const fetchUsers = async (page = 1) => {
        try {
          const pageNumber = typeof page === "number" ? page : 1;
          const response = await fetch(
            `http://localhost:8000/users/?age_min=${filters.value.ageMin}&age_max=${filters.value.ageMax}&page=${pageNumber}`,
            { credentials: "include" }
          );
          if (!response.ok) throw new Error("Failed to fetch users");
          const data = await response.json();
          users.value = data.users as User[];
          pagination.value.total_pages = data.total_pages;
          pagination.value.current_page = data.current_page;
        } catch (error) {
          console.error("Error fetching users:", error);
        }
      };
  
      const applyFilters = () => {
        fetchUsers(); // Apply the current filters when the button is clicked
      };
  
      const calculateAge = (dob: string) => {
        const birthDate = new Date(dob);
        const today = new Date();
        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
          age--;
        }
        return age;
      };
  
      fetchLoggedInUser();
      fetchUsers();
  
      return {
        users,
        loggedInUser,
        pagination,
        filters,
        fetchUsers,
        applyFilters,
        calculateAge,
      };
    },
  });
  </script>
  
  <style scoped>
  h1 {
    text-align: center;
  }
  
  .table {
    margin-top: 20px;
  }
  
  .table-responsive {
    margin-bottom: 20px;
  }
  </style>
  