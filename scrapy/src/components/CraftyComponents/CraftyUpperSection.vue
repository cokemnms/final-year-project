<template>
    <div class="quotes">
        <h1>Repurpose</h1>
        <h1>Reinvent</h1>
        <h1>Reimagine</h1>
    </div>
</template>

<script>
    export default{
        name:'CraftyUpperSection'
    }
</script>

<style scoped>
.quotes{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 8vw;
    /* border: 2px solid black; */
    color: lightgreen;
    font-family: "Concert One", serif;
    position: relative;
    top: 5vh;

}
h1{
    font-size: 6vw;
}
</style>