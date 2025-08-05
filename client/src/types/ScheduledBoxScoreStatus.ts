export const BoxScoreStatusMessage = {
    ERRORED: 'errored',
    PENDING: 'pending',
    PROGRESSING: 'progressing',
    COMPLETED: 'completed',
} as const;

export type BoxScoreStatusMessage = typeof BoxScoreStatusMessage[keyof typeof BoxScoreStatusMessage];

export interface ScheduledBoxScoreStatus {
    gameId: number
    errorMessage?: string
    progress: number
    status: BoxScoreStatusMessage
}

