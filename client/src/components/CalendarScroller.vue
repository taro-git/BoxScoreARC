<template>
    <v-card flat class="pa-2 bg-darken">
        <v-row justify="space-between" class="ma-2">
            <v-btn size="small" width="50px" variant="text" @click="$emit('update-date', new Date())">
                Today
            </v-btn>
            <span class="text-h6">{{ selectedMonth }}</span>
            <v-btn size="xlarge" min-width="50px" variant="text" icon @click="dialog = true">
                <v-icon>mdi-calendar</v-icon>
            </v-btn>
        </v-row>

        <v-slide-group show-arrows class="px-2" center-active v-model="selectedDateString">
            <v-slide-group-item v-for="date in dates" :key="date.toDateString()" :value="date.toDateString()">
                <v-chip @click="$emit('update-date', date)" class="ma-1 text-center" pill :style="{
                    minWidth: '3rem',
                    justifyContent: 'center',
                    fontWeight: isSelected(date) ? 'bold' : undefined,
                    fontSize: isSelected(date)
                        ? '1.5rem'
                        : isToday(date)
                            ? '1.2rem'
                            : undefined,
                    border: isSelected(date)
                        ? '2px solid'
                        : isToday(date)
                            ? '1px dashed'
                            : undefined
                }">
                    {{ date.getDate() }}
                </v-chip>
            </v-slide-group-item>
        </v-slide-group>
    </v-card>
    <v-dialog v-model="dialog">
        <v-date-picker v-model="selectedDateString" v-on:update:model-value="dialog = false" />
    </v-dialog>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'

const props = defineProps<{
    selectedDate: Date
}>()

const emit = defineEmits<{
    (e: 'update-date', date: Date): void
}>()

const selectedMonth = computed(() =>
    `${props.selectedDate.getFullYear()}/${props.selectedDate.getMonth() + 1}`
)

const dialog = ref(false)

const dates = ref<Date[]>([])
const generateDates = (centerDate: Date) => {
    const start = new Date(centerDate)
    start.setDate(centerDate.getDate() - 30)
    const newDates: Date[] = []
    for (let i = 0; i <= 60; i++) {
        const d = new Date(start)
        d.setDate(start.getDate() + i)
        newDates.push(new Date(d))
    }
    dates.value = newDates
}
watch(() => props.selectedDate, (newDate) => {
    generateDates(newDate)
}, { immediate: true })
const isSelected = (date: Date) =>
    date.toDateString() === props.selectedDate.toDateString()
const isToday = (date: Date) => {
    const now = new Date()
    return date.getFullYear() === now.getFullYear() &&
        date.getMonth() === now.getMonth() &&
        date.getDate() === now.getDate()
}
const selectedDateString = computed({
    get: () => props.selectedDate.toDateString(),
    set: (val: string) => {
        const date = new Date(val)
        if (!isNaN(date.getTime())) {
            emit('update-date', date)
        }
    }
})
</script>

<style scoped></style>
