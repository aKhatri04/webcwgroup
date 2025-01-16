<template>
  <div class="profile-page container mt-5">
    <!-- Page Title -->
    <h2 class="text-center mb-4 fw-bold text-primary">User Profile</h2>

    <!-- Profile Card -->
    <div class="card p-4 shadow-lg" style="border-radius: 15px; background-color: #ffffff;">
      <div v-if="loading" class="text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div v-else>
        <!-- Profile Details -->
        <div v-if="!editing">
          <p><strong>Name:</strong> {{ updatedUser.name }}</p>
          <p><strong>Email:</strong> {{ updatedUser.email }}</p>
          <p><strong>Date of Birth:</strong> {{ updatedUser.date_of_birth }}</p>
          <p><strong>Hobbies:</strong>
            <span v-for="hobby in updatedUser.hobbies" :key="hobby.id" class="badge bg-secondary me-1">
              {{ hobby.name }}
            </span>
          </p>
          <button class="btn btn-primary w-100 fw-bold" @click="editProfile">Edit Profile</button>
        </div>

        <!-- Edit Form -->
        <div v-else>
          <div class="form-group mb-3">
            <label for="name" class="form-label fw-bold text-secondary">Name</label>
            <input
              id="name"
              v-model="updatedUser.name"
              type="text"
              class="form-control"
              placeholder="Enter your name"
            />
          </div>
          <div class="form-group mb-3">
            <label for="email" class="form-label fw-bold text-secondary">Email</label>
            <input
              id="email"
              v-model="updatedUser.email"
              type="email"
              class="form-control"
              placeholder="Enter your email"
            />
          </div>
          <div class="form-group mb-3">
            <label for="dob" class="form-label fw-bold text-secondary">Date of Birth</label>
            <input
              id="dob"
              v-model="updatedUser.date_of_birth"
              type="date"
              class="form-control"
            />
          </div>
          <div class="form-group mb-3">
            <label class="form-label fw-bold text-secondary">Hobbies</label>
            <select v-model="selectedHobby" class="form-select mb-2">
              <option value="" disabled>Select an existing hobby</option>
              <option v-for="hobby in hobbies" :key="hobby.id" :value="hobby">{{ hobby.name }}</option>
            </select>
            <button
              class="btn btn-success w-100 mb-2"
              @click="addExistingHobby"
            >
              Add Existing Hobby
            </button>
            <input
              v-model="newHobby"
              type="text"
              class="form-control mb-2"
              placeholder="Enter a new hobby"
            />
            <button
              class="btn btn-primary w-100"
              @click="addNewHobby"
            >
              Add New Hobby
            </button>
          </div>
          <div class="d-flex justify-content-between">
            <button class="btn btn-secondary fw-bold" @click="editing = false">Cancel</button>
            <button class="btn btn-primary fw-bold" @click="saveProfile">Save Changes</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useUserStore } from "../stores/userStore";

interface Hobby {
  id: number;
  name: string;
}

export default defineComponent({
  setup() {
    const store = useUserStore();
    const loading = ref(true);
    const editing = ref(false);
    const updatedUser = ref({ ...store.user });
    const hobbies = ref<Hobby[]>([]);
    const selectedHobby = ref<Hobby | null>(null);
    const newHobby = ref("");

    onMounted(async () => {
      await store.fetchCurrentUser();
      await store.fetchHobbies();
      updatedUser.value = { ...store.user };
      hobbies.value = store.hobbies;
      loading.value = false;
    });

    const editProfile = () => (editing.value = true);

    const addExistingHobby = () => {
      if (
        selectedHobby.value &&
        !updatedUser.value.hobbies.some((hobby) => hobby.id === selectedHobby.value!.id)
      ) {
        updatedUser.value.hobbies.push(selectedHobby.value);
      }
    };

    const addNewHobby = async () => {
      if (!newHobby.value.trim()) return;
      const response = await fetch("/hobbies/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newHobby.value.trim() }),
      });
      const hobby: Hobby = await response.json();
      updatedUser.value.hobbies.push(hobby);
      hobbies.value.push(hobby);
      newHobby.value = "";
    };

    const saveProfile = async () => {
      await store.updateUserProfile(updatedUser.value);
      editing.value = false;
    };

    return {
      loading,
      editing,
      updatedUser,
      hobbies,
      selectedHobby,
      newHobby,
      editProfile,
      addExistingHobby,
      addNewHobby,
      saveProfile,
    };
  },
});
</script>

<style scoped>
/* General Styling */
.profile-page {
  max-width: 600px;
  margin: auto;
}

.card {
  background-color: #f8f9fa;
  border: none;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* Typography */
.text-primary {
  color: #007bff !important;
  font-family: "Poppins", sans-serif;
}

h2 {
  font-family: "Poppins", sans-serif;
  font-weight: bold;
}

/* Form Styling */
.form-control,
.form-select {
  border-radius: 10px;
  font-family: "Poppins", sans-serif; /* Consistent Font */
  font-size: 1rem;
  padding: 10px;
}

/* Button Styling */
.btn-primary {
  background-color: #007bff !important;
  border-color: #0056b3 !important;
}

.btn-secondary {
  background-color: #6c757d !important;
  border-color: #6c757d !important;
}

.btn-success {
  background-color: #28a745 !important;
  border-color: #28a745 !important;
}

.badge {
  font-size: 0.9rem;
  padding: 0.5em;
  font-family: "Poppins", sans-serif;
}
</style>
