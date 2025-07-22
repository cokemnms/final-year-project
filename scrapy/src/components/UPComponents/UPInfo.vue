<template>
  <Navbar />
  <div class="container flex" v-if="user">
    <div class="otherInfo flex" v-if="userStore.user && userStore.user.id === user.id">
      <div class="savedItems flex">
        <h1 style="font-size: 3vw;">LISTINGS MANAGEMENT</h1>
        <router-link to="/MyListings"><button class="button">VIEW</button></router-link>
      </div>
      <div class="listingManagement flex">
        <h1 style="font-size: 3vw;">SAVED POSTS</h1>
        <router-link to="/Saved"><button class="button">VIEW</button></router-link>
      </div>
      <div class="userSettings flex">
        <h1 style="font-size: 3vw;">EDIT PROFILE</h1>
        <router-link to="/editProfile"><button class="button">VIEW</button></router-link>
      </div>
    </div>



    <div class="otherUser " v-if="userStore.user && userStore.user.id !== user.id">
      <div class="otherUserPosts flex">
        <div class="other-scrap flex">
          <h1 style="font-size: 3vw;">SCRAP POSTS</h1>
          <router-link :to="{ name: 'OtherScrap', params: { id: user.id } }"><button
              class="button">VIEW</button></router-link>
        </div>
        <div class="other-craft flex">
          <h1 style="font-size: 3vw;">CRAFTY POSTS</h1>
          <router-link :to="{ name: 'OthersCrafty', params: { id: user.id } }"><button
              class="button">VIEW</button></router-link>
        </div>

        <div class="other-auction flex">
          <h1 style="font-size: 3vw;">AUCTIONS</h1>
       <router-link :to="`/profile/${user.id}/auctions`">
  View Auctions
</router-link>


        </div>
      </div>
    </div>





    <div class="userinfo flex">
      <div class="info flex">
        <div class="pic flex">
          <img :src="getAvatarUrl(user.avatar)" alt="Avatar" />
        </div>

        <!-- Hidden file input -->
        <input type="file" ref="fileInput" @change="handleAvatarUpload" accept="image/*" style="display: none;" />

        <!-- Visible button -->
        <div v-if="userStore.user.id === user.id" style="margin-top: 1vh; text-align: center;">
          <button @click="$refs.fileInput.click()" class="change-avatar-button">
            CHANGE AVATAR
          </button>
        </div>



        <div class="headerInfo flex">
          <h1>{{ user.firstName }} {{ user.lastName }}</h1>
          <p>{{ user.email }}</p>
          <p>{{ user.number }}</p>
          <p>{{ user.city }}</p>

          <button @click="sendDirectMessage" v-if="userStore.user.id !== user.id">
            CHAT
          </button>
          <button @click="reportUser(user.id)" v-if="userStore.user.id !== user.id">
            REPORT
          </button>
          <button v-if="userStore.user.id === user.id">LOG OUT</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import Navbar from "@/layouts/Navbar.vue";

export default {
  name: 'UPInfo',
  components: { Navbar },
  props: { user: Object },
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  methods: {
    showBanner(message, color = 'success') {
  alert(message);  // or replace with your custom banner system
},
    getAvatarUrl(avatar) {
      if (!avatar) return '/default-avatar.png'; // make sure this exists in /public

      // Case: full URL already
      if (avatar.startsWith('http')) return avatar;

      // Case: relative media path from Django
      return `http://127.0.0.1:8000${avatar}`;
    },
    sendDirectMessage() {
      axios
        .get(`/api/chat/${this.$route.params.id}/get-or-create/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('user.access')}`
          }
        })
        .then(() => this.$router.push('/chat'))
        .catch(console.error);
    },
    handleAvatarUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('avatar', file);

      axios
        .put('/api/upload-avatar/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('user.access')}`
          }
        })
        .then((res) => {
          this.user.avatar = res.data.avatar_url;
          // update it in userStore as well for consistency
          if (this.userStore.user.id === this.user.id) {
            this.userStore.user.avatar = res.data.avatar_url;
          }
          alert("Avatar updated!");
        })
        .catch((err) => {
          console.error(err);
          alert("Failed to upload avatar.");
        });
    },
    async reportUser(userId) {
  const token = localStorage.getItem('user.access');
  try {
    const res = await fetch(`http://localhost:8000/api/users/${userId}/report/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    const data = await res.json();
    if (res.ok) {
      this.showBanner(data.message, 'warning');
    } else {
      this.showBanner(data.error || 'Could not report user.', 'danger');
    }
  } catch (err) {
    this.showBanner('Error reporting user.', 'danger');
    console.error(err);
  }
}

  }
};
</script>

<style scoped>
img {
  width: 11vw;
  height: 23vh;
  border-radius: 50%;
}

.pic {
  border: 4px solid #000000;
  width: 20vw;
  background-color: white;
  height: 30vh;
  border-radius: 30px;
}

p {
  color: grey;
}

.userinfo {
  flex-direction: column;
  width: 25vw;
  height: 95vh;
  border-radius: 30px;
  background-color: s;
  border: 4px solid black;
  background-color: rgb(149, 194, 149);
}

.headerInfo {
  flex-direction: column;
  gap: 2vh;
  width: 20vw;
  height: 50vh;
  border-radius: 30px;
  background-color: white;
  font-size: 1.5vw;
  border: 4px solid #000000;
}

.headerInfo button {
  width: 8vw;
  font-size: 1.4vw;
  height: 6vh;
  color: white;
  border-radius: 30px;
  background-color: lightgreen;
  font-family: "Concert One", serif;
  border: 3px solid black;
  transition: transform 0.2s;
}

h1 {
  font-family: "Concert One", serif;
  color: rgb(68, 68, 68);
}

.container {
  width: 100vw;
  height: 100vh;
  gap: 6vw;
  position: relative;
  top: 6vh;
  left: 10vw;
}

.info {
  flex-direction: column;
  gap: 2vh;
}

.otherInfo,
.otherUserPosts {
  width: 50vw;
  height: 95vh;
  border: 4px solid black;
  flex-direction: column;
  background-color: rgb(149, 194, 149);
  gap: 4vh;
  border-radius: 30px;
}

.savedItems,
.listingManagement,
.userSettings,
.other-craft,
.other-scrap,
.other-auction {
  width: 40vw;
  height: 25vh;
  border: 4px solid #000000;
  flex-direction: column;
  gap: 2vh;
  border-radius: 30px;
  background-color: white;
}

.button {
  width: 7vw;
  height: 5vh;
  border-radius: 30px;
  background-color: #8db161;
  color: white;
  border: 3px solid black;
  font-family: "Concert One", serif;
  font-size: 1.4vw;
  transition: transform 0.2s;
}

.button:hover,
.headerInfo button:hover {
  background-color: white;
  color: black;
  transform: scale(1.1);
}

.change-avatar-button {
  padding: 8px 16px;
  background-color: #79aa7b;
  color: white;
  cursor: pointer;
  border: 3px solid black;
  border-radius: 30px;
}

.change-avatar-button:hover {
  background-color: #ffffff;
  color: rgb(0, 0, 0);
}
</style>
