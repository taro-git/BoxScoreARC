export const BoxScoreStatusMessage = {
    ERRORED: 'errored',
    PENDING: 'pending',
    PROGRESSING: 'progressing',
    COMPLETED: 'completed',
} as const;

export type BoxScoreStatusMessage = typeof BoxScoreStatusMessage[keyof typeof BoxScoreStatusMessage];

export interface ScheduledBoxScoreStatus {
    game_id: number
    error_message?: string
    progress: number
    status: BoxScoreStatusMessage
}

