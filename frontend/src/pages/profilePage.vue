<template>
    <div class="container pt-3">
      <div class="h1 text-center border rounded bg-light p-2 mb-3">
        {{ greet() }}
        <h2>User Profile</h2>
      </div>
  
      <!-- Profile Info -->
      <div v-if="loading" class="text-center my-3">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <table v-if="!loading" class="table">
        <thead>
          <tr>
            <th>Name: </th>
            <td>{{ updatedUser.name }}</td>
            </tr>
            <tr>
                <th>Email: </th>
                <td>{{ updatedUser.email }}</td>
            </tr>
            <tr>
                <th>Date of Birth: </th>
                <td>{{ updatedUser.date_of_birth }}</td>
            </tr>
            <tr>
                <th>Hobbies: </th>
                <td>
                    <span v-for="hobby in updatedUser.hobbies" :key="hobby.id" class="badge bg-secondary me-1">
                        {{ hobby.name }}
                    </span>
                </td>
                <td>              
                    <button class="btn btn-sm btn-primary" @click="editProfile">Edit</button>
                </td>
          </tr>
        </thead>

      </table>
  
      <!-- Edit Form Modal -->
      <div v-if="editing" class="modal-overlay">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Edit Profile</h5>
              <button type="button" class="btn-close" @click="cancelEdit"></button>
            </div>
            <div class="modal-body">
              <label class="form-label">Name</label>
              <input v-model="updatedUser.name" type="text" class="form-control" />
  
              <label class="form-label mt-2">Email</label>
              <input v-model="updatedUser.email" type="email" class="form-control" />
  
              <label class="form-label mt-2">Date of Birth</label>
              <input v-model="updatedUser.date_of_birth" type="date" class="form-control" />
  
              <!-- Hobby Dropdown -->
              <label class="form-label mt-2">Hobbies</label>
              <select v-model="selectedHobby" class="form-select" @change="addExistingHobby">
                <option value="" disabled>Select an existing hobby</option>
                <option v-for="hobby in hobbies" :key="hobby.id" :value="hobby">
                  {{ hobby.name }}
                </option>
              </select>
  
              <input v-model="newHobbyName" type="text" class="form-control mt-2" placeholder="Or type a new hobby to add" />
              <button class="btn btn-success mt-2" @click="addNewHobby">Add Hobby</button>
  
              <div class="mt-2">
                <span v-for="hobby in updatedUser.hobbies" :key="hobby.id" class="badge bg-secondary me-1">
                  {{ hobby.name }}
                  <button class="btn btn-sm btn-danger ms-1" @click="removeHobby(hobby)">x</button>
                </span>
              </div>
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password (leave blank to keep the same)</label>
              <input v-model="updatedUser.password" type="password" class="form-control" id="password" />
            </div>
            <div class="modal-footer">
              <button class="btn btn-secondary" @click="cancelEdit">Close</button>
              <button class="btn btn-primary" @click="saveChanges">Save Changes</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from "vue";
  import { useUserStore } from "../stores/userStore";
  
  export default defineComponent({
    setup() {
      const userStore = useUserStore();
      const editing = ref(true);
      const selectedHobby = ref<{ id: number; name: string } | null>(null);
      const newHobbyName = ref("");
      const updatedUser = ref({ ...userStore.user });
      const hobbies = ref<{ id: number; name: string }[]>([]);
      const loading = ref(true);
  
      // Fetch current user and hobbies when mounted
      onMounted(async () => {
        try { 
            console.log(1); 
            await userStore.fetchCurrentUser(); 
            console.log(2); 
            await userStore.fetchHobbies(); 
            console.log(3); 
            console.log("User and hobbies fetched successfully!");

            updatedUser.value = { ...userStore.user }; 
            hobbies.value = userStore.hobbies;
            console.log("Hobbies loaded into component:", hobbies.value);
            
        } 
        catch (error) { 
            console.error("Error loading user data:", error); 
        } finally { 
            loading.value = false; 
        }
      });
  
      const greet = () => {
        return `Welcome to your profile, ${userStore.user?.name || "User"}!`;
      };
  
      const editProfile = () => {
        editing.value = true;
        updatedUser.value = { ...userStore.user };
      };
  
      const cancelEdit = () => {
        editing.value = false;
      };
  
      const addNewHobby = () => {
        if (newHobbyName.value.trim()) {
          updatedUser.value.hobbies.push({ id: Date.now(), name: newHobbyName.value });
          newHobbyName.value = "";
        }
      };
  
      const addExistingHobby = () => {
        if (selectedHobby.value && !updatedUser.value.hobbies.some((hobby) => hobby.id === selectedHobby.value!.id)) {
          updatedUser.value.hobbies.push({ ...selectedHobby.value });
          selectedHobby.value = null;
        }
      };
  
      const removeHobby = (hobby: { id: number; name: string }) => {
        updatedUser.value.hobbies = updatedUser.value.hobbies.filter((h) => h.id !== hobby.id);
      };
  
      const saveChanges = async () => {
        try {
          await userStore.updateUserProfile(updatedUser.value);
          alert("Profile updated successfully!");
          editing.value = false;
        } catch (error) {
          console.error("Failed to update profile:", error);
          alert("An error occurred while saving changes.");
        }
      };
  
      return {
        editing,
        selectedHobby,
        newHobbyName,
        updatedUser,
        loading,
        user: userStore.user,
        hobbies,
        greet,
        editProfile,
        cancelEdit,
        addNewHobby,
        addExistingHobby,
        removeHobby,
        saveChanges,
      };
    },
  });
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
    margin: auto;
  }
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .modal-dialog {
    background-color: white;
    border-radius: 10px;
    padding: 1rem;
    width: 100%;
    max-width: 600px;
  }
  </style>
  