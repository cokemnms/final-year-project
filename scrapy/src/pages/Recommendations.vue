<template>
  <Navbar />

  <!-- Action Banner -->
  <transition name="banner-slide">
    <div v-if="actionMessage" :class="['action-banner', actionColor]">
      {{ actionMessage }}
    </div>
  </transition>

  <!-- Confirmation Modal -->
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

  <div class="recommendHead flex">
    <h1>DONT MISS OUT <br /> ON THESE!</h1>
    <img style="width: 40vw;" src="@/assets/recommend.gif" alt="" />
  </div>

  <h1 class="mainH1">TOP PICKS FOR YOU</h1>

  <div class="mainCont flex justify-center">
    <!-- Crafty Posts -->
    <div class="craftyRec">
      <div v-if="craftyPosts.length || fallbackCrafty.length">
        <h2 class="subHeading">CRAFTY POSTS</h2>
        <div class="crafty-posts">
          <div v-for="post in displayedCraftyPosts" class="posts flex  justify-center gap-6">
          
  
              <FeedItem  :key="post.id" :post="post" :customSize="{ width: '21vw', height: 'auto' }"
              />
           
            </div>

        </div>
        <!-- View More Button -->
        <button class="viewMore" v-if="craftyPosts.length > displayedCraftyPosts.length"
          @click="loadMorePosts('crafty')">
          VIEW MORE
        </button>
      </div>
    </div>

    <!-- Scrap Posts -->
    <div class="scrapRec">
      <div v-if="scrapPosts.length || fallbackScrap.length">
        <h2 class="subHeading">SCRAP POSTS</h2>
        <div class="postss flex flex-wrap justify-center gap-6">
          <RouterLink v-for="scrap in displayedScrapPosts" :key="scrap.id" :to="`/scrap-posts/${scrap.id}`">
            <div class="scrap-post flex">
              <div class="user-info flex">
                <img v-if="scrap.user && scrap.user.avatar"
                  :src="scrap.user.avatar.startsWith('http') ? scrap.user.avatar : 'http://localhost:8000' + scrap.user.avatar"
                  alt="avatar" class="avatar-img" style="width: 2vw; height: 4vh; border-radius: 50px;" />
                <p>{{ scrap.user?.firstName }} {{ scrap.user?.lastName }}</p>
              </div>
              <img v-if="scrap.attachments && scrap.attachments.length" :src="scrap.attachments[0].get_image"
                class="w-48 h-48 object-cover rounded-lg shadow" />

              <div class="text-center mt-2 scrap-info">
                <p class="font-bold">{{ scrap.title }}</p>
                <p class="text-gray-500">Rs {{ scrap.price }}</p>
                <p class="text-gray-400 text-sm">{{ formatDate(scrap.created_at) }}</p>
                <p class="text-gray-400 text-sm">{{ scrap.user?.city || 'City not set' }}</p>
              </div>

              <!-- Actions -->
              <div class="post-actions flex">
                <button @click.prevent="toggleSave(scrap)" class="action-btn"
                  :title="scrap.is_saved ? 'Unsave' : 'Save'">
                  <i :class="scrap.is_saved ? 'fas fa-bookmark' : 'far fa-bookmark'"></i>
                </button>
                <button v-if="userStore.user.id === scrap.user?.id" @click.prevent="confirmDelete(scrap.id)"
                  class="action-btn" title="Delete Post">
                  <i class="fas fa-trash-alt"></i>
                </button>
                <button @click.prevent="confirmReport(scrap.id)" class="action-btn" title="Report Post">
                  <i class="fas fa-flag"></i>
                </button>
              </div>
            </div>
          </RouterLink>
        </div>
        <!-- View More Button -->
        <button v-if="scrapPosts.length > displayedScrapPosts.length" @click="loadMorePosts('scrap')">
          VIEW MORE
        </button>
      </div>
    </div>
  </div>
  <Footer />
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import Navbar from "@/layouts/Navbar.vue";
import FeedItem from '@/components/CraftyComponents/FeedItem.vue';
import Footer from '@/layouts/Footer.vue'

