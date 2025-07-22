<template>
  <Navbar/>
  <div>
    <!-- Action Banner -->
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

    <main style="margin-top: 5vh;">
      <h1>USER'S SCRAP POSTS</h1>

      <!-- Filter Controls -->
      <div class="filters">
      

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

      <!-- Posts List -->
      <div class="scrap-container">
        <div v-if="filteredPosts.length === 0" class="no-results">Sorry, nothing matches your filters.</div>
        <div v-for="post in filteredPosts" :key="post.id" class="item">
          <!-- User Info -->
          <div class="user-info" v-if="post.user">
            <img v-if="post.user.avatar" :src="formatAvatar(post.user.avatar)" alt="avatar" class="avatar-img" />
            <div class="user-meta">
              <RouterLink v-if="post.user.id" :to="{ name: 'UserProfile', params: { id: post.user.id } }" class="user-link">
                {{ post.user.firstName }} {{ post.user.lastName }}
              </RouterLink>
            </div>
          </div>
          <p v-else>Posted by: Unknown</p>

          <!-- Post Content -->
           <RouterLink :to="{ name: 'ProductDetails', params: { id: post.id } }" class="item-link">

             <img :src="post.attachments?.[0]?.get_image || '/default.jpg'" alt="post image" />
             <h3>{{ post.title }}</h3>
             <p>Rs {{ post.price }}</p>
             <p>{{ post.user.city }}</p>
            </RouterLink>


          <!-- Action Buttons -->
          <div class="post-actions">
            <button @click="toggleSave(post)" class="action-btn" :title="post.is_saved ? 'Unsave' : 'Save'">
              <i :class="post.is_saved ? 'fas fa-bookmark' : 'far fa-bookmark'"></i>
            </button>
            <button v-if="userStore.user.id === post.user?.id" @click="confirmDelete(post.id)" class="action-btn" title="Delete Post">
              <i class="fas fa-trash-alt"></i>
            </button>
            <button @click="confirmReport(post.id)" class="action-btn" title="Report Post">
              <i class="fas fa-flag"></i>
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
  <Footer/>
</template>

<script>
import Navbar from '@/layouts/Navbar.vue';
import { useUserStore } from '@/stores/user';
import { RouterLink } from 'vue-router';
import Footer from '@/layouts/Footer.vue'
export default {
  name: 'OtherScrap',
  components: { RouterLink,Navbar,Footer },
  data() {
    return {
      posts: [],
      filteredPosts: [],
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
  async created() {
  const profileUserId = this.$route.params.id;
  try {
    const token = localStorage.getItem('user.access');
    if (!token) return;

    const res = await fetch(`http://localhost:8000/api/scrap-posts/user/${profileUserId}/posts/`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    const data = await res.json();

    if (Array.isArray(data)) {
      // Sort by created_at descending (newest first)
      const sorted = data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

      this.posts = sorted.map(post => ({
        ...post,
        is_saved: post.is_saved || false,
        image: post.image?.startsWith('http') ? post.image : 'http://localhost:8000' + post.image,
        user: post.user
          ? {
              ...post.user,
              avatar: post.user.avatar?.startsWith('http')
                ? post.user.avatar
                : post.user.avatar
                ? 'http://localhost:8000' + post.user.avatar
                : null
            }
          : null
      }));

      this.$nextTick(() => this.applyFilters());
    }
  } catch (err) {
    console.error('Error loading posts:', err);
  }
}
,
  methods: {
    formatDate(datetime) {
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
      }else if (type === 'report') {
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
};
</script>

<style scoped>
/* Action Banner */
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
p { font-size: 1.3vw; font-family: 'Gill Sans', sans-serif; }
h1 {
  margin: 4vh 5vw 2vh;
  font-size: 5vw;
  color: black;
  font-family: 'Concert One', serif;

}

.scrap-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: self-start;
  column-gap: 1vw;
  row-gap: 0vw;
  margin: auto;
  padding: 0 2vw;
  position: relative;
  width: 96vw !important;
  min-height: 100vh;
}
.item {
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
.item:hover { transform: scale(1.03); }
.item img {
  width: 20vw;
  height: 30vh;
  object-fit: cover;
  border-radius: 15px;
}
.item-link {
  color: inherit;
  text-decoration: none;
  display: block;
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
.action-btn:hover { color: #000; }
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
.no-results {
  font-size: 1.5vw;
  text-align: center;
  color: grey;
  margin: 5vh auto;
  width: 100%;
  font-family: 'Gill Sans', sans-serif;
}
</style>
