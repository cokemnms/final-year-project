<template>
    <footer class="flex">
      <hr style="position: relative; bottom: 1vh; width: 90vw; left: 0vw; border: .2px solid white;">
      <div class="footerCont flex">
        <div class="footerSec flex">
          <h3>About Us</h3>
          <!-- This router-link navigates to the About Us page -->
          <router-link to="/AboutUs">About us</router-link>
          <h6>LOREM</h6>
        </div>
        <div class="footerSec flex">
          <h3>Popular Categories</h3>
          <h6>LOREM</h6>
          <h6>LOREM</h6>
        </div>
        <div class="footerSec flex">
          <h3>Scrapy</h3>
          <h6>LOREM</h6>
          <h6>LOREM</h6>
        </div>
      </div>
      <div class="footerEnd flex">
        <h5>&copy; 2025 Scrapy. All Rights Reserved.</h5>
      </div>
    </footer>
  </template>
<script>

export default{
        name:'Footer'
    }
</script>

<style scoped>
/* @import 'src/style.css'; */
    footer{
        width: 100vw;
        height: 41.5vh;
        /* border: 2px solid black; */
        position:relative;
        bottom: 130vh;
        flex-direction: column;
        gap: 2vh;
        color: white;
    background-color:#9CCC65;



    }
    .footerSec{
        width: 25vw;
        height: 30vh;
        /* border: 2px solid black; */
        font-family: "Concert One", serif;
        font-size: 2vw;
        flex-direction: column;
    }
    .footerSec h6{
        font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    }
    .footerCont{
        
        gap: 5vw;
    }
    .footerEnd{
        /* border: 2px solid black; */
        width: 90vw;
        height: 6vh;
    }
</style>