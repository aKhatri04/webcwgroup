<template>
    <div>
      <h2>Send a Friend Request</h2>
      <input v-model="toUserId" type="number" placeholder="Enter user ID" />
      <button @click="sendRequest">Send Request</button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  
  export default defineComponent({
    setup() {
      const toUserId = ref<number | null>(null);
  
      const sendRequest = async () => {
        if (!toUserId.value) {
          alert('Please enter a valid user ID.');
          return;
        }
        try {
          const response = await fetch('/friend-request/send/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ to_user_id: toUserId.value }),
          });
          if (response.ok) {
            alert('Friend request sent!');
            toUserId.value = null;
          } else {
            const errorData = await response.json();
            alert(errorData.error || 'Failed to send friend request.');
          }
        } catch (error) {
          alert('An unexpected error occurred.');
        }
      };
  
      return { toUserId, sendRequest };
    },
  });
  </script>
  
  <style scoped>
  /* Add styling here if needed */
  </style>
  