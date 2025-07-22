<template>
  <Navbar />

  <div class="auction-list">
    <div class="aucHead flex">
      <img style="width: 35vw;" src="@/assets/bid.png" alt="Auction Image" />
      <h1 class="heading">THE CLOCK <br> IS TICKING! <br> BID BEFORE <br> IT'S GONE</h1>
    </div>

    <h1 class="heading" style="position: relative; left: 5vw;">LIVE AUCTIONS</h1>

    <!-- Display Auctions -->
    <div class="auction-grid">
      <div v-for="auction in sortedAuctions" :key="auction.id" class="auction-card">
        <img
          :src="auction.images && auction.images.length ? auction.images[0] : '/default-auction.jpg'"
          alt="auction image"
          class="auction-image"
        />
        <h3 class="auction-title">{{ auction.title }}</h3>
        <p class="auction-user">Posted by: {{ auction.created_by.firstName }} {{ auction.created_by.lastName }}</p>
        <p class="auction-price">Base Price: ${{ auction.base_price }}</p>
        <router-link
          :to="{ name: 'AuctionDetail', params: { id: auction.id } }"
          class="auction-link"
        >
          View Auction
        </router-link>

        <button
          v-if="userStore.user && userStore.user.id === auction.created_by.id"
          @click="deleteAuction(auction.id)"
          class="delete-button"
        >
          Delete Auction
        </button>
      </div>
    </div>
  </div>
  <Footer />
</template>

<script>
import Navbar from "@/layouts/Navbar.vue";
import Footer from '@/layouts/Footer.vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';

export default {
  name: "OtherAuctions",
  components: { Navbar, Footer },
  data() {
    return {
      auctions: []
    };
  },
  computed: {
    sortedAuctions() {
      return this.auctions.slice().sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    }
  },
  setup() {
    const userStore = useUserStore();
    return { userStore };
  },
  methods: {
    deleteAuction(id) {
      const token = localStorage.getItem('user.access');
      axios
        .delete(`/api/auctions/${id}/delete/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(() => {
          alert('Auction deleted successfully');
          this.auctions = this.auctions.filter(auction => auction.id !== id);
        })
        .catch(err => {
          console.error('Error deleting auction:', err);
          alert('Failed to delete the auction.');
        });
    }
  },
  mounted() {
    const profileUserId = this.$route.params.id;
    const token = localStorage.getItem('user.access');

    axios
      .get(`http://localhost:8000/api/auctions/user/${profileUserId}/`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        this.auctions = res.data;
      })
      .catch(err => {
        console.error('Error fetching auctions:', err);
      });
  }
};
</script>

<style scoped>
.aucHead { gap: 10vw; }
.auction-list { padding: 20px; }
.heading {
  font-size: 5vw;
  font-family: "Concert One", serif;
  margin-bottom: 16px;
}
.auction-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  width: 96vw;
  margin: auto;
  padding: 1vw 5vw;
}
.auction-card {
  border: 1px solid #ccc;
  padding: 16px;
  border-radius: 8px;
  width: 30%;
}
.auction-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 4px;
}
.auction-title { font-size: 18px; margin-top: 10px; }
.auction-user {
  font-style: italic;
  color: #777;
  margin-top: 4px;
}
.auction-price { color: #555; }
.auction-link {
  color: #007BFF;
  text-decoration: none;
  margin-top: 8px;
  display: inline-block;
}
.delete-button {
  background-color: red;
  color: white;
  border: none;
  padding: 8px;
  cursor: pointer;
  margin-top: 10px;
}
.delete-button:hover { background-color: darkred; }
</style>
