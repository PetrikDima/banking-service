<template>
  <div class="item">
    <img :src="img" alt="" />
    <p>{{ name }}</p>
  </div>
</template>

<script setup>
defineProps(['name', 'img'])
</script>

<style scoped>
.item {
  text-align: center;
}
.item img {
  width: 60px;
  height: 60px;
  object-fit: contain;
}
.item p {
  margin-top: 8px;
  font-weight: bold;
}
</style>
