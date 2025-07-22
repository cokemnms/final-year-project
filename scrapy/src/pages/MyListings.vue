<template>
  <Navbar />

  <div class="my-listings">
    <!-- Banner -->
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

    <div class="my-posts">

      <h1>MY POSTS</h1>
    </div>

    <!-- Crafty Posts -->
    <h1 class="my-craftyHead">CRAFTY POSTS</h1>


    <div class="my-craftyCont flex">

      <div class="pa-2 my-craftyPost" v-for="post in userPosts" :key="post.id">
        <FeedItem :post="post" @deletePost="deletePost" />
      </div>
    </div>


    <!-- Scrap Posts -->
    <h1 class="my-scrapHead">SCRAP POSTS</h1>
    <div class="scrap-container">
      <div v-for="post in scrapUserPosts" :key="post.id" class="item">
        <div class="user-info" v-if="post.user">
          <img v-if="post.user.avatar" :src="formatAvatar(post.user.avatar)" alt="avatar" class="avatar-img" />
          <div class="user-meta">
            <RouterLink v-if="post.user.id" :to="{ name: 'UserProfile', params: { id: post.user.id } }"
              class="user-link">
              {{ post.user.firstName }} {{ post.user.lastName }}
            </RouterLink>
          </div>
        </div>
        <RouterLink :to="{ name: 'ProductDetails', params: { id: post.id } }" class="item-link">
          <img :src="post.attachments?.[0]?.get_image || '/default.jpg'" alt="post image" />

          <p class="truncate-title">{{ post.title }}</p>
          <p>Rs {{ post.price }}</p>
          <p style="color:grey;font-size: 1vw;">{{ formatDate(post.created_at) }}</p>
          <p style="color:grey;font-size: 1vw;">{{ post.user?.city || 'City not set' }}</p>
        </RouterLink>

        <div class="post-actions">
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
  </div>

  <!-- Modal -->
  <div v-if="confirmModal.visible" class="modal-backdrop">
    <div class="modal scale-in">
      <h3>{{ confirmModal.type === 'delete' ? 'Confirm Deletion' : 'Confirm Report' }}</h3>
      <p>
        {{ confirmModal.type === 'delete'
          ? 'Are you sure you want to delete this post?'
          : 'Are you sure you want to report this post?' }}
      </p>
      <div class="modal-buttons">
        <button class="confirm-btn" @click="handleModalConfirm">Yes</button>
        <button class="cancel-btn" @click="confirmModal.visible = false">No</button>
      </div>
    </div>
  </div>

  <Footer />
</template>

<script>
import axios from 'axios'
import Navbar from '@/layouts/Navbar.vue'
import Footer from '@/layouts/Footer.vue'
import FeedItem from '@/components/CraftyComponents/FeedItem.vue'
import { onMounted, reactive, computed, ref, nextTick } from 'vue'
import { useUserStore } from '@/stores/user'

