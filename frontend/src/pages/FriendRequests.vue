<template>
  <div>
    <h2>Pending Friend Requests</h2>

    <!-- Display Pending Requests -->
    <ul v-if="friendRequests.length">
      <li v-for="request in friendRequests" :key="request.id">
        {{ request.from_user.name }} sent you a friend request.
        <button @click="acceptRequest(request.id)">Accept</button>
        <button @click="rejectRequest(request.id)">Reject</button>
      </li>
    </ul>

    <!-- No Pending Requests -->
    <p v-else>No pending friend requests.</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, computed } from "vue";
import { useUserStore } from "../stores/userStore";

export default defineComponent({
  setup() {
    const userStore = useUserStore();

    // Fetch friend requests on mount
    onMounted(async () => {
      console.log("Fetching friend requests on mount...");
      await userStore.fetchFriendRequests();
    });

    // Reactive friendRequests from the store
    const friendRequests = computed(() => userStore.friendRequests);

    const acceptRequest = async (requestId: number) => {
      try {
        const response = await fetch("/friend-request/handle/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": userStore.csrfToken,
          },
          body: JSON.stringify({ request_id: requestId, action: "accept" }),
        });

        if (response.ok) {
          alert("Friend request accepted!");
          await userStore.fetchFriendRequests(); // Re-fetch the list
        } else {
          const error = await response.json();
          console.error("Error accepting friend request:", error);
        }
      } catch (error) {
        console.error("Error accepting friend request:", error);
      }
    };

    const rejectRequest = async (requestId: number) => {
      try {
        const response = await fetch("/friend-request/handle/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": userStore.csrfToken,
          },
          body: JSON.stringify({ request_id: requestId, action: "reject" }),
        });

        if (response.ok) {
          alert("Friend request rejected!");
          await userStore.fetchFriendRequests(); // Re-fetch the list
        } else {
          const error = await response.json();
          console.error("Error rejecting friend request:", error);
        }
      } catch (error) {
        console.error("Error rejecting friend request:", error);
      }
    };

    return {
      friendRequests,
      acceptRequest,
      rejectRequest,
    };
  },
});
</script>

