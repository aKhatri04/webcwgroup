// src/stores/userStore.ts
import { defineStore } from 'pinia';

export interface Hobby {
  id: number;
  name: string;
}

export interface User {
  id: number;
  name: string;
  email: string;
  date_of_birth: string;
  hobbies: Hobby[];
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: {
      id: 0,
      name: '',
      email: '',
      date_of_birth: '',
      hobbies: [] as Hobby[],
    } as User,
  }),
  actions: {
    async fetchUser() {
      const baseUrl = 'http://localhost:8000';
      const response = await fetch(`${baseUrl}/api/user/`);
      if (response.ok) {
        this.user = await response.json();
      }
    },
    addHobby(newHobby: Hobby) {
      this.user.hobbies.push(newHobby);
    },
    async updateUserProfile() {
      const baseUrl = 'http://localhost:8000';
      await fetch(`${baseUrl}/api/user/${this.user.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(this.user),
      });
    },
  },
});
