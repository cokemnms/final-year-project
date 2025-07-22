<template>
   <router-link to="/Login"><h1>SCRAPY</h1></router-link>
  <div class="forgetPassCont">
  <div class="form flex" style="flex-direction: column;">
    <h2 class="resetHead">RESET PASSWORD</h2>
    <input class="resetInput" type="password" v-model="password" placeholder="Enter new password" />
    <button class="resetBtn" @click="resetPassword">RESET</button>
    <p v-if="message">{{ message }}</p>
  </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      password: '',
      message: ''
    }
  },
  methods: {
async resetPassword() {
  try {
    const { uid, token } = this.$route.params;
    const res = await axios.post(
      `http://localhost:8000/api/reset-password/${uid}/${token}/`,
      { password: this.password },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': ''  // ✅ Override any default token
        }
      }
    );
    this.message = res.data.message;
  } catch (err) {
    this.message = err.response?.data?.error || 'Something went wrong';
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

  .resetHead {
    font-size: 3vw;
  font-family: "Concert One", serif;

  }

  .resetInput{
      width: 20vw;
      border: 3px solid black;
      border-radius: 30px;
      height: 7vh;
      padding: 10px;
  }
  .resetBtn{
    width: 6vw;
    height: 5vh;
    border: 3px solid black;
    color: white;
    background-color: #8db161;
    margin-top: 2vh;
    border-radius: 30px;
  }
</style>