<template>
  <div>
    <h2>Profile</h2>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <p>Name: {{ updatedUser.name }}</p>
      <p>Email: {{ updatedUser.email }}</p>
      <p>Date of Birth: {{ updatedUser.date_of_birth }}</p>
      <p>Hobbies:
        <span v-for="hobby in updatedUser.hobbies" :key="hobby.id">{{ hobby.name }}</span>
      </p>
      <button @click="editProfile">Edit</button>
    </div>
    <div v-if="editing">
      <input v-model="updatedUser.name" placeholder="Name" />
      <input v-model="updatedUser.email" placeholder="Email" />
      <input v-model="updatedUser.date_of_birth" type="date" placeholder="Date of Birth" />
      <select v-model="selectedHobby">
        <option v-for="hobby in hobbies" :key="hobby.id" :value="hobby">{{ hobby.name }}</option>
      </select>
      <button @click="addExistingHobby">Add Hobby</button>
      <input v-model="newHobby" placeholder="New Hobby" />
      <button @click="addNewHobby">Create Hobby</button>
      <button @click="saveProfile">Save</button>
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
      if (selectedHobby.value && !updatedUser.value.hobbies.some(hobby => hobby.id === selectedHobby.value!.id)) {
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
