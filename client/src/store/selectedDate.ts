import { defineStore } from 'pinia'


export const selectedDateStore = defineStore('selectedDate', {
    state: () => ({
        selectedDate: new Date(),
    }),
    persist: {
        storage: sessionStorage,
        serializer: {
            serialize: (value) => JSON.stringify(value),
            deserialize: (value) => {
                const parsed = JSON.parse(value)
                if (parsed.gameDate) {
                    parsed.gameDate = new Date(parsed.gameDate)
                }
                return parsed
            },
        },
    },
})