<template>
  <Navbar />
  <div class="auction-heading">
    <h1>LIST WITH CONFIDENCE</h1>
    <h1 style="color: #a5ce9d;">SELL WITH SUCCESS</h1>
  </div>

  <div class="auction flex">
    <div class="create-auction flex">
      <h1 class="heading">CREATE AUCTION</h1>
      <form @submit.prevent="submitForm" class="form flex">
        <input v-model="form.title" placeholder="Title" class="input" />
        <textarea v-model="form.description" placeholder="Description" class="textarea"></textarea>
        <input type="datetime-local" v-model="form.expires_at" class="input" />
        <input type="number" v-model="form.base_price" placeholder="Base Price" class="input" />

        <!-- Image Upload -->
        <div class="image-upload flex" style="position: relative; right: 3vw;">
          <h2>UPLOAD IMAGES</h2>
          <input
            type="file"
            id="file-upload"
            @change="handleFile"
            accept="image/*"
            style="display: none"
            multiple
          />
          <label for="file-upload" class="cursor-pointer">
            <img
              width="50"
              height="50"
              src="https://img.icons8.com/ios-filled/50/ffffff/image.png"
              alt="upload-icon"
              style="width: 2vw; height: 5vh"
            />
          </label>
        </div>

        <button type="submit" class="button">SUBMIT</button>

        <!-- Image Previews -->
        <div class="image-preview-container">
          <div v-for="(image, index) in imagePreviews" :key="index" class="image-preview">
            <img :src="image" class="preview-img" />
            <button class="remove-btn" @click.prevent="removeImage(index)">✕</button>
          </div>
        </div>
      </form>
    </div>
    <img src="@/assets/auction-create.png" alt="">
  </div>
  <Footer/>
</template>

<script>
import Navbar from '@/layouts/Navbar.vue'
import Footer from '@/layouts/Footer.vue'
import axios from 'axios'


export default {
  name: 'AuctionCreate',
  components: {
    Navbar,
    Footer
  },
  data() {
    return {
      form: {
        title: '',
        description: '',
        base_price: '',
        expires_at: '',
        max_price: '',
        images: []
      },
      imagePreviews: []
    }
  },
  methods: {
    handleFile(e) {
      const files = Array.from(e.target.files)
      this.form.images.push(...files)

      // Add previews
      files.forEach((file) => {
        const reader = new FileReader()
        reader.onload = (e) => this.imagePreviews.push(e.target.result)
        reader.readAsDataURL(file)
      })
    },
    removeImage(index) {
      this.form.images.splice(index, 1)
      this.imagePreviews.splice(index, 1)
    },
    submitForm() {
      if (!this.form.title || !this.form.description || !this.form.base_price) {
        alert('Please fill in all required fields including title, description, and base price.')
        return
      }

      const formData = new FormData()
      formData.append('title', this.form.title)
      formData.append('description', this.form.description)
      formData.append('base_price', this.form.base_price)

      if (this.form.expires_at) {
        const localDate = new Date(this.form.expires_at)
        formData.append('expires_at', localDate.toISOString())
      }

      this.form.images.forEach((image) => {
        formData.append('images', image)
      })

      axios
        .post('/api/auctions/create/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('user.access')}`
          }
        })
        .then(() => this.$router.push('/auctions'))
        .catch((err) => console.error(err))
    }
  }
}
</script>

<style scoped>
.create-auction {
  padding: 20px;
  width: 40vw;
  flex-direction: column;
  gap: 2vh;
  border: 3px solid black;
  border-radius: 30px;
  background-color: #a5ce9d;
  position: relative;
  left: 8vw;
}

.create-auction h1 {
  font-family: "Concert One", serif;
  font-size: 4vw;
  color: white;
}

.heading {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 16px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 2vh;
}

.input,
.textarea {
  padding: 10px;
  border-radius: 20px;
  width: 30vw;
  border: 1px solid black;
  outline: none;
}

.textarea {
  height: 20vh;
  background-color: white;
}

.button {
  background-color: #ffffff;
  color: rgb(93, 131, 96);
  padding: 10px 20px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  border: 3px solid black;
  font-family: "Concert One", serif;
  transition: transform .2s;
}

.button:hover {
  background-color: black;
  color: white;
  transform: scale(1.1);
}

.auction img {
  width: 60vw;
  height: 70vh;
  position: relative;
  left: 5vw;
}

.auction-heading {
  margin-top: 4vh;
  margin-bottom: 10vh;
  width: 100vw;
  text-align: center;
  font-size: 6vw;
  font-family: "Concert One", serif;
}

input {
  background-color: white;
}

.auction {
  margin-bottom: 10vh;
}

h2 {
  font-size: 3vw;
  color: white;
  font-family: "Concert One", serif;
}

.image-preview-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1vw;
  margin-top: 2vh;
  /* border: 1px solid red; */
}

.image-preview {
  position: relative;
  /* border: 2px solid black; */
  display: flex;
  justify-content: center;
  align-items: center;
   position: relative !important;
  right: 5vw !important;
}

.preview-img {
  width: 10vw !important;
  height: 20vh !important;
  object-fit: cover;
  border-radius: 8px;
  /* border: 2px solid black; */
 
}

.remove-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: red;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  width: 20px;
  height: 20px;
  font-size: 12px;
}
</style>
