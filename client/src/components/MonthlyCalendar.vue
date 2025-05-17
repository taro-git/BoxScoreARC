<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="calendar-popup">
      <VueDatePicker
        v-model="internalDate"
        :locale="'ja'"
        :enable-time-picker="false"
        :auto-apply="true"
        inline
        @update:model-value="onSelect"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, defineEmits, defineProps } from 'vue'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

const props = defineProps<{
  selectedDate: Date
}>()

const emit = defineEmits(['select', 'close'])

const internalDate = ref<Date>(props.selectedDate)

watch(() => props.selectedDate, (newVal) => {
  internalDate.value = newVal
})

const onSelect = (date: Date) => {
  emit('select', date)
  emit('close') // 選択後に閉じる
}
</script>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.calendar-popup {
  background-color: #fff;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(25, 118, 210, 0.9);
}
</style>
