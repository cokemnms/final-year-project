<template>
  <div class="Container flex">
    <div class="loginInfo flex">
      <h1>SCRAPY</h1>
      <p class="text">Log in to your account</p>
      <p class="text">New to Scrapy? <router-link to="/SignUp"><u>Create an account</u></router-link></p>

      <form @submit.prevent="submitForm">
        <div class="loginCreds">
          <input type="email" placeholder="Email" v-model="form.email" />
          <input type="password" placeholder="Password" v-model="form.password" />
          <router-link to="/ForgotPass">Forgot Password?</router-link>
          <button>CONTINUE</button>
        </div>

        <!-- Error message styling -->
        <template v-if="errors.length > 0">
          <div class="error-container flex" :class="{ showError: showError }">
            <p style="font-size: 1.3vw;" v-for="error in errors" :key="error" class="error-message">{{ error }}</p>
          </div>
        </template>
      </form>
    </div>

    <hr class="vertical-hr">

    <div class="loginText flex">
      <p>LOG IN TO UNLOCK</p>
      <p> CREATIVITY AND CONNECT </p>
      WITH THE COMMUNITY 
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

export default {
  setup() {
    const userStore = useUserStore()
    const router = useRouter()

    return {
      userStore,
      router
    }
  },

  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      errors: [],
      showError: false, // Control the error message visibility
    }
  },

  methods: {
    async submitForm() {
      this.errors = [] // Reset the errors
      this.showError = true; // Display error messages immediately

      if (!this.form.email) this.errors.push('Your e-mail is missing')
      if (!this.form.password) this.errors.push('Your password is missing')

      if (this.errors.length === 0) {
        try {
          const loginResponse = await axios.post('/api/login/', this.form)

          const token = loginResponse.data.access
          this.userStore.setToken(loginResponse.data)
          axios.defaults.headers.common["Authorization"] = `Bearer ${token}`

          const userInfoResponse = await axios.get('/api/me/')
          this.userStore.setUserInfo(userInfoResponse.data)

          this.router.push({ path: '/MainPage' })
        } catch (error) {
          this.errors.push('Login failed. Please check your credentials.')
          console.error('Login error:', error.response || error)
        }
      }

      // Hide the error messages after 7 seconds
      if (this.errors.length > 0) {
        setTimeout(() => {
          this.showError = false;
        }, 7000);
      }
    }
  }
}
</script>

<style scoped>
.Container {
  width: 100vw;
  height: 100vh;
  gap: 10vw;
}

.loginInfo {
  width: 45vw;
  height: 99vh;
  flex-direction: column;
}

.loginText {
  width: 55vw;
  height: 99vh;
  font-family: "Concert One", serif;
  color: lightgreen;
  font-size: 4vw;
  flex-direction: column;
  text-align: left;
  align-items: start;
  position: relative;
  right: 5vw;
}

.loginCreds {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2vh;
  flex-direction: column;
}

a button {
  color: black;
}

.loginInfo input {
  width: 22vw;
  height: 7vh;
  border: 1px solid grey;
  border-radius: 10px;
  padding: 10px;
  position: relative;
  bottom: 3vh;
}

.vertical-hr {
  width: 1px;
  height: 90vh;
  background-color: rgb(228, 228, 228);
  border: none;
  margin: 0;
}

.loginInfo button {
  width: 10vw;
  height: 8vh;
  border: 3px solid black;
  border-radius: 40px;
  cursor: pointer;
  transition: transform 0.2s;
  background-color: #8db161;
  color: white;
  font-family: "Concert One", serif;
  font-size: 1.5vw;
}

.loginInfo button:hover {
  transform: scale(1.05);
  background-color: lightgreen;
  color: white;
}

.loginInfo h1 {
  position: relative;
  color: lightgreen;
  font-family: "Concert One", serif;
  bottom: 5vh;
  font-size: 7vw;
}

.text {
  position: relative;
  bottom: 8vh;
}

/* Error message styling */
.error-container {
  position: absolute;
  top: 20px; /* Position the error message near the top */
  left: 50%; /* Center horizontally */
  transform: translateX(-50%); /* Adjust the positioning to exactly center */
  padding: 15px;
  background-color: #f8d7da;
  border-radius: 5px;
  z-index: 999;
  opacity: 0; /* Initially hidden */
  animation: fadeInOut 7s ease-in-out forwards;
  width: 30vw;
  flex-direction: column;
}

/* Apply showError class when error is visible */
.error-container.showError {
  opacity: 1;
}

.error-message {
  color: #721c24;
  font-size: 1.1rem;
  margin: 5px 0;
  font-weight: 600;
}

/* Keyframes for fade-in and fade-out */
@keyframes fadeInOut {
  0% {
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>
