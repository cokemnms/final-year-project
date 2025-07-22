<template>
  <Navbar />
  <hr style="position: relative; bottom: 0vh; width: 90vw; left: 5vw; border: 1px solid lightgray;">
  <h1 class="heading">Share Your Treasure</h1>
  <div class="categories">
    <div
      class="category"
      v-for="cat in categories"
      :key="cat"
      @click="goToSell(cat)"
    >
      <img src="" alt="">
      <h1>{{ cat }}</h1>
    </div>
  </div>
  <Footer/>
</template>

<script>
import Navbar from '@/layouts/Navbar.vue';
import Footer from '@/layouts/Footer.vue'
export default {
  name: 'DisplayCategories',
  components: {
    Navbar,
    Footer
  },
  data() {
    return {
      categories: ['Metal', 'Wood', 'Glass', 'Textile', 'Electronic', 'Paper', 'Furniture','Plastic']
    };
  },
  methods: {
    goToSell(category) {
      this.$router.push({ name: 'Sell', query: { category } });
    }
  }
};
</script>

<style scoped>
.categories {
  width: 100vw;
  height: 50vh;
  flex-wrap: wrap;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2vw;
  position: relative;
  top: 5vh;
}

.category {
  width: 22vw;
  height: 15vh;
  border: 2px solid rgb(224, 224, 224);
  box-shadow: 1px 3px 10px 1px rgb(207, 207, 207);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50px;
  cursor: pointer;
}

.heading {
  color: lightgreen;
  font-size: 6vw;
  font-family: "Concert One", serif;
  position: relative;
  top: 2vh;
  left: 23vw;
}

.category h1 {
  font-size: 2.8vw;
  font-family: "Concert One", serif;
  color: black;
}
</style>
