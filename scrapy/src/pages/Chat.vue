<template>
  <Navbar />

  <!-- Success Banner -->
  <div v-if="successMessage" class="success-banner" style=" background-color: #9fd3bc ;
  color: #0f5132;
  padding: 12px;
  margin: 10px 20px;
  font-weight: bold;
  border-radius: 5px;
  font-family: 'Segoe UI', sans-serif;
  text-align: center;">
    {{ successMessage }}
  </div>

  <!-- Delete Confirmation Modal -->
  <div v-if="showDeleteConfirm" class="modal-overlay">
    <div class="modal">
      <p>Are you sure you want to delete this chat?</p>
      <div class="modal-buttons">
        <button @click="performDelete" class="confirm-btn">Yes, Delete</button>
        <button @click="cancelDelete" class="cancel-btn">Cancel</button>
      </div>
    </div>
  </div>

  <div class="mainChat flex">
    <!-- Sidebar: Chat List -->
    <div class="sideNames">
      <div class="chat-list-column">
        <div class="chatNames flex items-center justify-between px-3 py-2 cursor-pointer hover:bg-gray-100"
          :class="{ 'active-chat': conversation.id === activeConversation.id }" v-for="conversation in conversations"
          :key="conversation.id" @click="setActiveConversation(conversation.id)">
          <div class="user-wrapper">
            <img :src="getAvatarUrl(getOtherUser(conversation.users)?.avatar)" class="user-avatar" alt="avatar" />
            <p class="user-name">
              {{ getOtherUser(conversation.users)?.firstName || '...' }}
              {{ getOtherUser(conversation.users)?.lastName || '' }}
            </p>
          </div>

          <!-- Styled Delete Button -->
          <button class="delete-btn" @click.stop="confirmDelete(conversation.id)" title="Delete chat">
            🗑️
          </button>
        </div>
      </div>
    </div>

    <!-- Main Chat Panel -->
    <div class="flex" style="flex-direction: column; gap: 2vh;">
      <div class="chat flex flex-col">
        <!-- Recipient Name -->
        <div class="w-[40vw] py-3 px-4 bg-white border-b border-gray-200 text-lg font-semibold">
       <template v-if="activeConversation && activeConversation.id">
            <template
              v-for="user in conversations.find(c => c.id === activeConversation.id)?.users || []"
              :key="user.id"
            >
              <router-link
                :to="{ name: 'UserProfile', params: { id: user.id } }"
              >
                <span v-if="user.id !== userStore.user.id">
                  {{ user.firstName }} {{ user.lastName }}
                </span>
              </router-link>
            </template>
          </template>

        
        </div>

        <!-- Messages -->
        <div ref="chatScroll" class="message-list w-[40vw] overflow-y-auto space-y-3">
          <template v-for="message in activeConversation.messages" :key="message.id">
            <div v-if="message.created_by.id === userStore.user.id"
              class="flex bg-white w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
              <div>
                <div
                  class="bg-blue text-white p-3 rounded-l-lg rounded-br-lg flex flex-col gap-2 max-w-[300px] break-words">
                  <p v-if="message.body" class="text-sm" style="padding: 1vh; text-align: right;">
                    {{ message.body }}
                  </p>
                  <img v-if="message.image" :src="getFullImageUrl(message.image)" alt="sent image"
                    class="max-w-full rounded-md" style="max-height: 200px; object-fit: contain;" />
                </div>
                <span class="text-xs text-gray leading-none">
                  {{ message.created_at_formatted }} ago
                </span>
              </div>
            </div>

            <!-- Received -->
            <div v-else class="otherChat flex bg-white w-full mt-2 space-x-3 max-w-md mr-auto justify-start">
              <div class="flex-shrink-0 h-10 w-10 rounded-full">
                <img :src="getAvatarUrl(message.created_by?.avatar)" class="w-[40px] rounded-full"
                  alt="sender avatar" />
              </div>
              <div>
                <div
                  class="bg-gray-300 text-black p-3 rounded-r-lg rounded-bl-lg flex flex-col gap-2 max-w-[300px] break-words"
                  style="text-align: right;">
                  <p v-if="message.body" class="text-sm">{{ message.body }}</p>
                  <img v-if="message.image" :src="getFullImageUrl(message.image)" alt="received image"
                    class="max-w-full rounded-md" style="max-height: 200px; object-fit: contain;" />
                </div>
                <span class="text-xs text-gray-500 leading-none">
                  {{ message.created_at_formatted }} ago
                </span>
              </div>
            </div>
          </template>
        </div>
      </div>

      <!-- Message Form -->
      <div class="bg-white rounded-lg">
        <form @submit.prevent="submitForm">
          <div class="p-4 flex flex-col gap-2">
            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg"
              placeholder="What do you want to say?"></textarea>
            <div class="flex items-center gap-4">
              <button type="button" @click="$refs.fileInput.click()" class="text-xl" title="Attach Image"><img
                  width="50" height="50" src="https://img.icons8.com/ios/50/image--v1.png" alt="image--v1" /></button>
              <input ref="fileInput" type="file" accept="image/*" @change="onFileChange" style="display: none;" />
              <button class="inline-block  text-white rounded-lg"
                style="background-color: lightgreen; border: 3px solid black; font-family: Concert One, serif; font-size: 1.1vw; height: 5vh; width: 4vw;">
                SEND
              </button>
            </div>
            <div v-if="selectedImage" class="image-preview mt-2 flex" style="flex-direction: column;">
              <img :src="imagePreview" alt="Preview" class="max-w-full max-h-48 rounded-md" />
              <button type="button" @click="removeImage" class="text-red-600 mt-1 underline rmv-btn">
                REMOVE
              </button>
            </div>
          </div>


        </form>
      </div>
    </div>
  </div>
  
  <Footer/>
  
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import Navbar from "@/layouts/Navbar.vue";
import Footer from '@/layouts/Footer.vue'


