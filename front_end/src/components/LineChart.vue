<template>
  <div>
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
} from 'chart.js'
import { Line } from 'vue-chartjs'
import { computed } from 'vue'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  label: {
    type: String,
    default: 'SOL Price',
  }
})

const chartData = computed(() => ({
  labels: props.data.map(item => item.date),
  datasets: [
    {
      label: props.label,
      data: props.data.map(item => item.price),
      fill: false,
      borderColor: '#16a34a',
      tension: 0.3,
      pointRadius: 3,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  plugins: {
    legend: {
      display: false,
      position: 'top',
    },
  },
  scales: {
    x: {
      ticks: {
        maxTicksLimit: 10,
        autoSkip: true,
      },
    },
    y: {
      beginAtZero: false,
    },
  },
}
</script>
