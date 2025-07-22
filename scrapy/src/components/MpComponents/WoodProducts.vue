<template>
    <div>
      <h1>Wood</h1>
      <category-products 
        :items="wood" 
        @update-favorite="updateFavorite" 
      />
    </div>
  </template>
  
  <script>
  import CategoryProducts from "./CategoryProducts.vue";
  
  export default {
    components: { CategoryProducts },
    data: () => ({
      wood: [
        {
          name: "Smartphone",
          image: "src/assets/woodimages/wood1.jpg",
          price: 299.99,
          timeAgo: "2 hours",
          rating: 4.5,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/woodimages/wood2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/woodimages/wood1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/woodimages/wood2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/woodimages/wood1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/woodimages/wood2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/woodimages/wood1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/woodimages/wood2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/woodimages/wood1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/woodimages/wood2.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/woodimages/wood1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
      ],
    }),
    methods: {
      updateFavorite(index) {
        this.wood[index].isFavorite = !this.wood[index].isFavorite;
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
        font-family: "Concert One", serif;
        font-size: 3.5vw;
    }
</style>
  