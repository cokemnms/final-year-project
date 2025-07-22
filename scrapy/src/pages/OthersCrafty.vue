<template>
  <Navbar />

  <div class="my-listings">
    <h1>USER'S LISTINGS</h1>

    <div class="post-container">
      <div
        class="post-card"
        v-for="post in userPosts"
        :key="post.id"
      >
        <FeedItem :post="post" @deletePost="deletePost" />
      </div>
    </div>
  </div>
  <Footer/>
</template>

<script>
import Navbar from '@/layouts/Navbar.vue'
import FeedItem from '@/components/CraftyComponents/FeedItem.vue'
import CommentItem from '@/components/CraftyComponents/CommentItem.vue'
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { computed, onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'  // <-- import useRoute
import Footer from '@/layouts/Footer.vue'
export default {
  name: 'OthersCrafty',
  components: {
    Navbar,
    FeedItem,
    CommentItem,
    Footer
  },

  setup() {
    const userStore = useUserStore()
    const route = useRoute()

    // Get the profile user ID from the route param
    const profileUserId = route.params.id

    const state = reactive({
      posts: [],
      body: '',
      url: null,
      warning: ''
    })

    const getFeed = () => {
      axios
        .get('/api/posts/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('user.access')}`
          }
        })
        .then(response => {
          state.posts = response.data
        })
        .catch(error => {
          console.error('GET /api/posts/ error:', error)
        })
    }

    const deletePost = (id) => {
      state.posts = state.posts.filter(post => post.id !== id)
    }

    const likePost = (post) => {
      axios
        .post(`/api/posts/${post.id}/like/`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('user.access')}`
          }
        })
        .then(response => {
          if (response.data.message === 'like created') {
            post.likes_count += 1
            post.is_liked = true
          } else if (response.data.message === 'like removed') {
            post.likes_count -= 1
            post.is_liked = false
          }
        })
        .catch(error => {
          console.error('POST /like/ error:', error)
        })
    }

    // Filter posts by profileUserId, showing posts of the profile being viewed
    const userPosts = computed(() =>
      state.posts.filter(post => post.created_by.id === profileUserId)
    )

    const submitForm = () => {
      if (!state.url) {
        state.warning = 'Please attach an image before posting.'
        return
      }

      state.warning = ''

      let formData = new FormData()
      formData.append('image', state.url)
      formData.append('body', state.body)

      axios.post('/api/posts/create/', formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('user.access')}`,
          'Content-Type': 'multipart/form-data',
        }
      })
        .then(response => {
          state.posts.unshift(response.data)
          state.body = ''
          state.url = null
        })
        .catch(error => {
          console.error('POST /api/posts/create/ error:', error)
        })
    }

    const onFileChange = (e) => {
      const file = e.target.files[0]
      state.url = file
    }

    onMounted(() => {
      getFeed()
    })

    return {
      userStore,
      ...state,
      getFeed,
      deletePost,
      likePost,
      submitForm,
      onFileChange,
      userPosts
    }
  }
}
</script>

<style scoped>
.my-listings {
  padding: 1rem;
}

h1 {
  font-size: 4vw;
  margin-bottom: 1rem;
  font-family: "Concert One", serif;
  color: rgb(73, 73, 73);
  text-align: center;
}

.post-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  margin-top: 30px;
  width: 100%;
}

.post-card {
  background: #f5f5f5;
  width: 21vw;
  min-height: 70vh;
  border-radius: 12px;
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);
background-color:white;
  padding: 1rem;
  transition: transform 0.2s ease;
}

.post-card:hover {
    transform:scale(1.03)
}

</style>
