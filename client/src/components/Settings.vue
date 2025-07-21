<template>
    <v-container>
        <v-row>
            <v-col class="d-flex align-center">
                Theme Color
            </v-col>
            <v-col class="d-flex align-center">
                <v-btn @click="colorPicker = true">Open Color Palette</v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-col class="d-flex align-center">
                Display Score
            </v-col>
            <v-col class="d-flex align-center">
                <v-switch v-model="settings.scoreDisplay" color="primary" hide-details inset />
            </v-col>
        </v-row>
        <v-row>
            <v-col class="d-flex align-center">
                Default Range of Quarter
            </v-col>
            <v-col class="d-flex align-center">
                <v-select v-model="settings.defaultQuarterRangeType" :items="quarterRangeLabels" />
            </v-col>
        </v-row>
    </v-container>
    <v-dialog v-model="colorPicker">
        <v-color-picker v-model="themeColorModel" />
    </v-dialog>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

import { DEFAULT_THEME_COLOR_BASE } from '../vuetify'
import { isValidRgbaColor } from '../core/colorControl'
import { settingsStore } from '../store/settings'
import { quarterRangeLabels } from '../types/QuarterRangeVariations'

const colorPicker = ref(false)

const settings = settingsStore()
const themeColorModel = computed({
    get: () => settings.themeColor,
    set: (val: string) => {
        settings.themeColor = isValidRgbaColor(val) ? val : DEFAULT_THEME_COLOR_BASE
    }
})

</script>

<style scoped></style>
