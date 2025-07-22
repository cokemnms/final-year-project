<template>
    <div class="container flex">
        <div class="otherPages flex">
            <h1>CRAFTY</h1>
            <div class="info flex">

            <img src="@/assets/UPPicture/crafty.svg" alt="">
         <p>DISCOVER CREATIVE REPURPOSED ITEMS CRAFTED BY TALENTED ARTISTS</p>
            <router-link to="/Crafty"><button>VIEW</button></router-link>
            </div>
        </div>
        <div class="otherPages flex">
            <h1>EXPLORE</h1>
            <div class="info flex">
            <img src="@/assets/UPPicture/explore.svg" alt="">
            <p>FILTER AND FIND THE BEST DEALS FROM SELLERS ACROSS THE PLATFORM</p>
          <router-link to="/recommendations"><button>VIEW</button></router-link>
            </div>
        </div>
        <div class="otherPages flex">
            <h1>SELL</h1>
            <div class="info flex">

            <img src="@/assets/UPPicture/cart.svg" alt="">
           <p>TURN YOUR UNWANTED SCRAP INTO CASH</p>
          <router-link to="/Sell"><button>VIEW</button></router-link>
            </div>
        </div>
    </div>
</template>




<script>
export default {
    name: 'OtherPages'
}
</script>

<style scoped>

*{
    font-family: "Concert One", serif;

}
.container {
 width: 90vw;
   min-height: 80vh; 
   gap: 5vw;
   position: relative;
   top: 10vw;
   margin: auto;
}
.otherPages{
    flex-direction: column;
    height: 85vh;
}
img {
    width: 32vw;
    height: 44vh;
}

h1{
    font-size: 5vw;
    font-family: "Concert One", serif;
    color: rgb(132, 172, 132);
}
.info{
    flex-direction: column;
    border: 2px solid rgb(180, 180, 180);
    width: 23vw;
    height: 75vh;
    padding: 10px;
    text-align: center;
    border-radius: 40px;
    font-size: 1.2vw;
}

button {
    width: 7vw;
    height: 5vh;
    border-radius: 30px;
    background-color: lightgreen;
    color: white;
    border: 3px solid rgb(0, 0, 0);
    position: relative;
    top: 2vh;
}
</style>