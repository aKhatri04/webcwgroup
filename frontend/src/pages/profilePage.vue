<template>
  <div class="container pt-3">
    <div class="h1 text-center border rounded bg-light p-2 mb-3">Profile Page</div>

    <div v-if="isLoading">Loading...</div>
    <div v-else>
      <!-- Profile Table -->
      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Date of Birth</th>
            <th>Hobbies</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.date_of_birth }}</td>
            <td>
              <span v-for="hobby in user.hobbies" :key="hobby.id" class="badge bg-secondary me-1">
                {{ hobby.name }}
              </span>
            </td>
            <td>
              <button class="btn btn-sm btn-primary" @click="editProfile">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useUserStore } from '../stores/userStore';

export default defineComponent({
  setup() {
    const userStore = useUserStore();
    const isLoading = ref(false);

    const fetchUser = async () => {
      isLoading.value = true;
      await userStore.fetchUser();
      isLoading.value = false;
    };

    const editProfile = () => {
      userStore.user.name = prompt('Edit Name:', userStore.user.name) || userStore.user.name;
      userStore.user.email = prompt('Edit Email:', userStore.user.email) || userStore.user.email;
      userStore.updateUserProfile();
      alert('Profile updated successfully!');
    };

    onMounted(() => {
      fetchUser();
    });

    return {
      user: userStore.user,
      fetchUser,
      editProfile,
      isLoading,
    };
  },
});
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}
</style>
