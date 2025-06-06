<template>
    <div class="calendar-wrapper">
        <div class="month">{{ selectedMonth }}</div>
        <div class="scroll-container" ref="scrollContainer">
            <div v-for="date in dates" :key="date.toDateString()" :ref="el => assignRef(date, el)"
                :class="['date', isSelected(date) ? 'selected' : isToday(date) ? 'today' : '']"
                @click="$emit('update-date', date)">
                {{ date.getDate() }}
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, defineProps, defineEmits, ComponentPublicInstance } from 'vue'

const props = defineProps<{
    selectedDate: Date
}>()

defineEmits<{
    (e: 'update-date', date: Date): void
}>()

const dates = ref<Date[]>([])

const scrollContainer = ref<HTMLElement | null>(null)
const dateRefs = new Map<string, HTMLElement>()

const assignRef = (date: Date, el: Element | ComponentPublicInstance | null) => {
    if (el instanceof HTMLElement) {
        dateRefs.set(date.toDateString(), el)
    }
}


const generateDates = (centerDate: Date) => {
    const newDates: Date[] = []
    const start = new Date(centerDate)
    start.setDate(centerDate.getDate() - 30)
    for (let i = 0; i <= 60; i++) {
        const d = new Date(start)
        d.setDate(start.getDate() + i)
        newDates.push(new Date(d))
    }
    dates.value = newDates
}

const isSelected = (date: Date) =>
    date.toDateString() === props.selectedDate.toDateString()

const isToday = (date: Date) =>
    date.getYear() === new Date().getYear() &&
    date.getMonth() === new Date().getMonth() &&
    date.getDate() === new Date().getDate()

const scrollToSelectedDate = () => {
    nextTick(() => {
        const selectedEl = dateRefs.get(props.selectedDate.toDateString())
        selectedEl?.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' })
    })
}

watch(() => props.selectedDate, (newDate) => {
    generateDates(newDate)
    scrollToSelectedDate()
}, { immediate: true })

const selectedMonth = computed(() =>
    `${props.selectedDate.getFullYear()}/${props.selectedDate.getMonth() + 1}`
)
</script>

<style scoped>
.calendar-wrapper {
    text-align: center;
    padding: 10px 0px;
    border-bottom: var(--border);
    background-color: var(--dark-backgroud-color);
}

.month {
    font-size: 14px;
    margin-bottom: 5px;
}

.scroll-container {
    display: flex;
    overflow-x: auto;
    padding: 5px 0;
    scrollbar-width: none;
    /* Firefox */
}

.scroll-container::-webkit-scrollbar {
    display: none;
    /* Chrome, Safari, Edge */
}

.date {
    background: transparent;
    color: white;
    padding: 10px 14px;
    border-radius: 10px;
    cursor: pointer;
    white-space: nowrap;
    flex: 0 0 auto;
    font-size: 14px;
    border: 1px solid transparent;
    transition: all 0.2s ease;
    width: 25px;
}

.date.selected {
    background: rgba(255, 255, 255, 0.9);
    color: #1A2B5D;
    font-weight: bold;
    border: 1px solid #ffffff;
    font-size: 16px;
}

.date.today {
    background: rgba(255, 255, 255, 0.15);
}
</style>
