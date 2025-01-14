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

export const useUserStore = defineStore("userStore", {
  state: () => ({
    user: {} as User,  // Store the current user
    hobbies: [] as Hobby[],  // Store all available hobbies for dropdown
  }),
  actions: {
    async fetchCurrentUser() {
      try {
        const response = await fetch("http://localhost:8000/api/user/current/", {
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
        const response = await fetch("http://localhost:8000/api/hobbies/");
        if (!response.ok) throw new Error("Failed to fetch hobbies");
        const data = await response.json();
        this.hobbies = data.hobbies; // Unwrap hobbies list
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      }
    },
    async updateUserProfile(updatedUser: Partial<User>) {
      try {
        const response = await fetch(`http://localhost:8000/api/user/${this.user.id}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
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
