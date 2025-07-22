<template>

   <div v-if="actionMessage" :class="['action-banner', actionColor]">
      {{ actionMessage }}
    </div>

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
  <div class="saved-items">
    <h2>SAVED POSTS</h2>

    <section class="saved-scrap-posts">
      <h3>SAVED SCRAP POSTS</h3>
      <div v-if="savedScrapPosts.length" class="my-savedScrap">
        <div v-for="post in savedScrapPosts" :key="post.id" class="saved-post ">
          <div class="user-info flex" v-if="post.user" style="gap: 1vw;">
          <img v-if="post.user.avatar" style="width: 48px;height: 48px; border-radius: 50%;" :src="formatAvatar(post.user.avatar)" alt="avatar" class="avatar-img" />
          <div class="user-meta flex"  >
            <RouterLink v-if="post.user.id" :to="{ name: 'UserProfile', params: { id: post.user.id } }"
              class="user-link" style="font-size: 1vw;">
              {{ post.user.firstName }} {{ post.user.lastName }}
            </RouterLink>
          </div>
        </div>
        <RouterLink :to="{ name: 'ProductDetails', params: { id: post.id } }" class="item-link">
       
           <img :src="post.attachments?.[0]?.get_image || '/default.jpg'" alt="post image" style="height: 30vh;"/>

            <p class="truncate-title">{{ post.title }}</p>
            <p>Rs {{ post.price }}</p>
            <p style="color:grey;">{{ formatDate(post.created_at) }}</p>
            <p style="color:grey;">{{ post.user?.city || 'City not set' }}</p>
          </RouterLink>

        <div class="post-actions flex" style="gap: 2vw;">
          <button @click="toggleSave(post)" class="action-btn" :title="post.is_saved ? 'Unsave' : 'Save'">
            <i :class="post.is_saved ? 'fas fa-bookmark' : 'far fa-bookmark'"></i>
          </button>
          <button v-if="userStore.user.id === post.user?.id" @click="confirmDelete(post.id)" class="action-btn"
            title="Delete Post">
            <i class="fas fa-trash-alt"></i>
          </button>
          <button @click="confirmReport(post.id)" class="action-btn" title="Report Post">
            <i class="fas fa-flag"></i>
          </button>
        </div>
        </div>
      </div>
      <p v-else>No saved scrap posts.</p>
    </section>

   <section class="saved-repurposed-posts">
  <h3>SAVED CRAFTY POSTS</h3>
  <div v-if="savedCraftyPosts.length" class="my-craftyPosts">
    <div class="pa-2 my-craftyPost" v-for="post in savedCraftyPosts" :key="post.id">
      <FeedItem :post="post" @deletePost="deletePost" :customSize="{ width: '21vw', height: 'auto' }"
               />
    </div>
  </div>
  <p v-else>No saved crafty posts.</p>
</section>

  </div>
</template>

<script>
import { onMounted, reactive, computed, ref, nextTick } from 'vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios'
import FeedItem from '../CraftyComponents/FeedItem.vue';

