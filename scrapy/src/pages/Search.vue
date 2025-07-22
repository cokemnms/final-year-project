<template>
  <Navbar />
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-3 space-y-4">
      <!-- No Matches -->
      <div v-if="!users.length && !posts.length && !scrapPosts.length" class="text-center mt-10">
        <h1 class="text-3xl text-gray-600 font-semibold">😕 Sorry, nothing matches your search.</h1>
      </div>

      <!-- User Carousel -->
      <div class="my-users flex" v-if="users.length">
        <h1>USERS</h1>
        <v-sheet class="mx-auto pa-4 slider" elevation="8" width="1650">
          <v-slide-group v-model="model" show-arrows center-active selected-class="bg-success">
            <v-slide-group-item v-for="user in users" :key="user.id" v-slot="{ isSelected, toggle, selectedClass }">
              <v-card :class="['ma-4 card', selectedClass]" color="grey-lighten-4" height="240" width="200"
                @click="toggle">
                <div class="pa-4 text-center">
                  <v-avatar size="100" class="mx-auto mb-3">
                    <img :src="`https://i.pravatar.cc/300`" alt="User Avatar" />
                  </v-avatar>
                  <div class="font-weight-bold mb-1">
                    <RouterLink :to="{ name: 'UserProfile', params: { id: user.id } }">
                      {{ user.firstName }} {{ user.lastName }}
                    </RouterLink>
                  </div>
                  <button @click.stop="sendDirectMessage(user.id)" v-if="userStore.user.id !== user.id">CHAT</button>
                  <v-scale-transition>
                    <v-icon v-if="isSelected" color="dark" icon="mdi-account-check" size="28"></v-icon>
                  </v-scale-transition>
                </div>
              </v-card>
            </v-slide-group-item>
          </v-slide-group>
        </v-sheet>
      </div>

      <!-- Crafty Posts -->
      <div class="searchpost-container flex" v-if="posts.length">
        <h1>CRAFTY POSTS</h1>
        <div class="posts flex flex-wrap justify-center gap-6">
          <div class="post" v-for="post in displayedPosts" :key="post.id">
            <FeedItem :post="post" />
          </div>
        </div>
        <!-- View More Button -->
        <button style="width: 9vw;" v-if="posts.length > displayedPosts.length" @click="loadMorePosts('posts')">VIEW MORE</button>
      </div>

      <!-- Scrap Posts -->
      <div v-if="actionMessage" :class="['action-banner', actionColor]">
        {{ actionMessage }}
      </div>

      <div v-if="confirmModal.visible" :class="['modal-backdrop', { 'fade-out': confirmModal.animateOut }]">
        <div class="modal scale-in">
          <h3>{{ confirmModal.title }}</h3>
          <p>{{ confirmModal.message }}</p>
          <div class="modal-buttons">
            <button class="confirm-btn" @click="handleModalConfirm">Yes</button>
            <button class="cancel-btn" @click="animateAndCloseModal">No</button>
          </div>
        </div>
      </div>

      <!-- Scrap Posts Loop -->
      <h1 style="position: relative; top: 20vh; left: 17vw;">SCRAP POSTS</h1>
      <div v-if="scrapPosts.length" class="scrap-post-container flex">
        <div v-for="post in scrapPosts" :key="post.id" class="scrap-post ">
          <div class="user-info flex" style="gap: 1vw;" v-if="post.user">
            <img v-if="post.user.avatar" :src="formatAvatar(post.user.avatar)" alt="avatar" class="avatar-img" />
            <div class="user-meta">
              <RouterLink v-if="post.user.id" :to="{ name: 'UserProfile', params: { id: post.user.id } }"
                class="user-link" style="font-size: 1.3vw;">
                {{ post.user.firstName }} {{ post.user.lastName }}
              </RouterLink>
            </div>
          </div>
           <RouterLink :to="{ name: 'ProductDetails', params: { id: post.id } }" class="item-link">

             <img :src="post.attachments?.[0]?.get_image || '/default.jpg'" alt="post image" />
             <h3>{{ post.title }}</h3>
             <p>Rs {{ post.price }}</p>
             <p>{{ post.user.city }}</p>
            </RouterLink>

         <div class="post-actions flex" style="gap: 2vw; font-size: 1.5rem;">
          <button @click="toggleSave(post)" class="action-btn" :title="post.is_saved ? 'Unsave' : 'Save'">
            <i :class="post.is_saved ? 'fas fa-bookmark' : 'far fa-bookmark'"></i>
          </button>
          <button v-if="userStore.user?.id && post.user?.id && userStore.user.id === post.user.id" @click="confirmDelete(post.id)" class="action-btn" title="Delete Post">
            <i class="fas fa-trash-alt"></i>
          </button>
          <button @click="confirmReport(post.id)" class="action-btn" title="Report Post">
            <i class="fas fa-flag"></i>
          </button>
        </div>
        </div>
        <!-- View More Button -->
        <button style="width: 9vw;" v-if="scrapPosts.length > displayedScrapPosts.length" @click="loadMorePosts('scrapPosts')">VIEW MORE</button>
      </div>
    </div>
  </div>
  <div class="main-right col-span-1 space-y-4">
    <!-- Sidebar content -->
  </div>
  <Footer/>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import Navbar from "@/layouts/Navbar.vue";
