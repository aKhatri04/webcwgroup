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
}

export const useUserStore = defineStore("userStore", {
  state: () => ({
    user: {} as User,  // Store the current user
    hobbies: [] as Hobby[],  // Store all available hobbies for dropdown
    csrfToken: "",  // Add csrfToken to the state
    friendRequests: [] as FriendRequest[], // Use the FriendRequest interface here

  }),
  actions: {
    /**
     * Fetch the CSRF token from the meta tag.
     */
    async fetchCsrfToken() {
      const tokenElement = document.querySelector('meta[name="csrf-token"]');
      if (tokenElement) {
        this.csrfToken = tokenElement.getAttribute("content") || "";
        console.log("CSRF token fetched successfully:", this.csrfToken);
      } else {
        console.error("CSRF token not found in meta tag.");
        this.csrfToken = "";
      }
    },

    /**
     * Fetch the currently authenticated user's details.
     */
    async fetchCurrentUser() {
      this.isLoading = true;
      try {
        const response = await fetch("http://localhost:8000/user/current/", {
          method: "GET",
          credentials: "include",
        });
        if (!response.ok) throw new Error("Failed to fetch current user");
        this.user = await response.json();
      } catch (error) {
        this.isAuthenticated = false;
        console.error("Error fetching current user:", error);
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Fetch all available hobbies.
     */
    async fetchHobbies() {
      try {
        const response = await fetch("/hobbies/");
        if (!response.ok) throw new Error("Failed to fetch hobbies");
        const data = await response.json();
        this.hobbies = data.hobbies;
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
          credentials: "include",
        });
  
        if (response.ok) {
          const data = await response.json();
          console.log("Fetched friend requests:", data.pending_requests);
          this.friendRequests = [...data.pending_requests]; // Trigger reactivity
        } else {
          console.error("Failed to fetch friend requests.");
        }
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Handle a failed request gracefully.
     */
    handleFailedRequest(response: Response) {
      if (response.status === 403 || response.status === 401) {
        console.error("Unauthorized access. Redirecting to login.");
        this.isAuthenticated = false;
      } else {
        console.error(`Unexpected response: ${response.status} - ${response.statusText}`);
      }
    },
    
    

    async updateUserProfile(updatedUser: Partial<User>) {
      try {
        const response = await fetch(`/user/${this.user.id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
          body: JSON.stringify(updatedUser),
        });
        if (!response.ok) throw new Error("Failed to update profile");
        this.user = await response.json();
      } catch (error) {
        console.error("Error updating user profile:", error);
      }
    },
  },
});
