<!-- Item.vue -->
<template>
  <div class="item" :class="{ selected: props.isSelected }" @click="handleClick">
    <img :src="img" :alt="name" />
    <p style="font-size: 20px">{{ name }}</p>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue'
const props = defineProps(['name', 'img', 'trading_key', 'isSelected'])
const emit = defineEmits(['select'])

function handleClick() {
  emit('select', props.trading_key.toUpperCase())
}
</script>

<style scoped>
.item {
  cursor: pointer;
  text-align: center;
}
.item img {
  width: 50px;
  height: 50px;
}
.item.selected {
  border: 2px solid #065f46;
  border-radius: 8px;
  background-color: #f0fdf4;
  box-shadow: 0 0 8px rgba(6, 95, 70, 0.4);
  transform: scale(1.05);
  transition: all 0.2s ease-in-out;
}

</style>
