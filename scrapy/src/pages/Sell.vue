<template>
  <Navbar />
  <SellInfo :category="category" />
  <Footer/>
</template>

<script>
import SellInfo from '@/components/SellComponents/SellInfo.vue';
import Navbar from '@/layouts/Navbar.vue';
import Footer from '@/layouts/Footer.vue'

export default {
  name: 'Sell',
  components: {
    Navbar,
    SellInfo,
    Footer
  },
  data() {
    return {
      category: this.$route.query.category || ''
    };
  },
  watch: {
    '$route.query.category'(newCategory) {
      this.category = newCategory;
    }
  }
};
</script>

<style scoped>
</style>
