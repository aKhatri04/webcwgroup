<template>
  <div class="friend-requests-container">
    <h2 class="text-center mb-4 fw-bold text-primary">Pending Friend Requests</h2>

    <!-- Display Pending Requests -->
    <div v-if="friendRequests.length">
      <ul class="list-group">
        <li
          v-for="request in friendRequests"
          :key="request.id"
          class="list-group-item d-flex justify-content-between align-items-center shadow-sm"
        >
          <span class="fw-semibold">
            <i class="bi bi-person-fill text-primary"></i> 
            <strong>{{ request.from_user.name }}</strong> sent you a friend request.
          </span>
          <div>
            <button
              class="btn btn-outline-success btn-sm me-2"
              @click="acceptRequest(request.id)"
            >
              Accept
            </button>
            <button
              class="btn btn-outline-danger btn-sm"
              @click="rejectRequest(request.id)"
            >
              Reject
            </button>
          </div>
        </li>
      </ul>
    </div>

    <!-- No Pending Requests -->
    <div v-else class="text-center text-muted mt-4">
      <p class="fw-semibold">No pending friend requests.</p>
    </div>
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

<style scoped>
.friend-requests-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 15px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  font-family: "Poppins", sans-serif;
}

h2 {
  color: #007bff;
}

.list-group-item {
  background-color: #ffffff;
  border-radius: 10px;
  border: 1px solid #ddd;
  margin-bottom: 10px;
}

.btn-outline-success:hover {
  background-color: #28a745;
  color: #fff;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: #fff;
}
</style>
