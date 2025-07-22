<template>
  <Navbar />
  <div class="auctionCont">
    <div class="createdAuction flex">
      <h1>CREATE AN AUCTION</h1>
      <router-link to="/auctions/create"><img style="width: 32vw;" src="@/assets/createAuction.png" alt=""></router-link>
    </div>

    <!-- Vertical Divider -->
    <div class="vertical-divider"></div>

    <div class="placeBid flex">
      <h1>PLACE A BID</h1>
      <router-link to="/auctions"><img src="@/assets/placeBid.png" alt=""></router-link>
    </div>
  </div>
  <Footer/>
</template>

<script>
import Navbar from '@/layouts/Navbar.vue';
import Footer from '@/layouts/Footer.vue'
    export default{
        name:'InitialAuction',
        components:{
            Navbar,
            Footer
        }
    }
</script>

<style scoped>
.auctionCont {
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
}

.auctionCont img {
  width: 30vw;
  transition: transform .2s;
}
.auctionCont img:hover{
    transform: scale(1.05);
}

.createdAuction,
.placeBid {
  width: 45vw;
  flex-direction: column;
  display: flex;
  align-items: center;
}

.vertical-divider {
  width: 1px;
  height: 75vh;
  background-color: rgb(212, 212, 212);
  margin: 0 1vw;
}

h1 {
  font-family: "Concert One", serif;
  font-size: 4vw;
  color: rgb(163, 194, 163);
}

</style>