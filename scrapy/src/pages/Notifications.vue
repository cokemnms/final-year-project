<template>
  <div class="page-wrapper">
    <Navbar />

    <div class="main-content">
      <div class="flex justify-between items-center mb-4">
        <button
          class="px-4 py-2 mark" 
          @click="markAllAsRead"
          v-if="notifications.length"
        >
          MARK ALL AS READ
        </button>
      </div>

      <div class="main-center ">
        <div
          class="bg-white rounded-lg notif "
          v-for="notification in notifications.reverse()"  
          :key="notification.id"
          v-if="notifications.length"
        >
          {{ notification.body }}

          <button class="text-green" @click="readNotification(notification)">
            view
          </button>
        </div>

        <div class="container flex" v-else>
          <img src="@/assets/notification.svg" alt="">
          <h1 class="empty-msg">YOU'RE ALL CAUGHT UP!</h1>
        </div>  
      </div>
    </div>

    <Footer/>
  </div>
</template>

<script>
import Navbar from "@/layouts/Navbar.vue";
import Footer from '@/layouts/Footer.vue'
import axios from 'axios'

export default {
  name: 'notifications',
  components: {
    Navbar,
    Footer
  },
  data() {
    return {
      notifications: []
    }
  },
  mounted() {
    this.getNotifications()
  },
  methods: {
    getNotifications() {
      const token = localStorage.getItem('user.access')

      axios
        .get('/api/notifications/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(response => {
          this.notifications = response.data;
        })
        .catch(error => {
          console.log('GET /api/notifications/ error:', error)
        })
    },
    markAllAsRead() {
      const token = localStorage.getItem('user.access')

      axios.post('/api/notifications/read-all/', {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(() => {
        this.notifications = []  // ✅ Remove from UI
        window.dispatchEvent(new Event('refresh-unread'))  // ✅ Update navbar
      })
      .catch(error => {
        console.error('Failed to mark all as read:', error)
      })
    },
    async readNotification(notification) {
      const token = localStorage.getItem('user.access')

      await axios
        .post(`/api/notifications/read/${notification.id}/`, {}, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(response => {
          this.notifications = this.notifications.filter(n => n.id !== notification.id)
          window.dispatchEvent(new Event('refresh-unread'))

          if (
            notification.type_of_notification === 'post_like' ||
            notification.type_of_notification === 'post_comment'
          ) {
            this.$router.push({ name: 'PostView', params: { id: notification.post_id } })
          } else {
            this.$router.push({ name: 'friends', params: { id: notification.created_for_id } })
          }
        })
        .catch(error => {
          console.log('Error marking notification as read:', error)
        })
    }
  }
}
</script>



<style scoped>
.page-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.main-center {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2vh;
  margin-top: 4vh;
  margin-bottom: 4vh;
}

.notif{
  border: 3px solid black;
  width: 40vw;
  height: 7vh;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2vw;
  font-size: 1.1vw;
}
.mark{
  background-color: #9CCC65;
  position: relative;
  top: 2vh;
  border: 3px solid black;
  transition: transform .2s;
  color: white;
  border-radius: 20px;
  font-family: "Concert One", serif;
  font-size: 1.3vw;
  
}

.mark:hover{
  transform: scale(1.1);
  background-color: white;
  color: black;
}

.empty-msg{
  font-size: 6vw;
  font-family: "Concert One", serif;
  text-align: center;
  
}
.container {
  position:relative;
right: 10vw;
color: rgb(51, 51, 51);
}
.container img{
  width: 70vw;
}
</style>