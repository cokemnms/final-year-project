<template>
    <div class="metal">
      <h1>Metal</h1>
      <category-products 
        :items="metal" 
        @update-favorite="updateFavorite" 
      />
    </div>
  </template>
  
  <script>
  import CategoryProducts from "./CategoryProducts.vue";
  
  export default {
    components: { CategoryProducts },
    data: () => ({
      metal: [
        {
          name: "Smartphone",
          image: "src/assets/metalimages/metal1.jpg",
          price: 299.99,
          timeAgo: "2 hours",
          rating: 4.5,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/metalimages/metal2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/metalimages/metal1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/metalimages/metal2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/metalimages/metal1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/metalimages/metal2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/metalimages/metal1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/metalimages/metal2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/metalimages/metal1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/metalimages/metal2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/metalimages/metal1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
      ],
    }),
    methods: {
      updateFavorite(index) {
        this.metal[index].isFavorite = !this.metal[index].isFavorite;
      },
    },
  };
  </script>

  <style scoped>
    h1{
        position: relative;
        top: 45vh;
        left: 5vw;
        color:white;
        font-size: 3.5vw;
        font-family: "Concert One", serif;
    }
    .metal{
        position: relative;
        bottom: 30vh;
    }
</style>
  