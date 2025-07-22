import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user',{
   
    state: () => ({
        user: {
            isAuthenticated: false,
            id: null,
            firstName: null,
            lastName: null,
            email: null,
            number: null,
            city:null,
            access: null,
            refresh: null,
        }
    }),

    actions: {
        initStore() {
            console.log('initStore', localStorage.getItem('user.access'))

            if (localStorage.getItem('user.access')) {
                console.log('User has access!')

                this.user.access = localStorage.getItem('user.access')
                this.user.refresh = localStorage.getItem('user.refresh')
                this.user.id = localStorage.getItem('user.id')
                this.user.firstName = localStorage.getItem('user.nfirstNme')
                this.user.lastName = localStorage.getItem('user.lastName')
                this.user.email = localStorage.getItem('user.email')
                this.user.number = localStorage.getItem('user.number')
                this.user.city = localStorage.getItem('user.city')
                this.user.isAuthenticated = true

                this.refreshToken()

                console.log('Initialized user:', this.user)
            }
        },

        setToken(data) {
            console.log('setToken', data)

            this.user.access = data.access
            this.user.refresh = data.refresh
            this.user.isAuthenticated = true

            localStorage.setItem('user.access', data.access)
            localStorage.setItem('user.refresh', data.refresh)

            console.log('user.access: ', localStorage.getItem('user.access'))
        },

        removeToken() {
            console.log('removeToken')

            this.user.refresh = null
            this.user.access = null
            this.user.isAuthenticated = false
            this.user.id = false
            this.user.firstName = false
            this.user.lastName = false
            this.user.email = false
            this.user.city = false
            this.user.number = false

            localStorage.setItem('user.access', '')
            localStorage.setItem('user.refresh', '')
            localStorage.setItem('user.id', '')
            localStorage.setItem('user.firstName', '')
            localStorage.setItem('user.lastName', '')
            localStorage.setItem('user.email', '')
            localStorage.setItem('user.city', '')
            localStorage.setItem('user.number', '')
        },

        setUserInfo(user) {
            console.log('setUserInfo', user)

            this.user.id = user.id
            this.user.firstName = user.firstName
            this.user.lastName = user.lastName
            this.user.email = user.email
            this.user.city = user.city

            localStorage.setItem('user.id', this.user.id)
            localStorage.setItem('user.firstName', this.user.firstName)
            localStorage.setItem('user.lastName', this.user.lastName)
            localStorage.setItem('user.email', this.user.email)
            localStorage.setItem('user.number', this.user.number)
            localStorage.setItem('user.city', this.user.city)

            console.log('User', this.user)
        },
        logout() {
            this.user = {
              isAuthenticated: false,
              id: null,
              firstName: null,
              lastName: null,
              email: null,
              number: null,
              access: null,
              city: null,
              refresh: null
            }
          
            localStorage.removeItem('user.access')
            localStorage.removeItem('user.refresh')
          }
          ,

        refreshToken() {
            axios.post('/api/refresh/', {
                refresh: this.user.refresh
            })
                .then((response) => {
                    this.user.access = response.data.access

                    localStorage.setItem('user.access', response.data.access)

                    axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access
                })
                .catch((error)=>{
                    console.log(error)

                    this.removeToken()
                })
        },
    }
})