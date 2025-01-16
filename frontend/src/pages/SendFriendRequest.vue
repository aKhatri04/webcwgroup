<template>
    <div>
      <h2>Send a Friend Request</h2>
      <input v-model="toUsername" type="text" placeholder="Enter username" />
      <button @click="sendRequest">Send Request</button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from "vue";
  
  export default defineComponent({
    setup() {
      const toUsername = ref<string>("");
  
      const sendRequest = async () => {
        if (!toUsername.value.trim()) {
          alert("Please enter a valid username.");
          return;
        }
  
        try {
          const response = await fetch("/friend-request/send/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCookie("csrftoken"), // Fetch CSRF token
            },
            body: JSON.stringify({ to_username: toUsername.value.trim() }),
          });
  
          if (response.ok) {
            alert("Friend request sent!");
            toUsername.value = ""; // Clear the input
          } else {
            const errorData = await response.json();
            alert(errorData.error || "Failed to send friend request.");
          }
        } catch (error) {
          console.error("Error sending friend request:", error);
          alert("An unexpected error occurred.");
        }
      };
  
      const getCookie = (name: string) => {
        const cookies = document.cookie.split(";");
        for (const cookie of cookies) {
          const [key, value] = cookie.trim().split("=");
          if (key === name) return value;
        }
        return "";
      };
  
      return { toUsername, sendRequest };
    },
  });
  </script>
  
  <style scoped>
  /* Add your styling here */
  </style>
  