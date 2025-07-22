<template>
    <Navbar/>
    <ItemDetails/>
    <!-- <SimilarProducts/> -->
    <Footer/>
</template>

<script>
import ItemDetails from '@/components/PDComponents/ItemDetails.vue';
import Navbar from '@/layouts/Navbar.vue';
import SimilarProducts from '@/components/PDComponents/SimilarProducts.vue';
import Footer from '@/layouts/Footer.vue'


    export default{
        name:'ProductDetails',
        components:{
            Navbar,
            ItemDetails,
            SimilarProducts,
            Footer
            
        }
    }
</script>

<style scoped>

</style>