import { ref } from 'vue'
import type { Ref } from 'vue'

type SwipeBehavior = {
    offsets: Ref<{ [key: number]: number }>
    isSliding: Ref<boolean>
    slideAnimationDurationSec: number
    onTouchStart: (e: TouchEvent) => void
    onTouchMove: (e: TouchEvent) => void
    onTouchEnd: () => void
}

export type PositionControl = {
    key: number
    initialPosition: number,
    offset: {
        beforeOnSwipeFuncExe: {
            left: number,
            right: number,
        }
        afterOnSwipeFuncExe: {
            left: number,
            right: number,
        }
    }
}

export const swipeService = (
    onSwipeLeftFunc: () => void,
    onSwipeRightFunc: () => void,
    positionControls: PositionControl[],
): SwipeBehavior => {
    const startX = ref(0)
    const offsets = ref(Object.fromEntries(positionControls.map(
        item => [item.key, item.initialPosition]
    )))
    const isSliding = ref(false)
    const slideAnimationDurationMs = 300
    const slideAnimationDurationSec = slideAnimationDurationMs / 1000

    const onTouchStart = (e: TouchEvent) => {
        startX.value = e.touches[0].clientX
        isSliding.value = false
    }

    const onTouchMove = (e: TouchEvent) => {
        const currentX = e.touches[0].clientX
        offsets.value = Object.fromEntries(positionControls.map(
            item => [item.key, item.initialPosition + (currentX - startX.value)]
        ))
    }

    const onTouchEnd = () => {
        const delta = offsets.value[positionControls[0].key] - positionControls[0].initialPosition

        if (delta < -100) {
            isSliding.value = true
            offsets.value = Object.fromEntries(positionControls.map(
                item => [item.key, item.initialPosition + item.offset.beforeOnSwipeFuncExe.left]
            ))
            setTimeout(() => {
                onSwipeLeftFunc()
                offsets.value = Object.fromEntries(positionControls.map(
                    item => [item.key, item.initialPosition + item.offset.afterOnSwipeFuncExe.left]
                ))
                isSliding.value = false
            }, slideAnimationDurationMs)
        } else if (delta > 100) {
            isSliding.value = true
            offsets.value = Object.fromEntries(positionControls.map(
                item => [item.key, item.initialPosition + item.offset.beforeOnSwipeFuncExe.right]
            ))
            setTimeout(() => {
                onSwipeRightFunc()
                offsets.value = Object.fromEntries(positionControls.map(
                    item => [item.key, item.initialPosition + item.offset.afterOnSwipeFuncExe.right]
                ))
                isSliding.value = false
            }, slideAnimationDurationMs)
        } else {
            isSliding.value = true
            offsets.value = Object.fromEntries(positionControls.map(
                item => [item.key, item.initialPosition]
            ))
        }
    }

    return {
        offsets,
        isSliding,
        slideAnimationDurationSec,
        onTouchStart,
        onTouchMove,
        onTouchEnd,
    }
}
