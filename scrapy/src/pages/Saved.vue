<template>
    <Navbar/>
    <SavedItems/>
    <Footer/>
   
</template>

<script>
    
import SavedItems from '@/components/SavedItemsComponents/SavedItems.vue';
import Navbar from '@/layouts/Navbar.vue';
import Footer from '@/layouts/Footer.vue'

    export default{
        name:'Cart',
        components:{
            Navbar,
            SavedItems,
            Footer
        }
    }
</script>

<style scoped>

</style>