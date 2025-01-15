<template>
    <div>
      <h2>Pending Friend Requests</h2>
      <ul v-if="pendingRequests.length">
        <li v-for="request in pendingRequests" :key="request.id">
          {{ request.from_user.name }} sent you a friend request.
          <button @click="acceptRequest(request.id)">Accept</button>
          <button @click="rejectRequest(request.id)">Reject</button>
        </li>
      </ul>
      <p v-else>No pending friend requests.</p>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive, onMounted } from 'vue';
  
  export default defineComponent({
    setup() {
      const state = reactive({
        pendingRequests: [] as Array<{
          id: number;
          from_user: { id: number; name: string };
        }>,
      });
  
      const fetchPendingRequests = async () => {
        const response = await fetch('/friend-requests/');
        const data = await response.json();
        state.pendingRequests = data.pending_requests;
      };
  
      const acceptRequest = async (requestId: number) => {
        await fetch('/friend-request/handle/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ request_id: requestId, action: 'accept' }),
        });
        fetchPendingRequests(); // Refresh the list
      };
  
      const rejectRequest = async (requestId: number) => {
        await fetch('/friend-request/handle/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ request_id: requestId, action: 'reject' }),
        });
        fetchPendingRequests(); // Refresh the list
      };
  
      onMounted(fetchPendingRequests);
  
      return { ...state, acceptRequest, rejectRequest };
    },
  });
  </script>
  
  <style scoped>
  /* Add styling here */
  </style>
  