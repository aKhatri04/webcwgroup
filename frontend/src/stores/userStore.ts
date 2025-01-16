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
    user: {} as User, // Authenticated user's data
    hobbies: [] as Hobby[], // Available hobbies
    csrfToken: "", // CSRF token for secure requests
    isAuthenticated: false, // Track user's authentication status
    isLoading: false, // Loading state for API calls
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
          credentials: "include", // Ensure cookies are included
        });

        const contentType = response.headers.get("content-type");
        if (!response.ok || !contentType?.includes("application/json")) {
          const errorText = await response.text();
          console.error("Failed to fetch current user:", errorText);
          throw new Error("Non-JSON response received. Check if user is authenticated.");
        }

        const data = await response.json();
        this.user = data;
        this.isAuthenticated = true;
        console.log("User fetched successfully:", this.user);
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
      this.isLoading = true;
      try {
        const response = await fetch("http://localhost:8000/hobbies/", {
          method: "GET",
          credentials: "include", // Ensure cookies are included
        });

        const contentType = response.headers.get("content-type");
        if (!response.ok || !contentType?.includes("application/json")) {
          const errorText = await response.text();
          console.error("Failed to fetch hobbies:", errorText);
          throw new Error("Non-JSON response received.");
        }

        const data = await response.json();
        this.hobbies = data.hobbies || [];
        console.log("Hobbies fetched successfully:", this.hobbies);
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

    /**
     * Update the user's profile.
     */
    async updateUserProfile(updatedUser: Partial<User>) {
      try {
        const response = await fetch(`http://localhost:8000/user/${this.user.id}/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": this.csrfToken,
          },
          body: JSON.stringify(updatedUser),
        });

        const contentType = response.headers.get("content-type");
        if (!response.ok || !contentType?.includes("application/json")) {
          this.handleFailedRequest(response);
          const errorText = await response.text();
          console.error("Failed to update profile:", errorText);
          throw new Error("Non-JSON response received.");
        }

        const data = await response.json();
        this.user = data;
        console.log("Profile updated successfully:", this.user);
      } catch (error) {
        console.error("Error updating user profile:", error);
      }
    },
  },
});
