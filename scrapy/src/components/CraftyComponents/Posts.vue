<template>
    <div class="mainCont">
        <img src="@/assets/plasticcrafty/plastic1.jpg" alt="" class="post">
        <img src="@/assets/plasticcrafty/plastic2.jpg" alt="" class="post">
        <img src="@/assets/plasticcrafty/plastic1.jpg" alt="" class="post">
        <img src="@/assets/plasticcrafty/plastic2.jpg" alt="" class="post">
        <img src="@/assets/woodencrafty/wood1.jpg" alt="" class="post">
        <img src="@/assets/woodencrafty/wood2.jpg" alt="" class="post">
        <img src="@/assets/woodencrafty/wood1.jpg" alt="" class="post">
        <img src="@/assets/woodencrafty/wood2.jpg" alt="" class="post">
        <img src="@/assets/glasscrafty/glass1.jpg" alt="" class="post">
        <img src="@/assets/glasscrafty/glass2.jpg" alt="" class="post">
        <img src="@/assets/glasscrafty/glass1.jpg" alt="" class="post">
        <img src="@/assets/glasscrafty/glass2.jpg" alt="" class="post">
        <img src="@/assets/metalcrafty/metal1.jpg" alt="" class="post">
        <img src="@/assets/metalcrafty/metal2.jpg" alt="" class="post">
        <img src="@/assets/metalcrafty/metal1.jpg" alt="" class="post">
        <img src="@/assets/metalcrafty/metal2.jpg" alt="" class="post">
       
    </div>

</template>

<script>
    export default{
        name:'Posts'
    }
</script>

<style scoped>
    .mainCont{
        width: 100vw;
        height: 100vh;
        /* border: 2px solid red; */
        position: relative;
        top: 10vh;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        row-gap: 3vw;
        column-gap: 2vw;

    }
    .post{
        width: 22vw;
        height: 32vh;
        /* border: 2px solid green; */
        border-radius: 20px;

    }
</style>