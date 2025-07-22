<template>
  <div class="post-wrapper">
    <!-- Feed Post -->
    <div class="feed-item flex" :style="{ width: customSize.width, height: customSize.height }">
      <div class="header">
        <div class="user-info" @click.stop>
          <img :src="getAvatarUrl(post.created_by.avatar)" class="avatar" alt="User avatar" />
          <p>
            <strong>
              <RouterLink :to="{ name: 'UserProfile', params: { id: post.created_by.id } }">
                {{ post.created_by.firstName }} {{ post.created_by.lastName }}
              </RouterLink>
            </strong>
          </p>
        </div>
        <p class="created-at" style="width: 6vw;">{{ formatDate(post.created_at_formatted) }}</p>
      </div>

      <template v-if="post.attachments?.length && !hideAttachments">
        <img :src="post.attachments[0].get_image" class="post-image" alt="Post attachment" @click.stop />
      </template>

      <div class="post-title" :style="{ fontSize: customFontSize, lineHeight: customLineHeight }">
        {{ post.title }}
      </div>

      <div v-if="showDescription" class="post-description" v-html="formattedBody"></div>

      <div class="like-comment flex" style="gap: 2vw; margin-bottom: 1vw;">
        <div class="actions">
          <div class="left-actions">
            <div class="like" @click.stop="likePost(post)">
              <svg xmlns="http://www.w3.org/2000/svg" :fill="post.is_liked ? 'red' : 'white'" :stroke="post.is_liked ? 'red' : 'black'"
                   viewBox="0 0 24 24" stroke-width="2.5" class="icon">
                <path stroke-linecap="round" stroke-linejoin="round"
                      d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5C14.377 3.75 12.715 4.876 12 6.483 11.285 4.876 9.623 3.75 7.688 3.75 5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
              </svg>
              <span class="likes-count">{{ post.likes_count }}</span>
            </div>
          </div>
        </div>

        <div class="comments">
          <RouterLink :to="{ name: 'PostView', params: { id: post.id } }" class="comments flex" style="align-items: center; gap: 0.5vw;">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor"
                 class="icon">
              <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 20.25c4.97 0 9-3.694 9-8.25S16.97 3.75 12 3.75 3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z" />
            </svg>
          </RouterLink>
          <span class="comments-count">{{ post.comments_count }}</span>
        </div>
      </div>

      <div class="post-actions flex" style="gap: 2vw;">
        <button @click="post_save(post)" class="action-btn" :title="post.is_saved ? 'Unsave' : 'Save'">
          <i :class="post.is_saved ? 'fas fa-bookmark' : 'far fa-bookmark'" style="font-size: 1.5rem;"></i>
        </button>
        <button v-if="userStore.user.id === post.created_by.id" @click="handleDelete(post.id)" class="action-btn" title="Delete Post">
          <i class="fas fa-trash-alt" style="font-size: 1.5rem;"></i>
        </button>
        <button @click="handleReport(post.id)" class="action-btn" title="Report Post">
          <i class="fas fa-flag" style="font-size: 1.5rem;"></i>
        </button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
