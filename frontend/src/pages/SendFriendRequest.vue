<template>
  <div>
    <h2>Send a Friend Request</h2>
    <input v-model="toUsername" type="text" placeholder="Enter username" />
    <button @click="sendRequest">Send Request</button>
    <p v-if="errorMessage" class="text-danger">{{ errorMessage }}</p>
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
        console.error("Error sending friend request:", error);
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
.text-danger {
  color: red;
}
</style>
