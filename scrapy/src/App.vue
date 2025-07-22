<template>
  <router-view />
</template>

<script>
import { onMounted } from 'vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user.js'

export default {
  name: 'App', // or 'MainLayout' depending on your structure
  setup() {
    const userStore = useUserStore()

    onMounted(async () => {
      const token = localStorage.getItem('user.access')
      const refresh = localStorage.getItem('user.refresh')

      if (token && !userStore.user.id) {
        try {
          const response = await axios.get('/api/me/', {
            headers: {
              Authorization: `Bearer ${token}`
            }
          })

          userStore.user = {
            id: response.data.id,
            firstName: response.data.firstName,
            lastName: response.data.lastName,
            email: response.data.email,
            number: response.data.number,
            access: token,
            refresh: refresh,
            isAuthenticated: true
          }

          console.log('✅ User restored from token:', userStore.user)
        } catch (error) {
          console.error('❌ Failed to restore user:', error)
          // Optional: clear token if invalid
          localStorage.removeItem('user.access')
          localStorage.removeItem('user.refresh')
        }
      }
    })

    return {}
  }
}
</script>


<style>
/* Global styles if needed */
</style>
