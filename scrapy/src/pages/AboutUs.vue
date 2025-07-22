<template>
    <Navbar/>
    <Vision/>
    <Developers/>
    <Footer/>
</template>


<script>

import Developers from "@/components/AboutUsComponents/Developers.vue";
import Vision from "@/components/AboutUsComponents/Vision.vue";
import Navbar from "@/layouts/Navbar.vue";
import Footer from '@/layouts/Footer.vue'
    export default{
        name:'AboutUs',
        components:{
            Navbar,
            Developers,
            Vision,
            Footer
        }
    }
</script>

<style>


</style>