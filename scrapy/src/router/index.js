import { createRouter, createWebHistory } from "vue-router";
import home from "@/views/home.vue";
import AboutUs from "@/pages/AboutUs.vue";
import Saved from "@/pages/Saved.vue";
import Chat from "@/pages/Chat.vue";
import Crafty from "@/pages/Crafty.vue";
import ForgotPass from "@/pages/ForgotPass.vue";
import Login from "@/pages/Login.vue";
import ProductDetails from "@/pages/ProductDetails.vue";
import Sell from "@/pages/Sell.vue";
import SignUp from "@/pages/SignUp.vue";
import UserProfile from "@/pages/UserProfile.vue";
import App from "@/App.vue";
import MainPage from "@/pages/MainPage.vue";
import CategoryPage from "@/pages/CategoryPage.vue";
import DisplayCategories from "@/pages/DisplayCategories.vue";
import PostView from "@/pages/PostView.vue";
import Recommendations from "@/pages/Recommendations.vue";
import EditProfile from "@/pages/EditProfile.vue";
import MyListings from "@/pages/MyListings.vue";
import Notifications from "@/pages/Notifications.vue";
import Search from "@/pages/Search.vue";
import AuctionCreate from "@/pages/AuctionCreate.vue";
import AuctionDetails from "@/pages/AuctionDetails.vue";
import AuctionList from "@/pages/AuctionList.vue";
import OthersCrafty from "@/pages/OthersCrafty.vue";
import InitialAuction from "@/pages/InitialAuction.vue";
import OtherScrap from "@/pages/OtherScrap.vue"
import OtherAuctions from "@/pages/OtherAuctions.vue"
import ResetPassword from '@/pages/ResetPassword.vue'
const routes = [
  { path: "/MainPage", name: "MainPage", component: MainPage },
  { path: "/", name: "home", component: home },
  { path: "/Saved", name: "Saved", component: Saved },
  { path: "/AboutUs", name: "AboutUs", component: AboutUs },
  { path: "/chat", name: "chat", component: Chat },
  { path: "/Sell", name: "Sell", component: Sell },
  { path: "/Crafty", name: "Crafty", component: Crafty },
  { path: "/ForgotPass", name: "ForgotPass", component: ForgotPass },
  { path: "/Login", name: "Login", component: Login },
  { path: "/UserProfile/:id", name: "UserProfile", component: UserProfile },
  { path: "/SignUp", name: "SignUp", component: SignUp },
  {
    path: "/ProductDetails/:id",
    name: "ProductDetails",
    component: ProductDetails,
  },{
  path: "/scrap-posts/:id",
  name: "ScrapPostDetails",
  component: ProductDetails
},
  { path: "/App", name: "App", component: App },
{
  path: '/category/:categoryName',
  name: 'CategoryPage',
  component: CategoryPage
},
  {
    path: "/DisplayCategories",
    name: "DisplayCategories",
    component: DisplayCategories,
  },

  {
    path: "/recommendations",
    name: "recommendations",
    component: Recommendations,
  },
  {
    path: "/MyListings",
    name: "MyListings",
    component: MyListings,
  },
  {
    path: "/Notifications",
    name: "Notifications",
    component: Notifications,
  },
  {
    path: "/Search",
    name: "Search",
    component: Search,
  },
 {
  path: '/auctions',
  name: 'AuctionList',
  component: AuctionList
},
{
  path: '/auctions/create',
  name: 'AuctionCreate',
  component: AuctionCreate
},
{
  path: '/auctions/:id',
  name: 'AuctionDetail',
  component: AuctionDetails
},
  {
    path: '/OthersCrafty/:id',
    name: 'OthersCrafty',
    component:OthersCrafty 
  },
  {
    path: '/InitialAuction',
    name: 'InitialAuction',
    component:InitialAuction
  },
  {
    path: '/OthersCrafty/:id',
    name: 'OthersCrafty',
    component:OthersCrafty 
  },
  {
    path: '/OtherScrap/:id',
    name: 'OtherScrap',
    component:OtherScrap 
  },
  {
     path: '/profile/:id/auctions',
  name: 'OtherAuctions',
  component: OtherAuctions
  },
  { path: "/editProfile", name: "editProfile", component: EditProfile },
     {
    path: '/reset-password/:uid/:token',
    name: 'ResetPassword',
    component: ResetPassword
  },
  { path: "/:id", name: "PostView", component: PostView },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
   
    return { top: 0 };
  },
});

export default router;