import FeedItem from '@/components/CraftyComponents/FeedItem.vue'
import Footer from '@/layouts/Footer.vue'

const userStore = useUserStore()
const model = ref(null)
const route = useRoute()
const router = useRouter()

const query = ref(route.query.q || '')
const users = ref([])
const posts = ref([])
const scrapPosts = ref([])

const displayedPosts = ref([]) // To track the posts displayed on the page
const displayedScrapPosts = ref([]) // To track the scrap posts displayed on the page
const actionMessage = ref('')
const actionColor = ref('')
const confirmModal = ref({ visible: false, animateOut: false, type: '', postId: null, title: '', message: '' })
const locationQuery = ref('')
const selectedPriceRange = ref('')

const getFullImageUrl = (imagePath) => {
  if (!imagePath) return '';
  return imagePath.startsWith('http') ? imagePath : `http://localhost:8000${imagePath}`;
};

const formatDate = (datetime) => {
  if (!datetime) return 'N/A';
  const date = new Date(datetime);
  return date.toLocaleDateString(); // Return only the date part
};

const formatAvatar = (avatarPath) => {
  return avatarPath?.startsWith('http') ? avatarPath : avatarPath ? `http://localhost:8000${avatarPath}` : '/default-avatar.png';
};

const applyFilters = () => {
  let result = [...posts.value];
  if (locationQuery.value.trim()) {
    const queryStr = locationQuery.value.trim().toLowerCase();
    result = result.filter(post => post.user?.city?.toLowerCase().includes(queryStr));
  }

  if (selectedPriceRange.value) {
    const [min, max] = selectedPriceRange.value.split('-').map(Number);
    result = result.filter(post => post.price >= min && post.price <= max);
  }

  filteredPosts.value = result;
};

const showBanner = (message, color = 'success') => {
  actionMessage.value = message;
  actionColor.value = color;
  setTimeout(() => {
    actionMessage.value = '';
    actionColor.value = '';
  }, 3000);
};

const confirmDelete = (postId) => {
  confirmModal.value = {
    visible: true,
    animateOut: false,
    type: 'delete',
    postId,
    title: 'Confirm Deletion',
    message: 'Are you sure you want to delete this post?'
  };
};

const confirmReport = (postId) => {
  confirmModal.value = {
    visible: true,
    animateOut: false,
    type: 'report',
    postId,
    title: 'Confirm Report',
    message: 'Are you sure you want to report this post?'
  };
};

const animateAndCloseModal = () => {
  confirmModal.value.animateOut = true;
  setTimeout(() => {
    confirmModal.value.visible = false;
    confirmModal.value.animateOut = false;
  }, 300);
};

