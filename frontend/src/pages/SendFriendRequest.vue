<template>
  <div class="send-request-container">
    <h2 class="text-center mb-4 fw-bold text-primary">Send a Friend Request</h2>

    <!-- Card Wrapper -->
    <div class="card p-4 shadow-lg">
      <!-- Icon -->
      <div class="text-center mb-4">
        <i class="bi bi-person-plus-fill text-primary" style="font-size: 3rem;"></i>
      </div>

      <!-- Input for Username -->
      <div class="form-group mb-3">
        <label for="username" class="form-label fw-semibold text-secondary">Enter Username</label>
        <input
          id="username"
          v-model="toUsername"
          type="text"
          class="form-control form-control-lg"
          placeholder="Type the username of your friend"
        />
      </div>

      <!-- Send Button -->
      <button
        @click="sendRequest"
        class="btn btn-lg btn-primary w-100 fw-bold"
      >
        <i class="bi bi-send-fill me-2"></i>Send Request
      </button>

      <!-- Error Message -->
      <p v-if="errorMessage" class="text-danger mt-3 text-center fw-semibold">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useUserStore } from "../stores/userStore";

export default defineComponent({
  setup() {
    const toUsername = ref("");
    const errorMessage = ref("");
    const userStore = useUserStore();

    const sendRequest = async () => {
      if (!toUsername.value.trim()) {
        errorMessage.value = "Please enter a valid username.";
        return;
      }

      try {
        const response = await fetch("/friend-request/send/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": userStore.csrfToken,
          },
          body: JSON.stringify({ to_username: toUsername.value.trim() }),
        });

        if (response.ok) {
          errorMessage.value = "";
          alert("Friend request sent!");
          toUsername.value = "";
        } else {
          const data = await response.json();
          errorMessage.value = data.error || data.message || "Failed to send friend request.";
        }
      } catch (error) {
        errorMessage.value = "An unexpected error occurred.";
      }
    };

    return {
      toUsername,
      errorMessage,
      sendRequest,
    };
  },
});
</script>

<style scoped>
.send-request-container {
  max-width: 500px;
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

.card {
  background-color: #ffffff;
  border: none;
}

.text-primary {
  color: #007bff !important;
}

.text-danger {
  color: #dc3545 !important;
}
</style>
