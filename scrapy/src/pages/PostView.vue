<template>
  <Navbar />

  <div class="main-center flex">
    <div class="imageSection flex">
      <div class="p-4 bg-white border border-gray rounded-lg text-black" v-if="post.id">
        <div v-if="post.attachments && post.attachments.length">
          <v-carousel hide-delimiters height="500">
            <v-carousel-item v-for="(attachment, index) in post.attachments" :key="attachment.id"
              :src="attachment.get_image" cover />
          </v-carousel>
        </div>

        
        <div class="user-information">
          <FeedItem :post="post" :fullText="true" :hideAttachments="true"
            :customSize="{ width: '100%', height: 'auto' }"
            customFontSize="1vw"  :showDescription="true" />
        </div>

        <div class="bg-white border border-gray rounded-lg mt-4">
          <form @submit.prevent="submitForm" method="post">
            <div class="p-4">
              <textarea v-model="body" class="p-4 w-full bg-gray rounded-lg" placeholder="What do you think?"
                rows="4"></textarea>
            </div>
            <div class="p-4 border-t border-gray">
              <button class="inline-block py-4 px-6 bg-purple text-white rounded-lg">Comment</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="post.comments && post.comments.length" class="commentSection">
      <div class="comments-list-wrapper">
        <h1 class="commentHead">COMMENTS</h1>
        <div class="comment-items">
          <CommentItem v-for="comment in post.comments" :key="comment.id" :comment="comment"
            @delete-comment="handleDeleteComment" />
        </div>
      </div>
    </div>
  </div>

  <Footer />
</template>

<script>
import axios from "axios";
import FeedItem from "@/components/CraftyComponents/FeedItem.vue";
import CommentItem from "@/components/CraftyComponents/CommentItem.vue";
import Navbar from "@/layouts/Navbar.vue";
import Footer from '@/layouts/Footer.vue';

export default {
  name: "PostView",
  components: {
    FeedItem,
    CommentItem,
    Navbar,
    Footer,
  },
  data() {
    return {
      post: {
        id: null,
        comments: [],
      },
      body: "",
    };
  },
  mounted() {
    this.getPost();
  },
  methods: {
    handleDeleteComment(deletedCommentId) {
      this.post.comments = this.post.comments.filter((c) => c.id !== deletedCommentId);
      if (this.post.comments_count > 0) {
        this.post.comments_count -= 1;
      }
    },
    getPost() {
      axios
        .get(`/api/posts/${this.$route.params.id}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("user.access")}`,
          },
        })
        .then((res) => {
          this.post = res.data.post;
        })
        .catch(console.error);
    },
    submitForm() {
      if (!this.body.trim()) return;

      axios
        .post(
          `/api/posts/${this.$route.params.id}/comment/`,
          { body: this.body },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("user.access")}`,
            },
          }
        )
        .then((res) => {
          this.post.comments.push(res.data);
          this.post.comments_count += 1;
          this.body = "";
        })
        .catch(console.error);
    },
  },
};
</script>

<style scoped>
::v-deep(.feed-item .post-body) {
  white-space: pre-wrap !important;
  overflow: visible !important;
  text-overflow: unset !important;
  font-size: 2vw;
  margin: 1rem 0;
}

.post-image {
  width: 20vw;
  height: 40vh;
  margin: 0.75rem 0;
  border-radius: 8px;
  object-fit: cover;
}

textarea {
  white-space: pre-wrap;
  word-wrap: break-word;
  overflow-wrap: break-word;
  resize: vertical;
  min-height: 4rem;
  max-width: 100%;
  box-sizing: border-box;
}

.user-information {
  margin-top: 1vh;
  margin-bottom: 2vh;
}

.imageSelection {
  width: 50vw;
  flex-direction: column;
  gap: 2vw;
}

.main-center {
  gap: 3vw;
  margin-top: 5vh;
  flex-wrap: wrap;
}

.v-carousel-item {
  width: 50vw;
  height: 60vh;
  border-radius: 30px;
}

.commentSection {
  width: 40vw;
}

.comments-list-wrapper {
  width: 40vw;
  max-height: 90vh;
  background: white;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.commentHead {
  font-family: "Concert One", serif;
  font-size: 4vw;
  padding: 1rem;
  margin: auto;
}

.comment-items {
  overflow-y: auto;
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  white-space: pre-wrap;
  overflow-x: hidden;
}

.comment-items::-webkit-scrollbar {
  width: 8px;
}

.comment-items::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.comment-items::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.comment-items::-webkit-scrollbar-thumb:hover {
  background: #555;
}

::v-deep(.v-carousel-item > img) {
  object-fit: cover !important;
  width: 100% !important;
  height: 100% !important;
  display: block;
}
</style>
