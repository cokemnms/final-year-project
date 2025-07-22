<template>
    <div class="developers">

        <h1>DEVELOPERS</h1>
        <div class="devs flex">
             <div class="coder flex">
                <img src="@/assets/developers/abdullah.jpg" alt="">
                <div class="coderInfo flex">
                    
                    <h2> Abdullah Habib</h2>
                    <p>22 years old</p>
                    <p>Frontend Developer</p>
                 
                            <div class="socialMedia"><a href="https://www.instagram.com/abdullah_habibb?igsh=MXg5dGZtNGxpYzBnNA=="><img width="50" height="50" src="https://img.icons8.com/ios/50/instagram-new--v1.png" alt="instagram-new--v1"/></a><a href="https://www.facebook.com/share/1FGMkRp9ow/?mibextid=wwXIfr"><img width="50" height="50" src="https://img.icons8.com/ios/50/facebook-new.png" alt="facebook-new"/></a><a href="https://www.linkedin.com/in/cokemnms?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app"><img width="50" height="50" src="https://img.icons8.com/ios/50/linkedin.png" alt="linkedin"/></a></div>
                </div>
            </div>
            
            <div class="coder flex">
                <img src="@/assets/developers/ayyan.jpg" alt="">
                <div class="coderInfo flex">
                    
                    <h2>Ayyan Nakai</h2>
                    <p>23 years old</p>
                    <p>Full Stack Developer</p>
                    <div class="socialMedia"><a href="https://www.instagram.com/ayyannakaii?igsh=MWNkcGQwbG0zeTZqZw=="><img width="50" height="50" src="https://img.icons8.com/ios/50/instagram-new--v1.png" alt="instagram-new--v1"/></a><a href="https://www.facebook.com/share/16oe7zZbjF/?mibextid=wwXIfr"><img width="50" height="50" src="https://img.icons8.com/ios/50/facebook-new.png" alt="facebook-new"/></a>
                    <a href="https://www.linkedin.com/in/ayyan-nakai-4759852b4?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app"><img width="50" height="50" src="https://img.icons8.com/ios/50/linkedin.png" alt="linkedin"/></a></div>
                </div>
            </div>
           
            <div class="coder flex">
                <img src="@/assets/developers/ahad.jpg" alt="">
                <div class="coderInfo flex">
                    
                    <h2>Ahad Vohra</h2>
                    <p>21 years old</p>
                    <p>Frontend Developer</p>
                    <div class="socialMedia"><a href="https://www.instagram.com/_.abdulahad1?igsh=MW1lbmdzbGhxOW5yeA=="><img width="50" height="50" src="https://img.icons8.com/ios/50/instagram-new--v1.png" alt="instagram-new--v1"/></a><a href="https://www.facebook.com/share/16UJTH4aG2/?mibextid=wwXIfr"><img width="50" height="50" src="https://img.icons8.com/ios/50/facebook-new.png" alt="facebook-new"/></a><a href="https://www.linkedin.com/in/abdul-ahad-vohra-4b553a221?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=ios_app"><img width="50" height="50" src="https://img.icons8.com/ios/50/linkedin.png" alt="linkedin"/></a></div>
                </div>
            </div>
            
        </div>
    </div>
    <!-- <Footer/> -->
    </template>

<script>
import Footer from '../MpComponents/Footer.vue';
    export default{
        name:'Developers',
        components:{
            Footer
        }
    }
</script>

<style scoped>
/* @import 'src/style.css'; */
.developers{
    position: relative;
    top: 5vh;
}
h1{
    color: lightgreen;
    font-family: "Concert One", serif;
    font-size: 4vw;
    position: relative;
    left: 3vw;
    margin-bottom: 3vw;
}
.devs{
    width: 100vw;
    height: 60vh;
    /* border: 2px solid black; */
    margin: auto 0;
    gap: 5vw;
}
.coder{
    width: 17vw;
    height: 50vh;
    /* border: 2px solid grey; */
    flex-direction: column;
    border-radius: 20px;
    box-shadow: 0 0 5px grey;
    transition: transform .2s;
}
.coder:hover{
    transform: scale(1.04);
}
.coder img{
    width: 15vw;
    height: 30vh;
    position: relative;
    bottom: 1vh;
    border-radius: 20px;
}
.coderInfo{
    flex-direction: column;
    gap: 1vh;
}
.socialMedia img{
    width: 2vw;
    height: 3.5vh;
    transition: transform .2s;
}

.socialMedia img:hover{
    transform: scale(1.1);
    
}
.socialMedia{
    position: relative;
    top: 2vh; 
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1vw;
}

h2{
    font-weight: bolder;
}
</style>