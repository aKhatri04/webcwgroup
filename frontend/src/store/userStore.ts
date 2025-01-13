import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  state: () => ({
    currentUserId: null as number | null, // Allow both number and null
  }),
  actions: {
    setCurrentUserId(id: number) {
      this.currentUserId = id;
    },
  },
});
