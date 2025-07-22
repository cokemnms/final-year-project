<template>
    <div class="plastic">
      <h1>Plastic</h1>
      <category-products 
        :items="plastic" 
        @update-favorite="updateFavorite" 
      />
    </div>
  </template>
  
  <script>
  import CategoryProducts from "./CategoryProducts.vue";
  
  export default {
    components: { CategoryProducts },
    data: () => ({
      plastic: [
        {
          name: "Smartphone",
          image: "src/assets/plasticimages/plastic1.jpg",
          price: 299.99,
          timeAgo: "2 hours",
          rating: 4.5,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/plasticimages/plastic2.jpeg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/plasticimages/plastic1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/plasticimages/plastic2.jpeg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/plasticimages/plastic1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/plasticimages/plastic2.jpeg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/plasticimages/plastic1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/plasticimages/plastic2.jpeg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/plasticimages/plastic1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/plasticimages/plastic2.jpeg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
        {
          name: "Laptop",
          image: "src/assets/plasticimages/plastic1.jpg",
          price: 899.99,
          timeAgo: "1 day",
          rating: 4.8,
          isFavorite: true,
        },
      ],
    }),
    methods: {
      updateFavorite(index) {
        this.plastic[index].isFavorite = !this.plastic[index].isFavorite;
      },
    },
  };
  </script>

  <style scoped>
    h1{
        position: relative;
        top: 45vh;
        left: 5vw;
        color:lightgreen;
        font-size: 3.5vw;
        font-family: "Concert One", serif;
    }
    .plastic{
        position: relative;
        bottom: 90vh;
    }
</style>
  