const router = useRouter();
const userStore = useUserStore();

const craftyPosts = ref([]);
const scrapPosts = ref([]);
const fallbackCrafty = ref([]);
const fallbackScrap = ref([]);

const displayedCraftyPosts = ref([]); // To track the crafty posts displayed on the page
const displayedScrapPosts = ref([]); // To track the scrap posts displayed on the page

const actionMessage = ref('');
const actionColor = ref('');

const confirmModal = ref({
  visible: false,
  animateOut: false,
  type: '',
  postId: null,
  title: '',
  message: ''
});

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function showBanner(message, color = 'success') {
  actionMessage.value = message;
  actionColor.value = color;
  setTimeout(() => {
    actionMessage.value = '';
    actionColor.value = '';
  }, 3000);
}

function confirmDelete(postId) {
  confirmModal.value = {
    visible: true,
    animateOut: false,
    type: 'delete',
    postId,
    title: 'Confirm Deletion',
    message: 'Are you sure you want to delete this post?'
  };
}

function confirmReport(postId) {
  confirmModal.value = {
    visible: true,
    animateOut: false,
    type: 'report',
    postId,
    title: 'Confirm Report',
    message: 'Are you sure you want to report this post?'
  };
}

function animateAndCloseModal() {
  confirmModal.value.animateOut = true;
  setTimeout(() => {
    confirmModal.value.visible = false;
    confirmModal.value.animateOut = false;
  }, 300);
}

async function handleModalConfirm() {
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
        scrapPosts.value = scrapPosts.value.filter(p => p.id !== postId);
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

}

function formatDate(datetime) {
  if (!datetime) return 'N/A';
  const date = new Date(datetime);
  return isNaN(date) ? 'Invalid Date' : date.toLocaleDateString();
}

