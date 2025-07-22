<template>
    <div class="categories">
        <div>
            <h1>CATEGORIES</h1>
        </div>
        <div class="select flex">
            <!-- First Row of Categories -->
            <div class="flex" style="gap: 5vw;">
                <router-link :to="{ name: 'CategoryPage', params: { categoryName: 'Metal' } }">
                    <div class="option flex size">
                        <img style="width: 6vw;" src="@/assets/metal.png" alt="Other" />
                    </div>
                </router-link>
                <router-link :to="{ name: 'CategoryPage', params: { categoryName: 'Plastic' } }">
                    <div class="option flex">
                        <img src="@/assets/plastic.png" alt="Plastic" />
                    </div>
                </router-link>
                <router-link :to="{ name: 'CategoryPage', params: { categoryName: 'Glass' } }">
                    <div class="option flex">
                        <img src="@/assets/glass.png" alt="Glass" />
                    </div>
                </router-link>
                <router-link :to="{ name: 'CategoryPage', params: { categoryName: 'Electronic' } }">
                    <div class="option flex">
                        <img src="@/assets/electronic.png" alt="Electronic" />
                    </div>
                </router-link>
             
            </div>
            <!-- Second Row of Categories -->
            <div class="flex" style="gap: 5vw; position: relative; bottom: 5vh;">
                <router-link :to="{ name: 'CategoryPage', params: { categoryName: 'Cardboard' } }">
                    <div class="option flex size">
                        <img src="@/assets/cardboard.png" alt="Cardboard" />
                    </div>
                </router-link>
                <router-link :to="{ name: 'CategoryPage', params: { categoryName: 'Wood' } }">
                    <div class="option flex size">
                        <img src="@/assets/wood.png" alt="Wood" />
                    </div>
                </router-link>
                <router-link :to="{ name: 'CategoryPage', params: { categoryName: 'Furniture' } }">
                    <div class="option flex size">
                        <img src="@/assets/furniture.png" alt="Furniture" />
                    </div>
                </router-link>
                   <router-link :to="{ name: 'CategoryPage', params: { categoryName: 'Textile' } }">
                    <div class="option flex">
                        <img src="@/assets/textile.png" alt="Textile" />
                    </div>
                </router-link>
                
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Categories'
}
</script>

<style scoped>
/* @import 'src/style.css'; */

.categories{
    position: relative;
    top: 12vh;
    width: 90vw;
    left: 5vw;
    height: 40vh;
}

h1{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: lightgreen;
    font-family: "Concert One", serif;
    font-size: 5vw;
}

.select{
    gap: 4vw;
    position: relative;
    top: 5vh;
    flex-direction: column;
    width: 100vw;
  
}

.option {
  width: 10vw;
  height: 20vh;
  border-radius: 50%;
  border: 4px solid rgb(0, 0, 0);
  background-color: rgb(149, 194, 149);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}

.option img {
  width: 4vw;
  height: 13vh;
  transition: filter 0.2s ease;
}

.option:hover {
  transform: scale(1.1);
  background-color: white;
}

.option:hover img {
  filter: brightness(0); /* turns white to black */
  
}


.size img{
    width: 5vw;
    height: 13vh;
}

@media (max-width:430px){
    .option{
        width: 22vw;
        height: 13vh;
       
    }
    .option img{
        width: 8vw;
        height: 8vh;
    }
    .select{
        gap: 15vw;
        /* border: 1px solid black; */
        margin-left: 7vw;
    }
    h1{
        font-size: 10vw;
    }
}
</style>
