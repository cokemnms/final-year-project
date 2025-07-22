<template>
    <div class="vision">

        <h1>OUR VISION</h1>
        <p>"We see a world where every discarded object finds a new purpose, where creativity and sustainability coexist, and where waste is turned into wonder.  Our platform provides discarded materials to <br> artists, craftspeople, and environmentally aware people so they may produce, invent, and reuse. We hope  to decrease waste, encourage upcycling, and inspire a future <br>  in which nothing is wasted by cultivating a circular economy."</p>
    </div>
    <div class="why">
        <h1>WHY SCRAPY?</h1>
        <div class="points">
            <div class="point">
                <img width="110" height="110" src="https://img.icons8.com/3d-fluency/94/sustainability.png"           
                 alt="sustainability"/>
                 <div class="pointInfo">
                    <h2>Sustainability</h2>
                    <span>Reducing waste by promoting upcycling</span>
                 </div>
            </div>
            <div class="point">
                <img width="110" height="110" src="https://img.icons8.com/fluency/96/creativity.png" alt="creativity"/>
                  <div class="pointInfo">
                    <h2 >Creativity</h2>
                    <span>Empowering artists and DIY enthusiasts</span>
                 </div>
            </div>
            <div class="point">
                <img width="110" height="110" src="https://img.icons8.com/3d-fluency/94/group--v1.png" alt="group--v1"/>
                  <div class="pointInfo">
                    <h2>Community</h2>
                    <span> Connecting sellers and buyers with shared interests</span>
                 </div>
            </div>
            <div class="point">
                <img width="110" height="110" src="https://img.icons8.com/3d-fluency/94/motherboard.png" alt="motherboard"/>
                  <div class="pointInfo">
                    <h2>Smart Tech</h2>
                    <span>AI-Chatbot, Personalized Recommendations and Live Auctions</span>
                 </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default{
        name:'Vision'
    }
</script>

<style scoped>
.vision{
    width:100vw;
    height: 30vh;
    /* border: 2px solid black; */
    position: relative;
    top: 5vh;
}
h1{
    color: lightgreen;
    font-family: "Concert One", serif;
    font-size: 4vw;
    position: relative;
    left: 3vw;
}
p{
    text-align: center;
    font-size: 1.05vw;
    color: grey;
    position: relative;
    top: 5vh;
}
.points{
    width: 60vw;
    height: 45vh;
    position: relative;
    left: 20vw;
    top: 5vh;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2vw;
    flex-wrap: wrap;
    column-gap: 5vw;
}
.point{
    width: 25vw;
    height: 20vh;
    /* border: 2px solid grey; */
    border-radius: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1vw;
}
.why{
    /* border: 2px solid red; */
    height: 70vh;
    position: relative;
    top: 5vh;
}
/* .point img{
    width: 19vh;
    width: 7vw;
} */
.pointInfo{
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    height: 19vh;
    width:15vw ;
    text-align: center;
    

}

h2{
    font-weight: bolder;
    font-size: 2vw;
}
</style>