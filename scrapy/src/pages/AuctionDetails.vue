<template>
  <Navbar />
  <div class="auction-detail flex" v-if="auction" style="width: 100vw;">
    <div class="aucImages" style="width: 60vw;">
      <!-- ✅ Vuetify Carousel for Images -->
      <v-carousel
        v-if="auction.images && auction.images.length"
        cycle
        show-arrows
        hide-delimiters
        height="600"
      >
        <v-carousel-item
          v-for="(image, index) in auction.images"
          :key="index"
          :src="image"
          cover
        ></v-carousel-item>
      </v-carousel>

      <!-- User Info -->
      <div class="user-info" v-if="auction.created_by" style="display: flex; align-items: center; gap: 1vw; margin-top: 20px;">
        <img
          v-if="auction.created_by.avatar"
          :src="auction.created_by.avatar"
          alt="User Avatar"
          class="bidder-avatar"
        />
        <div>
          <router-link
            :to="{ name: 'UserProfile', params: { id: auction.created_by.id } }"
            class="user-name-link"
          >
            <strong>{{ auction.created_by.firstName }} {{ auction.created_by.lastName }}</strong>
          </router-link>
        </div>
      </div>

      <h2 class="heading">{{ auction.title }}</h2>
      <p class="description">{{ auction.description }}</p>
      <p class="price">Current Base Price: Rs {{ auction.base_price }}</p>

      <h3 class="subheading">PLACE A BID</h3>
      <form @submit.prevent="placeBid" class="bid-form">
        <input v-model.number="bidAmount" type="number" placeholder="Bid Amount" class="input" />
        <button type="submit" class="button">Bid</button>
      </form>
    </div>

    <div class="aucHistory">
      <!-- ⏳ Countdown Timer -->
      <div class="timer" v-if="countdown">
        <p><strong>Time Remaining:</strong> {{ countdown }}</p>
      </div>

      <h3 class="subheading">CURRENT HIGHEST BIDDER</h3>
      <div class="highestBid" v-if="highestBid">
        <img
          v-if="highestBid.bidder.avatar"
          :src="highestBid.bidder.avatar"
          alt="avatar"
          class="bidder-avatar"
        />
        <p>{{ highestBid.bidder.firstName }} {{ highestBid.bidder.lastName }}</p>
        <p>Rs {{ highestBid.amount }}</p>
      </div>

      <h3 class="subheading">BID HISTORY</h3>
      <ul class="bid-history">
        <li v-for="bid in [...auction.bids].reverse()" :key="bid.id" class="bid-entry">
          <img
            v-if="bid.bidder.avatar"
            :src="bid.bidder.avatar"
            alt="avatar"
            class="bidder-avatar"
          />
          <div>
            <p>{{ bid.bidder.firstName }} {{ bid.bidder.lastName }}</p>
            <p>Rs {{ bid.amount }}</p>
          </div>
          <button class="delete-bid-btn" @click="deleteBid(bid.id)" title="Delete Bid">
            ✖
          </button>
        </li>
      </ul>
    </div>
  </div>
  <Footer />
</template>

<script>
import Navbar from '@/layouts/Navbar.vue'
import Footer from '@/layouts/Footer.vue'
import axios from 'axios'

export default {
  name: 'AuctionDetail',
  components: {
    Navbar,
    Footer
  },
  data() {
    return {
      auction: null,
      bidAmount: '',
      countdown: '',
      timer: null
    }
  },
  computed: {
    highestBid() {
      if (!this.auction || !this.auction.bids || !this.auction.bids.length) return null;
      return this.auction.bids.reduce((max, bid) =>
        bid.amount > max.amount ? bid : max, this.auction.bids[0]
      );
    }
  },
  mounted() {
    const token = localStorage.getItem('user.access')

    axios
      .get(`/api/auctions/${this.$route.params.id}/`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then((res) => {
        this.auction = res.data
        this.startCountdown()
      })
      .catch((err) => {
        console.error('Auction detail fetch failed:', err)
      })
  },
  beforeUnmount() {
    clearInterval(this.timer)
  },
  methods: {
    startCountdown() {
      if (!this.auction || !this.auction.expires_at) return

      const targetDate = new Date(this.auction.expires_at).getTime()

      this.timer = setInterval(() => {
        const now = new Date().getTime()
        const distance = targetDate - now

        if (distance < 0) {
          clearInterval(this.timer)
          this.countdown = 'Auction Ended'
          return
        }

        const days = Math.floor(distance / (1000 * 60 * 60 * 24))
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
        const seconds = Math.floor((distance % (1000 * 60)) / 1000)

        this.countdown = `${days}d ${hours}h ${minutes}m ${seconds}s`
      }, 1000)
    },
    placeBid() {
      axios
        .post(
          `/api/auctions/${this.$route.params.id}/bid/`,
          {
            amount: this.bidAmount
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('user.access')}`
            }
          }
        )
        .then((response) => {
          if (response.data.status === 'warning') {
            alert(response.data.message)
          } else {
            window.location.reload()
          }
        })
        .catch((err) => {
          console.error(err)
        })
    },
    deleteBid(bidId) {
      const token = localStorage.getItem('user.access')

      axios
        .delete(`/api/bids/${bidId}/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(() => {
          this.auction.bids = this.auction.bids.filter((bid) => bid.id !== bidId)
        })
        .catch((err) => {
          console.error('Failed to delete bid:', err)
        })
    }
  }
}
</script>

<style scoped>
.auction-detail {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  gap: 5vw;
}

.heading {
  font-size: 28px;
  font-weight: bold;
  margin-top: 16px;
}

.description {
  margin: 10px 0;
  color: #555;
}

.price {
  font-size: 18px;
  font-weight: 600;
}

.subheading {
  font-size: 3vw;
  margin-top: 20px;
  margin-bottom: 10px;
  font-family: "Concert One", serif;
  text-align: center;
}

.bid-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  flex: 1;
}

.button {
  background-color: #28a745;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.bid-history {
  list-style: none;
  padding: 0;
}

.bid-entry {
  padding: 10px;
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);
  width: 25vw;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  gap: 1vw;
  border-radius: 20px;
}

.bidder-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #ccc;
}

.delete-bid-btn {
  background-color: #dc3545;
  border: none;
  color: white;
  padding: 6px 10px;
  font-size: 14px;
  border-radius: 50%;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete-bid-btn:hover {
  background-color: #a71d2a;
}

.aucHistory {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.v-carousel {
  width: 50vw;
}

.highestBid {
  width: 15vw;
  height: 10vh;
  border-radius: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);
  flex-direction: column;
}

.timer {
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: bold;
  color: #dc3545;
}
</style>