export default {
  name: 'chat',
  components: { Navbar, Footer },

  setup() {
    const userStore = useUserStore()
    return { userStore }
  },

  data() {
    return {
      conversations: [],
      activeConversation: {},
      body: '',
      selectedImage: null,
      imagePreview: null,
      showDeleteConfirm: false,
      deleteTargetId: null,
      successMessage: ''
    }
  },

  mounted() {
    this.getConversations()
  },

  updated() {
    this.scrollToBottom()
  },

  methods: {
    scrollToBottom() {
      this.$nextTick(() => {
        const el = this.$refs.chatScroll
        if (el) el.scrollTop = el.scrollHeight
      })
    },

    getAvatarUrl(avatarPath) {
      if (!avatarPath) return '/default-avatar.png'
      return avatarPath.startsWith('http') ? avatarPath : `http://localhost:8000${avatarPath}`
    },

    getFullImageUrl(imagePath) {
      if (!imagePath) return ''
      return imagePath.startsWith('http') ? imagePath : `http://localhost:8000${imagePath}`
    },

    getOtherUser(users) {
      return Array.isArray(users) ? users.find((user) => user.id !== this.userStore.user.id) : {}
    },

  setActiveConversation(id) {
  axios.get(`/api/chat/${id}/`, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('user.access')}`,
    },
  })
  .then((response) => {
    this.activeConversation = response.data
    this.scrollToBottom()
  })
  .catch(console.log)
}
,

    getConversations() {
      axios.get('/api/chat/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('user.access')}`,
        },
      })
      .then((response) => {
        this.conversations = response.data
        if (this.conversations.length) {
          this.activeConversation = this.conversations[0]
          this.getMessages()
        }
      })
      .catch(console.log)
    },getOtherUser(users) {
  return Array.isArray(users) ? users.find((user) => user.id !== this.userStore.user.id) : {}
},

    getMessages() {
      if (!this.activeConversation?.id) return
      axios.get(`/api/chat/${this.activeConversation.id}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('user.access')}`,
        },
      })
      .then((response) => {
        this.activeConversation = response.data
        window.dispatchEvent(new Event('refresh-unread'))
      })
      .catch(console.log)
    },

    onFileChange(event) {
      const file = event.target.files[0]
      if (!file) return
      this.selectedImage = file
      this.imagePreview = URL.createObjectURL(file)
    },

    removeImage() {
      this.selectedImage = null
      this.imagePreview = null
      if (this.$refs.fileInput) this.$refs.fileInput.value = null
    },

    submitForm() {
      if (!this.activeConversation.id) return
      const formData = new FormData()
      formData.append('body', this.body)
      if (this.selectedImage) formData.append('image', this.selectedImage)

      axios.post(`/api/chat/${this.activeConversation.id}/send/`, formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('user.access')}`,
          'Content-Type': 'multipart/form-data',
        },
      })
      .then((response) => {
        this.activeConversation.messages.push(response.data)
        this.body = ''
        this.selectedImage = null
        this.imagePreview = null
      })
      .catch(console.log)
    },

    confirmDelete(id) {
      this.showDeleteConfirm = true
      this.deleteTargetId = id
    },

    cancelDelete() {
      this.showDeleteConfirm = false
      this.deleteTargetId = null
    },

    performDelete() {
      axios.delete(`/api/chat/${this.deleteTargetId}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('user.access')}`,
        },
      })
      .then(() => {
        this.conversations = this.conversations.filter(c => c.id !== this.deleteTargetId)
        if (this.activeConversation.id === this.deleteTargetId) {
          this.activeConversation = this.conversations[0] || {}
          if (this.activeConversation.id) this.getMessages()
        }
        this.successMessage = 'Chat deleted successfully!'
        setTimeout(() => this.successMessage = '', 3000)
        this.cancelDelete()
      })
      .catch((err) => {
        console.error('Failed to delete conversation:', err)
        alert('Failed to delete conversation.')
      })
    }
  }
}
</script>


<style scoped>


.mainChat {
  gap: 4vw;
  position: relative;
  top: 5vh;
}
.bg-blue p,
.bg-gray-300 p {
  text-align: left !important;
}

.sideNames {
  width: 30vw;
  height: 70vh;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 2vw;
  box-sizing: border-box;
}

.chat-list-column {
  display: flex;
  flex-direction: column;
  gap: 2vh;
}

.chatNames {
  border: 2px solid rgb(207, 207, 207);
  height: 10vh;
  border-radius: 40px;
  gap: 12px;
  width: 100%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chatNames:hover {
  background-color:  rgb(239, 255, 239);
}

.active-chat {
  background-color: #e9e9e9 !important;
}
.active-chat:hover {
  background-color: rgb(239, 255, 239) !important;
}

.delete-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #d32f2f;
  padding: 0 8px;
  user-select: none;
}

.delete-btn:hover {
  color: #9a0007;
}

.chat {
  height: 60vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 2px solid rgb(214, 214, 214);
  border-radius: 30px;
}

.message-list {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1.5rem 1rem;
}

.otherChat {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  margin-top: 0.5rem;
  gap: 1vh;
}

.otherChat p {
  font-size: 0.875rem;
}

.otherChat .bg-gray-300 {
  padding: 7px;
  border-radius: 0.75rem 0.75rem 0.75rem 0;
}

.user-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex-shrink: 0;
}

.user-name {
  font-size: 20px;
  font-weight: 600;
  color: black;
  white-space: nowrap;
}

::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #ffffff;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 10px;
  border: 2px solid #ffffff;
}

::-webkit-scrollbar-thumb:hover {
  background: #5f5f5f;
}

textarea {
  height: 70px;
  width: 40vw;
  resize: none;
  overflow-y: auto;
  padding: 10px;
  border: 2px solid rgb(214, 214, 214);
  outline: none;
}

.image-preview img {
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
}
a
.success-banner {
  background-color: #9fd3bc !;
  color: #0f5132;
  padding: 12px;
  margin: 10px 20px;
  font-weight: bold;
  border-left: 6px solid #0f5132;
  border-radius: 5px;
  font-family: 'Segoe UI', sans-serif;
  text-align: center;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0,0,0,0.4);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0,0,0,0.2);
  width: 320px;
  text-align: center;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.confirm-btn,
.cancel-btn {
  padding: 8px 16px;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

.confirm-btn {
  background-color: #dc3545;
  color: white;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.rmv-btn{
  width: 6vw;
  height: 5vh;
  background-color: rgb(155, 70, 70);
  color: white;
  text-decoration: none;
  border-radius: 30px;
  border: 3px solid black;
}
</style>
