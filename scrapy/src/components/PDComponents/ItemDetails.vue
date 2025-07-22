<template>
  <div>
    <div class="mainCont flex" v-if="post">
      <v-carousel hide-delimiters height="800" v-if="post.attachments && post.attachments.length">
  <v-carousel-item
    v-for="(attachment, index) in post.attachments"
    :key="index"
    :src="attachment.get_image"
    cover
  />
</v-carousel>


      <div class="details flex">
        <div class="sellerInfo flex">
          <h2 style="font-size: 3vw;  color: rgb(190, 211, 190); position: relative; bottom: 2vh;  font-family: 'Concert One', serif;">Seller</h2>
          <div class="seller flex">
            <img src="@/assets/developers/ayyan.jpg" alt="Seller" />
            <div class="contactSeller flex">
              <h2 style="font-size: 1.5vw;">
                {{ post.user?.firstName }} {{ post.user?.lastName }}
              </h2>
              <div class="contactButtons flex">
                <button @click="goToSellerProfile">
                  Show Seller Info
                </button>
                <button @click="sendDirectMessage" v-if="post?.user?.id && userStore.user?.id !== post.user.id">
                  CHAT
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="itemInfo">
          <h1>{{ post.title }}</h1>
          <h2>Rs {{ post.price }}</h2>

          <div class="desc flex">
            <h3>DESCRIPTION</h3>
            <p>{{ post.description }}</p>

            <h3>CONDITION</h3>
            <p>{{ post.condition }}</p>

            <h3>CONTACT</h3>
            <p>{{ post.contact }}</p>

            <h3>DELIVERY</h3>
            <p>{{ post.delivery }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Similar Products -->
    <div class="similarProducts" v-if="similarPosts.length">
      <h2 class="similarHeading">SIMILAR PRODUCTS</h2>
      <div class="similarGrid">
        <div v-for="post in similarPosts" :key="post.id" class="similarCard" @click="$router.push({ name: 'ProductDetails', params: { id: post.id } })">
           <RouterLink :to="{ name: 'ProductDetails', params: { id: post.id } }" class="item-link">

             <img :src="post.attachments?.[0]?.get_image || '/default.jpg'" alt="post image" />
             <h3>{{ post.title }}</h3>
             <p>Rs {{ post.price }}</p>
             <p>{{ post.user.city }}</p>
            </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
  name: 'ProductDetails',
  data() {
    return {
      post: null,
      similarPosts: []
    }
  },
  setup() {
    const userStore = useUserStore()
    return { userStore }
  },
  created() {
    this.fetchPost(this.$route.params.id)
  },
  methods: {
    async fetchPost(id) {
      const token = localStorage.getItem('user.access')
      try {
        const response = await axios.get(`http://localhost:8000/api/scrap-posts/scrapposts/${id}/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        this.post = response.data

        if (this.post?.category) {
          const similarRes = await axios.get(`http://localhost:8000/api/scrap-posts/category/${this.post.category}/`, {
            headers: { Authorization: `Bearer ${token}` }
          })

          this.similarPosts = similarRes.data
            .filter(p => p.id !== this.post.id)
            .slice(0, 8)
        }

      } catch (error) {
        console.error('Error loading scrap post or similar posts:', error)
      }
    },
    goToSellerProfile() {
      if (this.post?.user?.id) {
        this.$router.push({ name: 'UserProfile', params: { id: this.post.user.id } })
      }
    },
    sendDirectMessage() {
      if (!this.post?.user?.id) return
      axios
        .get(`/api/chat/${this.post.user.id}/get-or-create/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('user.access')}`
          }
        })
        .then(() => this.$router.push('/chat'))
        .catch(console.error)
    }
  },
  watch: {
    '$route.params.id': {
      immediate: true,
      handler(newId) {
        this.fetchPost(newId)
      }
    }
  }
}
</script>

<style scoped>
.mainCont {
  width: 100vw;
  height: 80vh;
  gap: 3vw;
  margin-top: 5vh;
  margin-bottom: 5vh;
}

.mainCont>img {
  width: 40vw;
  height: 60vh;
  border-radius: 20px;
  box-shadow: 4px 4px 10px rgba(160, 160, 160, 0.6);
}

.details {
  width: 32vw;
  height: 70vh;
  flex-direction: column;
  gap: 3vh;
}

.itemInfo {
  width: 100%;
  max-width: 32vw;
  box-sizing: border-box;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 4px 4px 10px rgba(202, 202, 202, 0.6);
}

.sellerInfo {
  width: 32vw;
  height: 27vh;
  border-radius: 20px;
  flex-direction: column;
  align-items: start;
  padding: 20px;
  box-shadow: 4px 4px 10px rgba(202, 202, 202, 0.6);
}

.seller {
  gap: 2vw;
}

.desc {
  flex-direction: column;
  align-items: start;
  gap: 0.5vh;
}

.sellerInfo img {
  width: 6vw;
  height: 12vh;
  border-radius: 50%;
}

.contactSeller {
  flex-direction: column;
  align-items: start;
  gap: 1vh;
}

.contactButtons {
  gap: 1vw;
}

.contactButtons button {
  width: 9vw;
  height: 6vh;
  border: 2px solid black;
  background-color: rgb(190, 211, 190);
  border-radius: 20px;
  color: white;
}

h1 {
  font-size: 2.5vw;
  color: rgb(144, 170, 144);
}

h3 {
  font-size: 1.7vw;
  font-family: "Concert One", serif;
}

h4 {
  font-size: 1.1vw;
}

p {
  color: grey;
  font-size: 1vw;
}

h3,
h4 {
  color: rgb(88, 88, 88);
}

h2 {
  font-size: 1.2vw;
}

.similarProducts {
  padding: 2vw 5vw;
  margin-bottom: 5vh;
}

.similarHeading {
  font-size: 4vw;
  font-family: 'Concert One', serif;
  color: rgb(144, 170, 144);
  margin-bottom: 2vh;
}

.similarGrid {
  display: flex;
  flex-wrap: wrap;
  gap: 2vw;
}

.similarCard {
  width: 20vw;
  padding: 1vw;
  border-radius: 15px;
  box-shadow: 2px 2px 8px rgba(180, 180, 180, 0.5);
  cursor: pointer;
  transition: 0.3s ease;
  background: white;
}

.similarCard p{
  font-size: 3vw;
}

.similarCard:hover {
  transform: scale(1.03);
}

.similarCard img {
  width: 100%;
  height: 30vh;
  object-fit: cover;
  border-radius: 10px;
}

.similarCard h3 {
  font-size: 1.3vw;
  margin-top: 0.5vh;
}

.similarCard p {
  font-size: 1vw;
  color: gray;
}
.v-carousel{
  width: 45vw;
}
</style>
