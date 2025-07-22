<template>
  <Navbar />
  <h2>{{ categoryName }}</h2>
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

  <div class="filters">
    <label>
      Filter by City:
      <input type="text" v-model="locationQuery" @input="applyFilters" placeholder="Enter city name..." />
    </label>

    <label>
      Filter by Price Range:
      <select v-model="selectedPriceRange" @change="applyFilters">
        <option value="">-- Select --</option>
        <option value="0-100">0 - 100</option>
        <option value="100-500">100 - 500</option>
        <option value="500-1000">500 - 1000</option>
        <option value="1000-2000">1000 - 2000</option>
        <option value="2000-5000">2000 - 5000</option>
      </select>
    </label>
  </div>

  <div class="category-page">
    <div v-if="filteredPosts.length > 0" class="posts flex">
      <div v-for="post in filteredPosts" :key="post.id" class="post">
        <div class="user-info">
          <img v-if="post.user.avatar" :src="formatAvatar(post.user.avatar)" alt="avatar" class="avatar-img" />
          <div class="user-meta">
            <RouterLink v-if="post.user.id" :to="{ name: 'UserProfile', params: { id: post.user.id } }" class="user-link">
              {{ post.user.firstName }} {{ post.user.lastName }}
            </RouterLink>
          </div>
        </div>
        <RouterLink :to="{ name: 'ProductDetails', params: { id: post.id } }" class="item-link">

             <img :src="post.attachments?.[0]?.get_image || '/default.jpg'" alt="post image" />
             <h3 style="font-size: 1.3vw;">{{ post.title }}</h3>
             <p style="font-size: 1.3vw;">Rs {{ post.price }}</p>
             <p style="font-size: 1.3vw;">{{ post.user.city }}</p>
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
    </div>

    <div class="noCategory" v-else>
      <h1>NO POST FOUND IN THIS CATEGORY</h1>
      <img src="@/assets/noCategory.gif" alt="No posts found" />
    </div>
  </div>
  <Footer/>
</template>

<script>
import axios from 'axios';
import Navbar from '@/layouts/Navbar.vue';
import { useUserStore } from '@/stores/user';
import Footer from '@/layouts/Footer.vue'
export default {
  name: 'CategoryPage',
  components: { Navbar,Footer },
  data() {
    return {
      posts: [],
      filteredPosts: [],
      categoryName: '',
      actionMessage: '',
      actionColor: '',
      locationQuery: '',
      selectedPriceRange: '',
      confirmModal: {
        visible: false,
        animateOut: false,
        type: '',
        postId: null,
        title: '',
        message: ''
      }
    };
  },
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  watch: {
    '$route.params.categoryName': {
      immediate: true,
      handler(newCategory) {
        this.categoryName = newCategory;
        this.fetchPosts();
      }
    }
  },
  methods: {
    fetchPosts() {
      if (!this.categoryName) return;

      axios
        .get(`http://localhost:8000/api/scrap-posts/category/${this.categoryName}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('user.access')}`
          }
        })
        .then(response => {
          this.posts = response.data;
          this.filteredPosts = response.data;
        })
        .catch(error => {
          console.error('Error fetching category posts:', error);
        });
    },
    getFullImageUrl(imagePath) {
      if (!imagePath) return '';
      return imagePath.startsWith('http') ? imagePath : `http://localhost:8000${imagePath}`;
    },
    formatDate(datetime) {
      if (!datetime) return 'N/A';
      const date = new Date(datetime);
      return date.toLocaleDateString(); // Return only the date part
    },
    formatAvatar(avatarPath) {
      return avatarPath?.startsWith('http') ? avatarPath : avatarPath ? `http://localhost:8000${avatarPath}` : '/default-avatar.png';
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
    showBanner(message, color = 'success') {
      this.actionMessage = message;
      this.actionColor = color;
      setTimeout(() => {
        this.actionMessage = '';
        this.actionColor = '';
      }, 3000);
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
        const response = await fetch(`http://localhost:8000/api/scrap-posts/${post.id}/save/`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}` }
        });

        if (response.ok) {
          post.is_saved = !post.is_saved; // Update the save status immediately
          this.showBanner(post.is_saved ? 'Post saved!' : 'Post unsaved.', 'success');
        } else {
          const err = await response.json();
          this.showBanner(err.error || 'Failed to save post.', 'danger');
        }
      } catch (err) {
        console.error('Error saving:', err);
        this.showBanner('An error occurred.', 'danger');
      }
    }
  }
};
</script>


<style scoped>

p{
  font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

.posts {
  flex-wrap: wrap;
  flex-wrap: wrap;
  gap: 2rem;
}

.post {
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

.post img {
  width: 100%;
  height: 30vh;
  object-fit: cover;
  border-radius: 10px;
}

.noCategory{
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-content: center;
  /* gap: 5vw; */
  font-size: 5vw;
  font-family: "Concert One", serif;
  /* border: 2px solid black; */
  padding: 2vw;

}

.noCategory img{
  width: 50vw;
  height: 80vh;
}

h2{
  font-family: "Concert One", serif;
  font-size: 4vw;
  position: relative;
  left: 2vw;
  color: lightgreen;
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
