<template>
    <Navbar/>
    <MainText />
    <Categories />
    <MpProducts />
    <!-- <WoodProducts />
    <MetalProducts /> -->
    <!-- <PlasticProducts /> -->
    <!-- <GlassProducts /> -->
  <Footer/>
  </template>
  
  <script>
import Navbar from "@/layouts/Navbar.vue";

  import Categories from '@/components/MpComponents/Categories.vue';
  import MpProducts from '@/components/MpComponents/MpProducts.vue';
  import WoodProducts from '@/components/MpComponents/WoodProducts.vue';
  import MetalProducts from '@/components/MpComponents/MetalProducts.vue';
  import PlasticProducts from '@/components/MpComponents/PlasticProducts.vue';
  import GlassProducts from '@/components/MpComponents/GlassProducts.vue';
  import MainText from '@/components/MpComponents/MainText.vue';
  import Footer from '@/layouts/Footer.vue'
  
  export default {
    name: 'MainPage',
    components: {
      Navbar,
      Categories,
      MpProducts,
      WoodProducts,
      MetalProducts,
      PlasticProducts,
      GlassProducts,
      MainText,
      Footer
  
    },
    mounted() {
      (function () {
        if (!window.chatbase || window.chatbase("getState") !== "initialized") {
          window.chatbase = (...args) => {
            if (!window.chatbase.q) window.chatbase.q = [];
            window.chatbase.q.push(args);
          };
          window.chatbase = new Proxy(window.chatbase, {
            get(target, prop) {
              if (prop === "q") return target.q;
              return (...args) => target(prop, ...args);
            },
          });
        }
  
        const onLoad = function () {
          const script = document.createElement("script");
          script.src = "https://www.chatbase.co/embed.min.js";
          script.id = "H5ZKp6Nt6vUkJR2h3HGnW";
          script.setAttribute("domain", "www.chatbase.co");
          document.body.appendChild(script);
        };
  
        if (document.readyState === "complete") {
          onLoad();
        } else {
          window.addEventListener("load", onLoad);
        }
      })();
    }
  };
  </script>