const handleModalConfirm = async () => {
  const { type, postId } = confirmModal.value;
  animateAndCloseModal();

  const token = localStorage.getItem('user.access');
  if (!token) return;

  if (type === 'delete') {
    try {
      const res = await fetch(`http://localhost:8000/api/scrap-posts/${postId}/delete/`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        posts.value = posts.value.filter(p => p.id !== postId);
        applyFilters();
        showBanner('Post deleted.', 'danger');
      } else {
        const err = await res.json();
        showBanner(err.error || 'Failed to delete post.', 'danger');
      }
    } catch {
      showBanner('An error occurred.', 'danger');
    }
  } else if (type === 'report') {
  try {
    const res = await fetch(`http://localhost:8000/api/scrap-posts/${postId}/report/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        reason: 'Reported via UI'  // optional reason
      })
    });

    if (res.ok) {
      this.showBanner('Post reported successfully.', 'warning');
    } else {
      const err = await res.json();
      this.showBanner(err.error || 'Failed to report post.', 'danger');
    }
  } catch (err) {
    console.error('Error reporting:', err);
    this.showBanner('An error occurred while reporting.', 'danger');
  }
}

};

const toggleSave = async (post) => {
  try {
    const token = localStorage.getItem('user.access');
    const response = await fetch(`http://localhost:8000/api/scrap-posts/${post.id}/save/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    });

    if (response.ok) {
      post.is_saved = !post.is_saved; // Update the save status immediately
      showBanner(post.is_saved ? 'Post saved!' : 'Post unsaved.', 'success');
    } else {
      const err = await response.json();
      showBanner(err.error || 'Failed to save post.', 'danger');
    }
  } catch (err) {
    console.error('Error saving:', err);
    showBanner('An error occurred.', 'danger');
  }
};

const fetchSearchResults = async (searchTerm) => {
  const token = localStorage.getItem('user.access')

  try {
    const response = await axios.post('/api/search/', { query: searchTerm }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    users.value = response.data.users;
    posts.value = response.data.posts;
    scrapPosts.value = response.data.scrap_posts;

    // Initialize the displayed posts to the first 8
    displayedPosts.value = posts.value.slice(0, 8);
    displayedScrapPosts.value = scrapPosts.value.slice(0, 8);
  } catch (error) {
    console.error('Search error:', error);
  }
};

const loadMorePosts = (type) => {
  if (type === 'posts') {
    const nextPosts = posts.value.slice(displayedPosts.value.length, displayedPosts.value.length + 8);
    displayedPosts.value.push(...nextPosts);
  } else if (type === 'scrapPosts') {
    const nextScrapPosts = scrapPosts.value.slice(displayedScrapPosts.value.length, displayedScrapPosts.value.length + 8);
    displayedScrapPosts.value.push(...nextScrapPosts);
  }
};

const sendDirectMessage = async (userId) => {
  const token = localStorage.getItem('user.access');

  try {
    await axios.get(`/api/chat/${userId}/get-or-create/`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    router.push('/chat');
  } catch (error) {
    console.error('Chat error:', error);
  }
};

watch(
  () => route.query.q,
  (newQuery) => {
    if (newQuery) {
      query.value = newQuery;
      fetchSearchResults(newQuery);
    }
  },
  { immediate: true }
);

</script>

<style scoped>

p{
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
  font-size: 1.3vw;
}

.post {
  width: 22vw;
  min-height: 71vh;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.25);
  border-radius: 30px;
  transition: transform .2s;
}

.post:hover {
  transform: scale(1.03);
}

.posts {
  gap: 2.3vw;
}

::v-deep(.v-slide-group__prev),
::v-deep(.v-slide-group__next) {
  color: black !important;
  opacity: 1 !important;
  font-size: 28px !important;
  z-index: 10;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  width: 45px;
  height: 50px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  position: relative;
  top: 100px;
}

::v-deep(.v-slide-group__prev svg),
::v-deep(.v-slide-group__next svg) {
  fill: black !important;
  stroke: black !important;
  width: 20px;
  height: 20px;
  background-color: black !important;
  color: black !important;
  opacity: 1 !important;
}

.searchpost-container {
  margin-top: 5vh;
  width: 95vw;
  position: relative;
  flex-direction: column;
  right: 14vw;
  gap: 2.3vw;
  top: 15vh;
  flex-wrap: wrap;
}
.scrap-post-container {
  margin-top: 5vh;
  width: 95vw;
  position: relative;
  right: 14vw;
  gap: 2.3vw;
  top: 15vh;
}
.action-btn{
  background-color: white;
  color: black;
  border: none;
}

.my-users {
  position: relative;
  top: 5vh;
  flex-direction: column;
  width: 67vw;
}

h1 {
  font-size: 6vw;
  color: rgb(66, 66, 66);
  font-family: "Concert One", serif;
}

.slider {
  background-color: rgb(175, 211, 175);
  position: relative;
  right: 10vw;
  border: 3px solid black;
  border-radius: 30px;
}

.card {
  border-radius: 30px;
  border: 3px solid black;
}

button {
  width: 7vw;
  height: 5vh;
  border-radius: 30px;
  background-color: #8db161;
  color: white;
  border: 3px solid black;
  font-family: "Concert One", serif;
  font-size: 1.4vw;
  transition: transform .2s;
}

.action-banner {
  position: fixed;
  top: 5vh;
  left: 50%;
  transform: translateX(-50%);
  padding: 1vh 3vw;
  border-radius: 10px;
  font-size: 1.2vw;
  z-index: 9999;
  font-family: 'Gill Sans', sans-serif;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
  animation: slideFade 0.4s ease-out, fadeOut 3s forwards;
}
.success { background-color: #4CAF50; color: white; }
.danger  { background-color: #f44336; color: white; }
.warning { background-color: #ffc107; color: black; }

@keyframes slideFade {
  from { opacity: 0; transform: translate(-50%, -10px); }
  to   { opacity: 1; transform: translate(-50%, 0); }
}
@keyframes fadeOut {
  0%, 85% { opacity: 1; }
  100%   { opacity: 0; }
}

/* Confirmation Modal */
.modal-backdrop {
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  animation: fadeIn 0.3s ease-in forwards;
}
.modal-backdrop.fade-out {
  animation: fadeOutBackdrop 0.3s ease-out forwards;
}
.modal {
  background: white;
  padding: 2vw;
  border-radius: 10px;
  width: 30vw;
  text-align: center;
  box-shadow: 0 0 20px rgba(0,0,0,0.25);
}
.modal-buttons {
  margin-top: 2vh;
  display: flex;
  justify-content: space-evenly;
}
.confirm-btn {
  background: #d9534f;
  color: white;
  padding: 0.5vh 2vw;
  border-radius: 5px;
  border: none;
  font-size: 1vw;
  cursor: pointer;
}
.cancel-btn {
  background: #6c757d;
  color: white;
  padding: 0.5vh 2vw;
  border-radius: 5px;
  border: none;
  font-size: 1vw;
  cursor: pointer;
}
.confirm-btn:hover { background: #c9302c; }
.cancel-btn:hover  { background: #5a6268; }

/* Modal animation */
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
@keyframes fadeOutBackdrop {
  from { opacity: 1; }
  to   { opacity: 0; }
}
.scale-in {
  animation: scaleIn 0.3s ease-in-out;
}
@keyframes scaleIn {
  from { transform: scale(0.95); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}

/* Existing Styles */
.truncate-title {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}
.scrap-post {
   width: 20vw;
  height: 60vh;
  margin: 2vh;
  padding: 10px;
  border: 2px solid lightgray;
  border-radius: 20px;
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-family: 'Concert One', serif;
  color: black;
  transition: transform .2s;
}

.scrap-post img {
  width: 100%;
  height: 30vh;
  object-fit: cover;
  border-radius: 10px;
}

.avatar-img {
  width: 45px !important;
  height: 45px !important;
  border-radius: 50px !important;
}

</style>
