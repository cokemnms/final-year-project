<template>
  <div class="mb-6 comment flex">
    <div class="flex userComment">
      <div class="flex userMeta" style="gap: .5vw;">
        <img
          :src="comment.created_by.avatar || defaultAvatar"
          class="avatar"
          alt="User Avatar"
        />
        <p>
          <strong>
            <RouterLink :to="{ name: 'UserProfile', params: { id: comment.created_by.id } }">
              {{ comment.created_by.firstName }} {{ comment.created_by.lastName }}
            </RouterLink>
          </strong>
        </p>
      </div>

      <div class="flex dateDelete" style="gap: 1vw;">
        <p class="text-gray">{{ comment.created_at_formatted }}</p>
        <button
          v-if="userStore.user.id === comment.created_by.id"
          @click="handleDelete"
          class="text-red text-sm"
        >
          DELETE
        </button>
      </div>
    </div>

    <p v-html="formattedBody" class="commentText"></p>
  </div>
</template>

<script>
import { RouterLink } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

export default {
  props: {
    comment: Object,
  },
  components: { RouterLink },
  setup() {
    const userStore = useUserStore()
    return { userStore }
  },
  data() {
    return {
      defaultAvatar: '/default-avatar.png' // make sure this file exists in your public folder
    }
  },
  computed: {
    formattedBody() {
      return this.comment.body.replace(/\n/g, '<br>')
    }
  },
  methods: {
    handleDelete() {
      axios
        .delete(`/api/posts/comments/${this.comment.id}/delete/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('user.access')}`,
          },
        })
        .then(() => {
          this.$emit('delete-comment', this.comment.id)
        })
        .catch((error) => {
          console.log('Failed to delete comment:', error)
        })
    },
  },
}
</script>

<style scoped>
.comment {
  border-radius: 30px;
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);
  min-width: 38vw;
  max-width: 38vw;
  padding: 1vw;
  gap: 1vw;
  flex-direction: column;
  text-align: left;
  background-color: white;
}

.userComment {
  gap: 2vw;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.userMeta {
  align-items: center;
}

.dateDelete {
  align-items: center;
  font-size: 0.9rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 9999px;
  object-fit: cover;
  border: 1px solid #ccc;
}

.commentText {
  white-space: pre-wrap;
  word-break: break-word;
  margin-left: 3.2rem;
}
</style>
