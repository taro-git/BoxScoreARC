<template>
    <v-app class="bg-base">
        <v-app-bar color="base" :elevation="2">
            <template v-slot:prepend>
                <v-app-bar-nav-icon @click.stop="open = !open"></v-app-bar-nav-icon>
            </template>
            <img v-if="selectedItemRouteName === ROUTE_NAMES.GAME" class="mr-5" :style="{ 'width': '2.5rem' }"
                :src="gameSummary.awayTeam.logo" />
            <span v-if="selectedItemRouteName === ROUTE_NAMES.GAME" class="text-h5">
                {{ gameSummary.awayScore }} - {{ gameSummary.homeScore }}
            </span>
            <img v-if="selectedItemRouteName === ROUTE_NAMES.GAME" class="ml-5" :style="{ 'width': '2.5rem' }"
                :src="gameSummary.homeTeam.logo" />
            <v-app-bar-title v-else>{{ selectedItemTitle }}</v-app-bar-title>
            <template v-slot:append>
                <v-btn icon @click="dialog = true">
                    <v-icon>mdi-dots-vertical</v-icon>
                </v-btn>
            </template>
        </v-app-bar>

        <v-navigation-drawer class="bg-lighten" v-model="open" :location="'top'">
            <v-list v-model:selected="selectedItemRouteName" mandatory>
                <v-list-item v-for="item in items" :key="item.routeName" :value="item.routeName"
                    @click="navigationClick(item.routeName)">
                    <template #prepend>
                        <v-icon>{{ item.prependIcon }}</v-icon>
                    </template>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

        <v-dialog v-model="dialog">
            <v-card>
                <v-card-title class="text-center">Settings</v-card-title>
                <v-card-text>
                    <Settings />
                </v-card-text>
                <v-card-actions>
                    <v-btn color="primary" @click="dialog = false">Close</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-main>
            <router-view />
        </v-main>
    </v-app>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted } from 'vue'
import { useTheme } from 'vuetify'
import { useRouter, useRoute } from 'vue-router'

import Settings from './components/Settings.vue'
import { baseToAccent, baseToDarken, baseToLighten, type RgbaColor } from './core/colorControl'
import { ROUTE_NAMES } from './router'
import { gameStore } from './store/game'
import { settingsStore } from './store/settings'

const open = ref(false)
const gameSummary = gameStore().gameSummary
const appBarTitles = computed(() => {
    return {
        [ROUTE_NAMES.HOME]: 'Home',
        [ROUTE_NAMES.GAMES]: 'Games',
        [ROUTE_NAMES.GAME]: '',
        [ROUTE_NAMES.ANALYSIS]: 'Analysis',
    }
})
const items = [
    {
        title: appBarTitles.value[ROUTE_NAMES.HOME],
        routeName: ROUTE_NAMES.HOME,
        prependIcon: 'mdi-view-dashboard',
    },
    {
        title: appBarTitles.value[ROUTE_NAMES.GAMES],
        routeName: ROUTE_NAMES.GAMES,
        prependIcon: 'mdi-basketball',
    },
    {
        title: appBarTitles.value[ROUTE_NAMES.ANALYSIS],
        routeName: ROUTE_NAMES.ANALYSIS,
        prependIcon: 'mdi-chart-bar',
    },
]
const router = useRouter()
const navigationClick = (routeName: string) => {
    open.value = false
    router.push({ name: routeName })
}
const route = useRoute()
const selectedItemRouteName = computed(() => route.fullPath.split('/')[1])
const selectedItemTitle = computed(() => appBarTitles.value[selectedItemRouteName.value] ?? 'Invalid Path')

const dialog = ref(false)
const settings = settingsStore()

const vuetifyTheme = useTheme()
const setThemeColor = (color: RgbaColor) => {
    vuetifyTheme.themes.value.myCustomTheme.colors.base = color
    vuetifyTheme.themes.value.myCustomTheme.colors.darken = baseToDarken(color)
    vuetifyTheme.themes.value.myCustomTheme.colors.lighten = baseToLighten(color)
    vuetifyTheme.themes.value.myCustomTheme.colors.accent = baseToAccent(color)
}
onMounted(() => {
    setThemeColor(settings.themeColor)
})
watch(
    () => settings.themeColor,
    (newColor) => {
        setThemeColor(newColor)
    },
    { deep: true }
)
</script>

<style scoped></style>
