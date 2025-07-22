<template>
  <Navbar />
  <div class="auctionHead">
    <img src="@/assets/bid.png" alt="">
    <h1>THE CLOCK IS TICKING! <br> BID BEFORE ITS GONE</h1>
  </div>
  <div class="auction-list">
    <h2 class="heading">LIVE AUCTIONS</h2>
    <div class="auction-grid">
      <div v-for="auction in sortedAuctions" :key="auction.id" class="auction-card">
        <img :src="auction.images[0]" alt="auction image" class="auction-image" />


        <h3 class="auction-title">{{ auction.title }}</h3>
        <p class="auction-user">{{ auction.created_by.firstName }} {{ auction.created_by.lastName }} </p>
        <p class="auction-price">Rs {{ auction.base_price }}</p>
        <div class="auctionButtons">
   

         <router-link :to="`/auctions/${auction.id}`" class="auction-link">
  View Auction
</router-link>

          <button @click="confirmDelete(auction.id)" class="delete-button" style="color: red;">
            Delete
          </button>
        </div>

      </div>
    </div>
  </div>
  <Footer/>
</template>

<script>
import Navbar from '@/layouts/Navbar.vue'
import Footer from '@/layouts/Footer.vue'
import axios from 'axios'

export default {
  name: 'AuctionList',
  components: {
    Navbar,
    Footer
  },
  data() {
    return {
      auctions: []
    }
  },
  computed: {
    // Sort auctions by created_at descending (latest first)
    sortedAuctions() {
      return this.auctions.slice().sort((a, b) => {
        // Convert to Date objects for comparison
        return new Date(b.created_at) - new Date(a.created_at)
      })
    }
  },
  mounted() {
    const token = localStorage.getItem('user.access')
    axios
      .get('/api/auctions/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(res => {
        this.auctions = res.data
        console.log("Auction image URLs:", this.auctions.map(a => a.image_url))
       console.log(this.auctions) // ✅ Valid
        console.log(this.auctions.map(a => a.id)) // ✅ Valid


      })
      .catch(err => {
        console.error('Auction fetch failed:', err)
      })
  },
  methods: {
  confirmDelete(auctionId) {
    if (confirm("Are you sure you want to delete this auction?")) {
      const token = localStorage.getItem('user.access')
      axios
        .delete(`/api/auctions/${auctionId}/delete/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        .then(() => {
          this.auctions = this.auctions.filter(a => a.id !== auctionId)
          alert("Auction deleted successfully.")
        })
        .catch(err => {
          console.error("Delete failed:", err)
          alert("Failed to delete auction.")
        })
    }
  }
}

}
</script>

<style scoped>
.auction-list {
  padding: 20px;
}

.heading {
  font-size: 4vw;
  font-weight: bold;
  margin-bottom: 16px;
  font-family: "Concert One", serif;
  margin-left: 3vw;

}

.auction-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 2vw;
  justify-content: center;
}

.auction-card {
  box-shadow: 1px 3px 7px 2px rgb(198, 198, 198);

  padding: 16px;
  border-radius: 8px;
  width: 21vw;
  height: 50vh;
  font-size: 1.1vw;

}

.auction-image {
  width: 100%;
  height: 30vh;
  object-fit: cover;
  border-radius: 4px;
}

.auction-title {
  font-size: 18px;
  margin-top: 10px;
}

.auction-user {
  font-style: italic;
  color: #777;
  margin-top: 4px;
}

.auction-price {
  color: #555;
}

.auction-link {
  color: #007BFF;
  text-decoration: none;
  margin-top: 8px;
  display: inline-block;
}

.auctionHead {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
}

.auctionHead img {
  width: 40vw;
}

.auctionHead h1 {
  font-size: 5vw;
  font-family: "Concert One", serif;

}
.auctionButtons{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2vw;
}
</style>
