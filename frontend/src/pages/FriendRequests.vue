<template>
  <div>
    <h2>Pending Friend Requests</h2>
    <ul v-if="friendRequests.length">
      <li v-for="request in friendRequests" :key="request.id">
        {{ request.from_user.name }} sent you a friend request.
        <button @click="acceptRequest(request.id)">Accept</button>
        <button @click="rejectRequest(request.id)">Reject</button>
      </li>
    </ul>
    <p v-else>No pending friend requests.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { useUserStore } from "../stores/userStore";

export default defineComponent({
  setup() {
    const userStore = useUserStore();

    // Fetch pending requests when the component is mounted
    onMounted(() => {
      userStore.fetchFriendRequests();
    });

    const acceptRequest = async (requestId: number) => {
      try {
        await fetch("/friend-request/handle/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": userStore.csrfToken,
          },
          body: JSON.stringify({ request_id: requestId, action: "accept" }),
        });
        userStore.fetchFriendRequests(); // Refresh the list
      } catch (error) {
        console.error("Error accepting friend request:", error);
      }
    };

    const rejectRequest = async (requestId: number) => {
      try {
        await fetch("/friend-request/handle/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": userStore.csrfToken,
          },
          body: JSON.stringify({ request_id: requestId, action: "reject" }),
        });
        userStore.fetchFriendRequests(); // Refresh the list
      } catch (error) {
        console.error("Error rejecting friend request:", error);
      }
    };

    return {
      friendRequests: userStore.friendRequests,
      acceptRequest,
      rejectRequest,
    };
  },
});
</script>
