<template>
    <main class="container pt-4">
        <div>
            <router-link
                class=""
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link>
            |
            <router-link
                class=""
                :to="{name: 'Other Page'}"
            >
                Other Page
            </router-link>
            <router-link
                class=""
                :to="{name: 'Profile Page'}"
            >
                Profile Page
            </router-link>
            <router-link
                class=""
                :to="{name: 'Friend Page'}"
            >
                Friend Page
            </router-link>
        </div>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";
import { useUserStore } from "@/store/userStore"; // Import Pinia store

export default defineComponent({
    components: { RouterView },
    setup() {
        const userStore = useUserStore();

        // Hardcode currentUserId for testing
        userStore.setCurrentUserId(1); // Replace 1 with a valid user ID from your database
        console.log("Hardcoded currentUserId:", userStore.currentUserId); // Debugging output

        return {};
    },
});
</script>

<style scoped>
</style>
