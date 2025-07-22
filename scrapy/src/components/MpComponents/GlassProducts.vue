<template>
    <div class="glass">
      <h1>Glass</h1>
      <category-products 
        :items="glass" 
        @update-favorite="updateFavorite" 
      />
    </div>
  </template>
  
  <script>
  import CategoryProducts from "./CategoryProducts.vue";
  
  export default {
    components: { CategoryProducts },
    data: () => ({
      glass: [
        {
          name: "Smartphone",
          image: "src/assets/glassimages/glass1.webp",
          price: 299.99,
          timeAgo: "2 hours",
          rating: 4.5,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/glassimages/glass2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/glassimages/glass1.webp",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/glassimages/glass2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/glassimages/glass1.webp",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/glassimages/glass2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/glassimages/glass1.webp",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/glassimages/glass2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/glassimages/glass1.webp",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/glassimages/glass2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/glassimages/glass1.webp",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
      ],
    }),
    methods: {
      updateFavorite(index) {
        this.glass[index].isFavorite = !this.glass[index].isFavorite;
      },
    },
  };
  </script>

  <style scoped>
    h1{
        position: relative;
        top: 30vh;
        left: 5vw;
        color:lightgreen;
        font-size: 3.5vw;
        font-family: "Concert One", serif;
    }
    .glass{
        position: relative;
        bottom: 140vh;
        
    }
</style>
  