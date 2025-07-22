<template>
  <Navbar />
  <div class="craftyHead flex">
    <img src="@/assets/DIY.gif" alt="" style="width: 40vw;">
    <h1 style="color: #8db161;">CRAFT <br >CONSERVER <br> CONNECT</h1>
  </div>

  <div class="mainCont flex">
    <form @submit.prevent="submitForm" method="post">
      <div class="form-body">
        <!-- TITLE FIELD -->
        <input v-model="title" type="text" placeholder="Enter a catchy title" class="title-input" />

        <!-- DESCRIPTION -->
        <textarea v-model="body" class="post-textarea" placeholder="Describe your product?"></textarea>

        <!-- Previews -->
        <div v-if="previews.length" class="preview-wrapper">
          <div v-for="(src, index) in previews" :key="index" class="preview-item">
            <button class="remove-btn" style="width: 2vw;" @click.prevent="removeFile(index)">X</button>
            <video v-if="selectedFiles[index].type.includes('video')" :src="src" controls />
            <img v-else :src="src" alt="preview" />
          </div>
        </div>
      </div>

      <div class="form-footer flex">
        <input type="file" id="file-upload" ref="file" @change="onFileChange" accept="image/*,video/*" multiple
          style="display: none" />

        <label for="file-upload" class="cursor-pointer">
          <img width="50" height="50" src="https://img.icons8.com/ios/50/image--v1.png" alt="upload" />
        </label>

        <div v-if="warning" class="warning-message">
          {{ warning }}
        </div>

        <button class="submit-button">POST</button>
      </div>
    </form>

    <h1 style="font-size: 5vw; font-family: 'Concert One', serif; margin: 5vh 0vh 3vh 0vh;">CRAFTY</h1>
    <div class="posts flex">
      <div class="post" v-for="post in posts" :key="post.id">
        <FeedItem :post="post" :showDescription="false" @deletePost="deletePost" />

      </div>
    </div>
  </div>
  <Footer />
</template>

<script>
import Navbar from "@/layouts/Navbar.vue";
import axios from 'axios';
import CommentItem from '@/components/CraftyComponents/CommentItem.vue';
import FeedItem from '@/components/CraftyComponents/FeedItem.vue';
import Footer from '@/layouts/Footer.vue';

export default {
  name: 'FeedView',
  components: {
    Navbar,
    CommentItem,
    FeedItem,
    Footer
  },

  data() {
    return {
      posts: [],
      title: '',        // ✅ NEW
      body: '',
      warning: '',
      selectedFiles: [],
      previews: []
    };
  },

  mounted() {
    this.getFeed();
  },

  methods: {
    deletePost(id) {
      this.posts = this.posts.filter(post => post.id !== id);
    },

    onFileChange(e) {
      const newFiles = Array.from(e.target.files);
      if (this.selectedFiles.length + newFiles.length > 5) {
        this.warning = 'You can upload up to 5 files only.';
        this.$refs.file.value = null;
        return;
      }
      this.warning = '';
      this.selectedFiles = this.selectedFiles.concat(newFiles);
      this.previews = this.selectedFiles.map(file => URL.createObjectURL(file));
      this.$refs.file.value = null;
    },

    removeFile(index) {
      this.selectedFiles.splice(index, 1);
      this.previews.splice(index, 1);
    },

    getFeed() {
      axios
        .get('/api/posts/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('user.access')}`
          }
        })
        .then(response => {
          this.posts = response.data;
        })
        .catch(error => {
          console.log('GET /api/posts/ error:', error);
        });
    },

    submitForm() {
      if (!this.title.trim()) {
        this.warning = 'Title is required.';
        return;
      }

      if (!this.body.trim()) {
        this.warning = 'Description is required.';
        return;
      }

      if (this.selectedFiles.length === 0) {
        this.warning = 'At least one image or video is required.';
        return;
      }

      this.warning = '';
      const formData = new FormData();
      formData.append('title', this.title); // ✅ NEW
      formData.append('body', this.body);

      this.selectedFiles.forEach(file => {
        formData.append('attachments', file);
      });

      axios.post('/api/posts/create/', formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('user.access')}`,
          'Content-Type': 'multipart/form-data'
        }
      })
        .then(response => {
          this.posts.unshift(response.data);
          this.title = '';
          this.body = '';
          this.selectedFiles = [];
          this.previews = [];
          this.$refs.file.value = null;
        })
        .catch(error => {
          console.log('POST /api/posts/create/ error:', error);
        });
    }
  }
};
</script>

<style scoped>
.form-footer {
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.mainCont {
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  top: 10vh;
}

textarea {
  width: 40vw;
  height: 20vh;
  border: 1px solid rgb(0, 0, 0);
  padding: 10px;
  border-radius: 8px;
  font-size: 16px;
  resize: none;
  background-color: white;
}

.title-input {
  width: 40vw;
  padding: 10px;
  margin-bottom: 20px;
  font-size: 16px;
  border: 1px solid black;
  border-radius: 8px;
  background-color: white;
}

form button,
.button {
  min-width: 120px;
  height: 40px;
  border-radius: 30px;
  background-color: #8db161;
  color: white;
  border: 3px solid black;
  font-family: "Concert One", serif;
  font-size: 1rem;
  transition: transform 0.2s;
  display: inline-block;
  margin-top: 10px;
}

.form-body {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.warning-message {
  color: red;
  margin-top: 10px;
  font-size: 14px;
  margin-left: 20px;
}

.posts {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 5vh;
  margin-top: 30px;
  width: 100%;
}

.post {
  background: white;
  width: 22vw;
  min-height: 300px;
  border-radius: 10px;
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);
  overflow: hidden;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform .2s;
}

.post:hover {
  transform: scale(1.03);
}

form {
  padding: 2vw;
  border-radius: 30px;
  position: relative;
  bottom: 3vw;
  background-color: rgb(255, 255, 255);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.submit-button {
  height: 7vh;
  font-size: 1.3vw;
}

.preview-wrapper {
  display: flex;
  gap: 10px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.preview-item {
  position: relative;
  width: 10vw;
  height: 25vh;
  border-radius: 8px;
  overflow: hidden;
}

.preview-item img,
.preview-item video {
  width: 100%;
  border-radius: 8px;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  background: red;
  color: white;
  border: none;
  border-radius: 50px;
  width: 8px;
  height: 18px;
  font-size: 12px;
  font-weight: bold;
  line-height: 18px;
  text-align: center;
  padding: 0;
  cursor: pointer;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
}

.craftyHead {
  width: 100vw;
  height: 70vh;
  gap: 7vw;
}

.craftyHead h1 {
  font-size: 6vw;
  font-family: "Concert One", serif;
}

@media (max-width: 768px) {

  .title-input,
  textarea,
  .post,
  form {
    width: 90%;
  }

  .post {
    width: 100%;
    max-width: 350px;
  }

  form button,
  .button {
    width: 100px;
    font-size: 14px;
  }
}
</style>
