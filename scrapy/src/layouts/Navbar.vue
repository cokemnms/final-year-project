<template>
  
  <nav class="flex sticky-nav">
    <router-link to="/MainPage">
      <h1>SCRAPY</h1>
    </router-link>
    <form @submit.prevent="handleSearch" class="search-container">
  <input
    v-model="navbarSearch"
    type="search"
    name="search"
    placeholder="Search for items"
    class="search-input"
  />

</form>

    <div class="navigation flex">
      <router-link to="/DisplayCategories"><button>SELL</button></router-link>

      <router-link to="/MainPage">
        <img width="50" height="50" src="https://img.icons8.com/ios/50/home--v3.png" alt="home--v3"/>
      </router-link>

      <router-link to="/recommendations">
        <img width="50" height="50" src="https://img.icons8.com/ios/50/shop--v1.png" alt="shop--v1"/>
      </router-link>

      <router-link to="/Crafty">
        <img width="50" height="50" src="https://img.icons8.com/ios/50/carpenter.png" alt="carpenter" />
      </router-link>
  <router-link to="/InitialAuction">
        <img width="50" height="50" src="https://img.icons8.com/external-smashingstocks-detailed-outline-smashing-stocks/48/external-Auction-politics-smashingstocks-detailed-outline-smashing-stocks.png" alt="external-Auction-politics-smashingstocks-detailed-outline-smashing-stocks"/>
      </router-link>
     

      <router-link to="/chat" class="relative inline-block">
       <img width="50" height="50" src="https://img.icons8.com/ios/50/filled-chat.png" alt="filled-chat"/>
        <span v-if="hasUnreadMessages" class="unread-dot"></span>
      </router-link>

      <router-link to="/Notifications" class="relative inline-block">
       <img width="50" height="50" src="https://img.icons8.com/forma-thin/50/appointment-reminders.png" alt="appointment-reminders"/>
        <span v-if="hasUnreadNotifications" class="unread-dot"></span>
      </router-link>
 <template v-if="userStore.user.isAuthenticated && userStore.user.id">
        <router-link :to="{ name: 'UserProfile', params: { id: userStore.user.id } }">
          <img width="50" height="50" src="https://img.icons8.com/forma-thin/50/guest-male.png" alt="guest-male" />
        </router-link>
      </template>
     <button @click="handleLogout" class="logout-button" style="background: none; border: none; cursor: pointer; width: 2.5vw;">
        <img width="50" height="50" src="https://img.icons8.com/sf-regular/50/exit.png" alt="logout" />
      </button>
    
    </div>

    <hr class="navbar-underline" />
  </nav>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  name: 'Navbar',
  setup() {
    const userStore = useUserStore()
    const hasUnreadMessages = ref(false)
    const hasUnreadNotifications = ref(false)
    const navbarSearch = ref('')
    const router = useRouter()
    const route = useRoute()

const checkUnreadMessages = () => {
  const token = localStorage.getItem('user.access')
  axios.get('/api/chat/messages/unread/', {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(response => {
      hasUnreadMessages.value = response.data.has_unread
    })
    .catch(error => console.error('Error checking unread messages:', error))
}

const checkUnreadNotifications = () => {
  const token = localStorage.getItem('user.access')
  axios.get('/api/notifications/', {
    headers: { Authorization: `Bearer ${token}` }
  })
    .then(response => {
      hasUnreadNotifications.value = response.data.length > 0
    })
    .catch(error => console.error('Error checking unread notifications:', error))
}
  const handleLogout = () => {
    userStore.logout()
    localStorage.removeItem('user.access')
    localStorage.removeItem('user.refresh')
    localStorage.setItem('logoutMessage', 'true')

    router.push('/')  // redirect to login/home page
  }


    const handleSearch = () => {
      if (navbarSearch.value.trim()) {
        router.push({ path: '/search', query: { q: navbarSearch.value.trim() } })
      }
    }

    onMounted(() => {
      if (route.path === '/search' && route.query.q) {
        navbarSearch.value = route.query.q
      }

      checkUnreadMessages()
      checkUnreadNotifications()
      setInterval(() => {
        checkUnreadMessages()
        checkUnreadNotifications()
      }, 15000)

      window.addEventListener('refresh-unread', () => {
        checkUnreadMessages()
        checkUnreadNotifications()
      })
    })

    onUnmounted(() => {
      window.removeEventListener('refresh-unread', () => {
        checkUnreadMessages()
        checkUnreadNotifications()
      })
    })

    return {
      userStore,
      hasUnreadMessages,
      hasUnreadNotifications,
      navbarSearch,
      handleSearch,
      handleLogout 
    }
  }
}
</script>

<style scoped>
nav {
  position: sticky;
  top: 0;
  background-color:rgb(255, 255, 255);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 20px;
  border-bottom: 1px solid #e6e6e6;
  gap: 5vw;
}
.search-container {
  position: relative;
  width: 30vw;
}
.navigation{
  gap: 1.5vw;
}
.search-input {
  width: 30vw;
  border: 2px solid black;
  outline: none;
  padding: 8px 35px 8px 10px; /* padding-right for icon space */
  font-size: 16px;
  box-sizing: border-box;
  border-radius: 30px;
  height: 7vh;
}

.search-button {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  border: none;
  background: transparent;
  padding: 0;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;

}
button{
    background-color: rgb(149, 194, 149);
    font-family: "Concert One", serif;
    color: white;
    border-radius: 30px;
    border: 4px solid black;
    width: 6.5vw;
    height: 5.5vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.5vw;
}
.search-button img {
  display: block;
}
h1{
  font-family: "Concert One", serif;
  font-size: 4vw;
  color: rgb(149, 194, 149);
}


</style>