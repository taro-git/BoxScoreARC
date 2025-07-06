<template>
    <label class="switch" :style="switchStyle">
        <input type="checkbox" :checked="modelValue" @change="$emit('update:modelValue', $event.target.checked)" />
        <span class="slider"></span>
    </label>
</template>

<script setup>
import { computed, defineEmits, defineProps } from 'vue'

const props = defineProps({
    modelValue: {
        type: Boolean,
        required: true,
    },
    size: {
        type: Number,
        default: 40,
    },
})

defineEmits(['update:modelValue'])

const switchStyle = computed(() => {
    const width = props.size
    const height = props.size / 2
    const circle = height - 6
    return {
        '--switch-width': `${width}px`,
        '--switch-height': `${height}px`,
        '--circle-size': `${circle}px`,
        '--circle-translate': `${width - height}px`,
    }
})
</script>

<style scoped>
.switch {
    position: relative;
    display: inline-block;
    width: var(--switch-width);
    height: var(--switch-height);
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #ccc;
    border-radius: 100px;
    transition: background-color 0.3s;
}

.slider::before {
    content: "";
    position: absolute;
    height: var(--circle-size);
    width: var(--circle-size);
    left: 3px;
    top: 3px;
    background-color: white;
    border-radius: 50%;
    transition: transform 0.3s;
}

input:checked+.slider {
    background-color: #4caf50;
}

input:checked+.slider::before {
    transform: translateX(var(--circle-translate));
}
</style>
