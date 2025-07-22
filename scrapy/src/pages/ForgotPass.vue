<template>
  <h1>SCRAPY</h1>
  <div class="forgetPassCont">

    <img src="@/assets/forgotpassword.png" alt="">
  <div class="form flex" style="flex-direction: column;">
    <h2 class="forgetHead">FORGOT PASSWORD</h2>
    <input class="forgetInput" type="email" v-model="email" placeholder="Enter your email" />
    <button class="forgetBtn" @click="submitEmail">Send Reset Link</button>
    <p v-if="message">{{ message }}</p>
  </div>

    </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ForgetPass',
  data() {
    return {
      email: '',
      message: '',
      error: '',
      loading: false
    }
  },
  methods: {
    async submitEmail() {
  try {
    const res = await axios.post('http://localhost:8000/api/request-password-reset/', {
      email: this.email
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': '' // ✅ clears any default token
      }
    })
    this.message = res.data.message
  } catch (err) {
    this.message = err.response?.data?.error || 'Something went wrong'
  }
}

  }
}

</script>

<style scoped>
  .forgetPassCont{
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5vw;
  }
  h1{
    font-size: 5vw;
  font-family: "Concert One", serif;
  color: #8db161;
  margin-left: 3vw;


  }
  .forgetPassCont img{
    width: 40vw;
  }

  .forgetHead {
    font-size: 3vw;
  font-family: "Concert One", serif;

  }

  .forgetInput{
      width: 20vw;
      border: 3px solid black;
      border-radius: 30px;
      height: 7vh;
      padding: 10px;
  }
  .forgetBtn{
    width: 6vw;
    height: 5vh;
    border: 3px solid black;
    color: white;
    background-color: #8db161;
    margin-top: 2vh;
    border-radius: 30px;
  }
</style>