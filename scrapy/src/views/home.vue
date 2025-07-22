<template>
    <div class="wrapper">
      <div class="home">
        <div class="title">
          <h1>SCRAPY</h1>
          <h2 style="position: relative; bottom: 3vh;">BUY SELL CREATE</h2>
        </div>
        <div class="button">
          <router-link to="/Login"><button>LOGIN</button></router-link>
          <router-link to="/SignUp"><button>SIGN UP</button></router-link>
        </div>
      </div>
      <img src="@/assets/platform.gif" alt="Platform" />
      <Toast />
    </div>
  </template>
  
  <script>
  import Toast from '@/components/Toast.vue'
  import axios from 'axios'
  import { useUserStore } from '@/stores/user'
  
  export default {
    components: { Toast },
    setup() {
      const userStore = useUserStore()
      return { userStore }
    },
    beforeCreate() {
      this.userStore.initStore()
      const token = this.userStore.user.access
      axios.defaults.headers.common["Authorization"] = token ? `Bearer ${token}` : ""
    }
  }
  </script>
  
  <style scoped>
  .wrapper {
    width: 100vw;
    height: 100vh;
    background-color: rgb(142, 197, 142);
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5vw;
  }
  .title {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  .button,
  .home {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .home {
    flex-direction: column;
    gap: 2vw;
    position: relative;
    bottom: 5vh;
  }
  .button {
    gap: 2vw;
  }
  button {
    width: 10vw;
    height: 8vh;
    border: 3px solid black;
    color: white;
    font-size: 1.6vw;
    border-radius: 40px;
    background-color: #8db161;
    font-family: "Concert One", serif;
    transition: transform 0.25s;
  }
  button:hover {
    background-color: white;
    color: rgb(132, 199, 124);
    transform: scale(1.1);
  }
  h1 {
    font-size: 10vw;
    color: rgb(81, 133, 84);
    font-family: "Concert One", serif;
  }
  h2 {
    font-size: 4vw;
    color: white;
    font-family: "Concert One", serif;
  }
  .wrapper img {
    width: 40vw;
    height: 80vh;
    position: relative;
    bottom: 5vh;
  }
  </style>
  