import { RouterLink, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'
import DOMPurify from 'dompurify';

const BASE_URL = 'http://127.0.0.1:8000'

export default {
  props: {
    post: Object,
    showDescription: {
  type: Boolean,
  default: false
},
    hideAttachments: Boolean,
    fullText: {
      type: Boolean,
      default: false
    },
     customSize: {
    type: Object,
    default: () => ({ width: '100%', height: '70vh'
     })
  },
   customFontSize: {
    type: String,
    default: '2rem'
  },
   customLineHeight: {
    type: String,
    default: '1.5'
  }
  },
  computed: {
  formattedBody() {
    const safeText = this.post.body.replace(/\n/g, '<br>');
    return DOMPurify.sanitize(safeText);
  }
},
  emits: ['deletePost'],
  data() {
    return {
      actionMessage: '',
      actionColor: '',
      fadingOut: false,
      confirmModal: {
        visible: false,
        animateOut: false,
        type: '',
        postId: null,
        title: '',
        message: ''
        

      }
    }
  },
  setup() {
    const userStore = useUserStore()
    const toastStore = useToastStore()
    const router = useRouter()
    return { userStore, toastStore, router }
  },
  

  methods: {
  formatDate(datetime) {
    if (!datetime) return 'N/A';
    const parsed = Date.parse(datetime);
    if (isNaN(parsed)) return 'Invalid Date';
    return new Date(parsed).toLocaleDateString('en-GB', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    });
  },
  async handleDelete(postId) {
    if (!window.confirm('Are you sure you want to delete this post?')) return;
    const token = localStorage.getItem('user.access');
    if (!token) return;
    try {
      const res = await fetch(`${BASE_URL}/api/posts/${postId}/delete/`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        this.$emit('deletePost', postId);
        alert('Post deleted.');
      }
    } catch (err) {
      console.error('Delete error:', err);
      alert('Error deleting post.');
    }
  },
 async handleReport(postId) {
  if (!window.confirm('Are you sure you want to report this post?')) return;

  const token = localStorage.getItem('user.access');
  if (!token) return;

  try {
    const res = await fetch(`${BASE_URL}/api/posts/${postId}/report/`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (res.ok) {
      alert('Post reported.');
    } else {
      const error = await res.json();
      alert(error.error || 'Failed to report post.');
    }
  } catch (err) {
    console.error('Report error:', err);
    alert('Error reporting post.');
  }
}
,
  async post_save(post) {
    try {
      const token = localStorage.getItem('user.access');
      await fetch(`${BASE_URL}/api/posts/${post.id}/save/`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      });
      post.is_saved = !post.is_saved;
      alert(post.is_saved ? 'Post saved!' : 'Post unsaved.');
    } catch (err) {
      console.error('Save error:', err);
    }
  },
  getAvatarUrl(avatarPath) {
    const base = !avatarPath
      ? '/default-avatar.png'
      : avatarPath.startsWith('http')
        ? avatarPath
        : `${BASE_URL}${avatarPath}`;
    return `${base}?t=${Date.now()}`;
  },
  likePost(post) {
    axios.post(`${BASE_URL}/api/posts/${post.id}/like/`, {}, {
      headers: { Authorization: `Bearer ${localStorage.getItem('user.access')}` }
    }).then(response => {
      if (response.data.message === 'like created') {
        post.likes_count += 1;
        post.is_liked = true;
      } else if (response.data.message === 'like removed') {
        post.likes_count -= 1;
        post.is_liked = false;
      }
    }).catch(error => {
      console.error('Like error:', error);
    });
  }
}

}
</script>
<style scoped>




.feed-item {
  height: 70vh;
  padding: 1rem;
  border-radius: 8px;
  flex-direction: column;
}

.header {
  display: flex;
  gap: 7vw;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 10vw;
  position: relative;
  left: 2vw;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
}

.created-at {
  color: #666;
  font-size: 0.9rem;
}

.post-image {
  width: 20vw;
  height: 40vh;
  margin: 0.75rem 0;
  border-radius: 8px;
  object-fit: cover;
}

.post-video {
  width: 20vw;
  height: 40vh;
  margin: 0.75rem 0;
  border-radius: 8px;
  object-fit: cover;
}

.post-body {
  margin: 1rem 0;
  font-size: 1.5vw;
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: block;
}


.post-body.full-text {
  white-space: normal !important;
  overflow: visible !important;
  text-overflow: unset !important;
}

.actions {
  display: flex;
  gap: 10vw;
  align-items: center;
}

.left-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.icon {
  width: 30px;
  height: 30px;
  cursor: pointer;
}

.likes-count,
.comments-count {
  margin-left: 0.5rem;
}

.extra-menu {
  cursor: pointer;
}

.extra-modal {
  margin-top: 0.5rem;
  border: 1px solid #ccc;
  background: white;
  border-radius: 6px;
  padding: 0.5rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.modal-actions>div {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  cursor: pointer;
  user-select: none;
}

.blue-text {
  color: #3b82f6;
}

.red-text {
  color: #ef4444;
}

.orange-text {
  color: #f97316;
}

.blue {
  stroke: #3b82f6;
}

.red {
  stroke: #ef4444;
}

.orange {
  stroke: #f97316;
}

.post-actions button i {
  width: 6vw;
}

.fade-post {
  opacity: 0.4;
  transition: opacity 0.4s ease-in-out;
}

.post-title {
  font-size: 1.8vw;
  font-weight: bold;
  color: #2b2b2b;
  margin-bottom: 1vh;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
}

.post-description {
  white-space: pre-wrap;
  overflow: visible;
  text-overflow: unset;
  color: #444;
}
.post-wrapper {
  position: relative;
  width: 100%;
}

</style>
