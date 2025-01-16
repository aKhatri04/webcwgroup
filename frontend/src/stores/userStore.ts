import { defineStore } from "pinia";

interface Hobby {
  id: number;
  name: string;
}

interface User {
  id: number;
  name: string;
  email: string;
  date_of_birth: string;
  hobbies: Hobby[];
  password?: string;
}

interface FriendRequest {
  id: number;
  from_user: { id: number; name: string };
  to_user: { id: number; name: string };
  is_accepted: boolean;
  created_at: string;
}

export const useUserStore = defineStore("userStore", {

  state: () => ({
    user: {} as User,  // Store the current user
    hobbies: [] as Hobby[],  // Store all available hobbies for dropdown
    csrfToken: "",  // Add csrfToken to the state
    friendRequests: [] as FriendRequest[], // Store pending friend requests
  }),
  actions: {
    async fetchCurrentUser() {
      try {
        const response = await fetch("/user/current/", {
          method: "GET",
          credentials: "include", // Important for session-based authentication
        });
        if (!response.ok) throw new Error("Failed to fetch current user");
        this.user = await response.json();
      } catch (error) {
        console.error("Error fetching current user:", error);
      }
    },
    async fetchHobbies() {
      try {
        const response = await fetch("/hobbies/");
        if (!response.ok) throw new Error("Failed to fetch hobbies");
        const data = await response.json();
        this.hobbies = data.hobbies; // Unwrap hobbies list
        console.log("Fetched hobbies:", this.hobbies); // Debug output
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      }
    },

    async fetchCsrfToken() {
      try {
        const tokenElement = document.querySelector('meta[name="csrf-token"]');
        if (tokenElement) {
          this.csrfToken = tokenElement.getAttribute("content") || "";
          console.log("CSRF token fetched:", this.csrfToken);
        } else {
          console.error("CSRF token meta tag not found.");
        }
      } catch (error) {
        console.error("Error fetching CSRF token:", error);
      }
    },

    async fetchFriendRequests() {
      try {
        const response = await fetch("/friend-requests/", {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });
    
        if (!response.ok) {
          console.error("Failed to fetch friend requests:", response.status, response.statusText);
          throw new Error("Failed to fetch friend requests");
        }
    
        const data = await response.json();
        console.log("Fetched friend requests:", data.pending_requests); // Debugging
        this.friendRequests = data.pending_requests; // Update the store
        console.log("Updated friendRequests state:", this.friendRequests); // Debugging
      } catch (error) {
        console.error("Error fetching friend requests:", error);
      }
    },

    async updateUserProfile(updatedUser: Partial<User>) {
      try {
        console.log("CSRF Token:", this.csrfToken);
        console.log("Sending data:", updatedUser);
        const response = await fetch(`/user/${this.user.id}`, {
          method: "PUT",
          headers: { 
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken, // Send CSRF token for security 
           },
          body: JSON.stringify(updatedUser),
        });
        if (!response.ok) throw new Error("Failed to update profile");
        this.user = await response.json();  // Update store with the saved profile data
      } catch (error) {
        console.error("Error updating user profile:", error);
      }
    },
  },
});