export default {
  name: "SavedItems",
  components:{
    FeedItem
  },
  data() {
    return {
      savedScrapPosts: [],
      savedCraftyPosts: []
    };
  },
  setup() {
    const userStore = useUserStore()
    const state = reactive({
      posts: [],
      scrapPosts: [],
      confirmModal: { visible: false, type: '', postId: null },
      actionMessage: '',
      actionColor: ''
    })

    const model = ref(null)

    const getCrafty = async () => {
      const token = localStorage.getItem('user.access')
      const res = await axios.get('http://localhost:8000/api/posts/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      state.posts = res.data
    }

    const getScrap = async () => {
      const token = localStorage.getItem('user.access')
      const res = await axios.get('http://localhost:8000/api/scrap-posts/scrapposts/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      state.scrapPosts = res.data.map(post => ({
        ...post,
        is_saved: post.is_saved || false,
        image: post.image?.startsWith('http') ? post.image : 'http://localhost:8000' + post.image,
        user: post.user
      }))
    }

    onMounted(() => {
      getCrafty()
      getScrap()
    })

    return {
      ...state,
      userStore,
      model
    }
  },
  methods: {
    formatAvatar(avatarPath) {
      return avatarPath?.startsWith('http')
        ? avatarPath
        : avatarPath
        ? `http://localhost:8000${avatarPath}`
        : '/default-avatar.png';
    },
    formatDate(datetime) {
      if (!datetime) return 'N/A';
      const date = new Date(datetime);
      return isNaN(date) ? 'Invalid Date' : date.toLocaleDateString();
    },
    async fetchSavedScrapPosts() {
      const token = localStorage.getItem("user.access");
      try {
        const res = await fetch("http://localhost:8000/api/scrap-posts/saved-posts/", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const data = await res.json();
        this.savedScrapPosts = data;
      } catch (err) {
        console.error("Error fetching saved scrap posts:", err);
      }
    },
    async fetchSavedCraftyPosts() {
      const token = localStorage.getItem("user.access");
      try {
        const res = await fetch("http://localhost:8000/api/posts/saved/", {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const data = await res.json();
        this.savedCraftyPosts = data;
      } catch (err) {
        console.error("Error fetching saved crafty posts:", err);
      }
    },
    toggleSave(post) {
      const token = localStorage.getItem('user.access');
      fetch(`http://localhost:8000/api/scrap-posts/${post.id}/save/`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(() => {
        post.is_saved = !post.is_saved;
        this.showBanner(post.is_saved ? 'Post saved!' : 'Post unsaved.', 'success');
      })
      .catch(err => {
        console.error('Save error:', err);
        this.showBanner('Failed to save post.', 'danger');
      });
    },
    confirmDelete(postId) {
      this.confirmModal = {
        visible: true,
        animateOut: false,
        type: 'delete',
        postId,
        title: 'Confirm Deletion',
        message: 'Are you sure you want to delete this post?'
      };
    },
    confirmReport(postId) {
      this.confirmModal = {
        visible: true,
        animateOut: false,
        type: 'report',
        postId,
        title: 'Confirm Report',
        message: 'Are you sure you want to report this post?'
      };
    },
    deletePost(id) {
  this.savedCraftyPosts = this.savedCraftyPosts.filter(post => post.id !== id);
}
,
    animateAndCloseModal() {
      this.confirmModal.animateOut = true;
      setTimeout(() => {
        this.confirmModal.visible = false;
        this.confirmModal.animateOut = false;
      }, 300);
    },
    async handleModalConfirm() {
      const { type, postId } = this.confirmModal;
      this.animateAndCloseModal();

      const token = localStorage.getItem('user.access');
      if (!token) return;

      if (type === 'delete') {
        const res = await fetch(`http://localhost:8000/api/scrap-posts/${postId}/delete/`, {
          method: 'DELETE',
          headers: { Authorization: `Bearer ${token}` }
        });
        if (res.ok) {
          this.savedScrapPosts = this.savedScrapPosts.filter(p => p.id !== postId);
          this.showBanner('Post deleted.', 'danger');
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

    },
    showBanner(message, color = 'success') {
      this.actionMessage = message;
      this.actionColor = color;
      setTimeout(() => {
        this.actionMessage = '';
        this.actionColor = '';
      }, 3000);
    }
  },
  mounted() {
    this.fetchSavedScrapPosts();
    this.fetchSavedCraftyPosts();
  }
};
</script>


<style scoped>
.saved-scrap-posts{
  margin-bottom: 20vh;
}
.my-savedScrap{
  /* border: 2px solid red; */
  width: 100vw;
  display: flex;
  justify-content: center;

  flex-wrap: wrap;
  gap: 2vw;
  
}
.saved-items {
  max-width: 100vw;
  margin: 2rem auto;
  padding: 0 1rem;
  font-family: Arial, sans-serif;
}
h2 {
  font-size: 5vw;
  margin-bottom: 1.5rem;
  text-align: center;
  font-family: "Concert One", serif;
  margin-bottom: 10vh;
  
}
section {
  margin-bottom: 2rem;
}
h3 {
  font-size:3vw;
  margin-bottom: 1rem;
  padding-bottom: 0.25rem;
  font-family: "Concert One", serif;
  margin-bottom: 5vh;
  margin-left: 3vw;

}
.saved-post {
  margin-bottom: 1rem;
  padding: 1rem;
    box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);

  width: 21vw;
  font-size: 1.3vw;
  border-radius: 30px;
  transition: transform .2s;
}

.saved-post:hover{
  transform: scale(1.03);
}
.saved-post img {
  width: 20vw;
  height: 30vh;
  height: auto;
  object-fit: cover;
  margin-bottom: 0.5rem;
  border-radius: 20px;
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

.success {
  background-color: #4CAF50;
  color: white;
}

.danger {
  background-color: #f44336;
  color: white;
}

.warning {
  background-color: #ffc107;
  color: black;
}

@keyframes slideFade {
  from {
    opacity: 0;
    transform: translate(-50%, -10px);
  }

  to {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

@keyframes fadeOut {

  0%,
  85% {
    opacity: 1;
  }

  100% {
    opacity: 0;
  }
}

/* Confirmation Modal */
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

/* Existing Styles */
.truncate-title {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.my-craftyPost{
  width: 22vw;
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);
border-radius: 30px;
  display: flex;
}
.my-craftyPosts{
  width: 100vw;
  display: flex;
  gap: 2vw;
  flex-wrap: wrap;
  justify-content: center;
}
</style>