async function toggleSave(post) {
  try {
    const token = localStorage.getItem('user.access');
    await fetch(`http://localhost:8000/api/scrap-posts/${post.id}/save/`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` }
    });
    post.is_saved = !post.is_saved;
    showBanner(post.is_saved ? 'Post saved!' : 'Post unsaved.', 'success');
  } catch (err) {
    console.error('Error saving:', err);
  }
}

onMounted(async () => {
  const token = localStorage.getItem('user.access');
  try {
    const res = await axios.get('/api/recommendations/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    const crafty = res.data.crafty_posts || [];
    const scrap = res.data.scrap_posts || [];
    shuffle(crafty);
    shuffle(scrap);
    craftyPosts.value = crafty;
    scrapPosts.value = scrap;

    // Load the first 8 posts
    displayedCraftyPosts.value = crafty.slice(0, 8);
    displayedScrapPosts.value = scrap.slice(0, 8);
  } catch (err) {
    console.warn('Recommendation fetch error:', err);
  }

  try {
    const [craftyFallbackRes, scrapFallbackRes] = await Promise.all([
      axios.get('/api/posts/', { headers: { Authorization: `Bearer ${token}` } }),
      axios.get('/api/scrap-posts/scrapposts/', { headers: { Authorization: `Bearer ${token}` } })
    ]);
    fallbackCrafty.value = shuffle(craftyFallbackRes.data.slice(0, 10));
    fallbackScrap.value = shuffle(scrapFallbackRes.data.slice(0, 10));
  } catch (fallbackError) {
    console.error('Error loading fallback posts:', fallbackError);
  }
});

// Function to load more posts
const loadMorePosts = (type) => {
  if (type === 'crafty') {
    const nextPosts = craftyPosts.value.slice(displayedCraftyPosts.value.length, displayedCraftyPosts.value.length + 8);
    displayedCraftyPosts.value.push(...nextPosts);
  } else if (type === 'scrap') {
    const nextPosts = scrapPosts.value.slice(displayedScrapPosts.value.length, displayedScrapPosts.value.length + 8);
    displayedScrapPosts.value.push(...nextPosts);
  }
};

</script>



<style scoped>
.crafty-posts{
  /* border: 1px solid green; */
  display: flex;
  gap: 2vw;
  
}
.feed-item {
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);

  width: 21vw;
  transition: transform .2s;
}

.feed-item:hover {
  transform: scale(1.03);
}

.recommendHead {
  font-size: 5vw;
  gap: 5vw;
  font-family: "Concert One", serif;
  height: 80vh;

}

.scrap-info {
  width: 21vw;
  margin-left: 2vw;
}

.action-btn i {
  font-size: 1.3rem;
  margin: 0vh 1vw;

}

.action-btn {
  position: relative;
  top: 2vh;

}

p {
  text-align: left;
  font-size: 1vw;
}

.mainH1 {
  font-size: 4vw;
  font-family: "Concert One", serif;
  position: relative;
}

.mainH1 {
  /* top: 7vh; */
  left: 5vw;
}

.mainCont {
  flex-wrap: wrap;
  gap: 2vw;
  position: relative;
  top: 10vh;
}

.subHeading {
  font-size: 4vw;
  font-family: "Concert One", serif;
  text-align: center;
  margin-top: 3vh;
  margin-bottom: 2vh;
  color: rgb(155, 180, 155);
}

.posts {
  gap: 2vw;
  margin-bottom: 5vh;
  width: 21vw;
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);
  border-radius: 30px;
}

.scrapRec {
  /* border: 2px solid black; */
  width: 100vw;
}

.scrap-post {
  width: 21vw;
  height: 60vh;
  transition: transform .2s;
  flex-direction: column;
  border-radius: 30px;
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);

}

.scrap-post:hover {
  transform: scale(1.03);
}

.scrap-post img {
  width: 19vw;
  height: 35vh;
  gap: 1vw;
}

.user-info {
  justify-content: start;
  width: 21vw;
  margin-left: 2vw;
  height: 2vh;
  gap: 1vw;
  margin-bottom: 2vh;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
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
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.25);
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

.confirm-btn:hover {
  background: #c9302c;
}

.cancel-btn:hover {
  background: #5a6268;
}

/* Modal animation */
@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes fadeOutBackdrop {
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
  }
}

.scale-in {
  animation: scaleIn 0.3s ease-in-out;
}

@keyframes scaleIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }

  to {
    transform: scale(1);
    opacity: 1;
  }
}

.action-banner {
  position: fixed;
  top: 2vh;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  padding: 1vh 2vw;
  border-radius: 8px;
  font-weight: bold;
  text-align: center;
  min-width: 250px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease-in-out;
}

.action-banner.success {
  background-color: #d4edda;
  color: #155724;
  border: 2px solid #c3e6cb;
}

.action-banner.warning {
  background-color: #fff3cd;
  color: #856404;
  border: 2px solid #ffeeba;
}

.action-banner.danger {
  background-color: #f8d7da;
  color: #721c24;
  border: 2px solid #f5c6cb;
}

/* Banner Fade Animation */
/* Opposite slide-in and slide-out effect */
.banner-slide-enter-active {
  transition: opacity 0.4s ease-in, transform 0.4s ease-in;
}

.banner-slide-leave-active {
  transition: opacity 0.4s ease-out, transform 0.4s ease-out;
}

.banner-slide-enter-from {
  opacity: 0;
  transform: translateY(-20px);
  /* Slide in from top */
}

.banner-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.banner-slide-leave-from {
  opacity: 1;
  transform: translateX(0);
}

.banner-slide-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

.viewMore {
  width: 9vw;
  border-radius: 30px;
  background-color: #8db161;
  color: white;
  border: 3px solid black;
  font-family: "Concert One", serif;
  font-size: 1.4vw;
  transition: transform .2s;
  margin-left: 45.5vw;
}
</style>