export default {
  components: { Navbar, Footer, FeedItem },
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

    const deletePost = (id) => {
      state.posts = state.posts.filter(post => post.id !== id)
    }

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

    const userPosts = computed(() =>
      state.posts.filter(p => p.created_by.id === userStore.user.id)
    )

    const scrapUserPosts = computed(() =>
      state.scrapPosts.filter(p => p.user?.id === userStore.user.id)
    )

    const toggleSave = async (post) => {
      const token = localStorage.getItem('user.access')
      try {
        await axios.post(`http://localhost:8000/api/scrap-posts/${post.id}/save/`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        })
        post.is_saved = !post.is_saved
        showBanner(post.is_saved ? 'Saved!' : 'Unsaved!', 'success')
      } catch {
        showBanner('Save failed', 'danger')
      }
    }

    const confirmDelete = (id) => {
      state.confirmModal = { visible: true, type: 'delete', postId: id }
    }

    const confirmReport = (id) => {
      state.confirmModal = { visible: true, type: 'report', postId: id }
    }

    const handleModalConfirm = async () => {
      const { type, postId } = state.confirmModal
      const token = localStorage.getItem('user.access')
      state.confirmModal.visible = false

      if (type === 'delete') {
        await axios.delete(`http://localhost:8000/api/scrap-posts/${postId}/delete/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        state.scrapPosts = state.scrapPosts.filter(p => p.id !== postId)
        showBanner('Deleted', 'danger')
      } else if (type === 'report') {
        await axios.post(`http://localhost:8000/api/scrap-posts/${postId}/report/`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        })
        showBanner('Reported', 'warning')
      }
    }

    const showBanner = (msg, color = 'success') => {
      state.actionMessage = msg
      state.actionColor = color
      nextTick(() => {
        setTimeout(() => {
          state.actionMessage = ''
        }, 3000)
      })
    }

    onMounted(() => {
      getCrafty()
      getScrap()
    })

    return {
      ...state,
      userStore,
      userPosts,
      scrapUserPosts,
      toggleSave,
      confirmDelete,
      confirmReport,
      handleModalConfirm,
      model,
      deletePost
    }
  },
  methods: {
    formatAvatar(avatarPath) {
      return avatarPath?.startsWith('http') ? avatarPath : avatarPath ? `http://localhost:8000${avatarPath}` : '/default-avatar.png';
    }, formatDate(datetime) {
      if (!datetime) return 'N/A';
      const date = new Date(datetime);
      return isNaN(date) ? 'Invalid Date' : date.toLocaleDateString();
    },
    formatAvatar(avatarPath) {
      return avatarPath?.startsWith('http') ? avatarPath : avatarPath ? `http://localhost:8000${avatarPath}` : '/default-avatar.png';
    },
    showBanner(message, color = 'success') {
      this.actionMessage = message;
      this.actionColor = color;
      setTimeout(() => {
        this.actionMessage = '';
        this.actionColor = '';
      }, 3000);
    },
    applyFilters() {
      let result = [...this.posts];

      if (this.locationQuery.trim()) {
        const query = this.locationQuery.trim().toLowerCase();
        result = result.filter(post => post.user?.city?.toLowerCase().includes(query));
      }

      if (this.selectedPriceRange) {
        const [min, max] = this.selectedPriceRange.split('-').map(Number);
        result = result.filter(post => post.price >= min && post.price <= max);
      }

      this.filteredPosts = result;
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
        try {
          const res = await fetch(`http://localhost:8000/api/scrap-posts/${postId}/delete/`, {
            method: 'DELETE',
            headers: { Authorization: `Bearer ${token}` }
          });
          if (res.ok) {
            this.posts = this.posts.filter(p => p.id !== postId);
            this.applyFilters();
            this.showBanner('Post deleted.', 'danger');
          } else {
            const err = await res.json();
            this.showBanner(err.error || 'Failed to delete post.', 'danger');
          }
        } catch {
          this.showBanner('An error occurred.', 'danger');
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
    async toggleSave(post) {
      try {
        const token = localStorage.getItem('user.access');
        await fetch(`http://localhost:8000/api/scrap-posts/${post.id}/save/`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` }
        });
        post.is_saved = !post.is_saved;
        this.showBanner(post.is_saved ? 'Post saved!' : 'Post unsaved.', 'success');
      } catch (err) {
        console.error('Error saving:', err);
      }
    }

  }
}
</script>

<style scoped>
.my-listings {
  padding: 1rem;
}

.scrap-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2vw;
}

.item {
  width: 20vw;
  padding: 1vw;
  border: 2px solid lightgray;
  border-radius: 15px;
  box-shadow: 1px 2px 6px rgba(0, 0, 0, 0.1);
}

.item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 10px;
}

.post-actions {
  display: flex;
  justify-content: space-around;
  margin-top: 10px;
}

.action-btn {
  background: none;
  border: none;
  font-size: 1.6vw;
  color: #555;
  cursor: pointer;
}

.action-btn:hover {
  color: #000;
}

.icon-lg {
  font-size: 1.5vw;
}

.action-banner {
  position: fixed;
  top: 5vh;
  left: 50%;
  transform: translateX(-50%);
  padding: 1vh 2vw;
  border-radius: 10px;
  font-size: 1vw;
  z-index: 999;
  font-family: 'Gill Sans', sans-serif;
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
  z-index: 1000;
}

.modal {
  background: white;
  padding: 2vw;
  border-radius: 10px;
  text-align: center;
  width: 30vw;
}

.modal-buttons {
  margin-top: 2vh;
  display: flex;
  justify-content: space-around;
}

.confirm-btn,
.cancel-btn {
  padding: 0.5vh 2vw;
  font-size: 1vw;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.confirm-btn {
  background: #d9534f;
  color: white;
}

.cancel-btn {
  background: #6c757d;
  color: white;
}


.my-craftyPost {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);

  border-radius: 30px;
  height: 71vh;
  width: 22vw;
  background-color: white;
}

.my-craftyCont {
  width: 100vw;
  flex-wrap: wrap;
  gap: 2vw;
}

.my-posts {
  margin: auto;
  width: 50vw;
  font-size: 5vw;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "Concert One", serif;
  margin-bottom: 10vh;
  margin-bottom: 10vh;


}

.my-craftyHead,
.my-scrapHead {
  font-family: "Concert One", serif;
  font-size: 4vw;
  position: relative;
  margin-bottom: 10vh;
  left: 3vw;


}

.my-scrapHead {
  margin: 2vw;
}


.avatar-img {
  width: 45px !important;
  height: 45px !important;
  border-radius: 50px !important;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5vw;
}

.user-link {
  font-size: 1.2vw;
  text-decoration: none;
  color: black;
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.post-actions {
  display: flex;
  justify-content: space-around;
  margin-top: 10px;
}

.action-btn {
  background: none;
  border: none;
  font-size: 1.5vw;
  color: #555;
  cursor: pointer;
}

.action-btn:hover {
  color: #000;
}

main {
  padding-bottom: 10vh;
  background: white;
  z-index: 1;
}

.filters {
  margin: 2vh 5vw;
  display: flex;
  gap: 2vw;
  align-items: center;
  font-family: 'Gill Sans', sans-serif;
  z-index: 2;
}

.filters label {
  font-size: 1.1vw;
  display: flex;
  flex-direction: column;
}

.filters input,
.filters select {
  margin-top: 0.5vh;
  padding: 0.5vh;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-size: 1vw;
  z-index: 3;
}
</style>
