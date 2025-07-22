<template>
    <div class="footerCont flex">

        <div class="footerHead flex">
            <h1>SCRAPY</h1>
        </div>
        <div class="footerNav flex">
            <router-link to="/MainPage"><h2>HOME</h2></router-link>
            <router-link to="/Sell"><h2>POST SCRAP</h2></router-link>
            <router-link to="/auctions"><h2>AUCTIONS</h2></router-link>
            <router-link to="/Recommendations"><h2>FOR YOU</h2></router-link>
            <router-link to="/Crafty"><h2>CRAFTY</h2></router-link>
            <router-link to="/Chat"><h2>CHAT</h2></router-link>
            <router-link to="/MainPage"><h2>CATEGORIES</h2></router-link>
            <router-link to="/AboutUs"><h2>ABOUT US</h2></router-link>
           
        </div>
        <div class="copyright flex" style="margin-top: 5vh;">
            <p>&copy; 2025 SCRAPY. All Rights Reserved.</p>
        </div>
    </div>

</template>

<script>

</script>

<style scoped>
.footerCont {
  background-color: rgb(149, 194, 149);
  /* border-top: 3px solid black; */
  padding: 1rem;
  margin-top: 30vh;
  flex-direction: column;
}

h1{
    font-size: 6vw;
  font-family: "Concert One", serif;
  color: rgb(94, 156, 115);
  
}
h2{
    
    font-family: "Concert One", serif;
    font-size: 2.7VW;
    color: whitesmoke;
    transition: transform .2s;
}

h2:hover{
    transform: scale(1.1);
}
.footerNav{
    column-gap: 3vw;
    row-gap: 2vw;
    width: 60vw;
    flex-wrap: wrap;
}
</style>