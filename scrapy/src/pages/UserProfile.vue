<template>
  <!-- <Navbar /> -->
  <UPInfo :user="user"/>
  <OtherPages />
  <Footer/>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user.js';
import UPInfo from '@/components/UPComponents/UPInfo.vue';
import OtherPages from '@/components/UPComponents/OtherPages.vue';
import Footer from '@/layouts/Footer.vue';
import Navbar from '@/layouts/Navbar.vue';

export default {
  name: "UserProfile",
  components: {
    Navbar,
    UPInfo,
    OtherPages,
    Footer

  },
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  data() {
    return {
      user: null,
      posts: [],
      savedPosts: []
    };
  },
  watch: {
    '$route.params.id': {
      handler(newId) {
        this.getProfileFeed(newId);
      },
      immediate: true
    }
  },
  methods: {
    getProfileFeed(id) {
      const token = localStorage.getItem('user.access');
      axios.get(`/api/posts/profile/${id}/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        }
      })
      .then(response => {
        this.posts = response.data.posts;
        this.user = response.data.user;
      })
      .catch(error => {
        console.error('Profile fetch failed:', error);
      });
    },
    refreshUserData() {
      const id = this.$route.params.id;
      this.getProfileFeed(id);
    }
  }
};
</script>
