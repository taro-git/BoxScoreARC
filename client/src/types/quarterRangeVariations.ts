export type quarterRangeVariations = 'Q1' | 'Q2' | 'firstHalf' | 'Q3' | 'Q4' | 'secondHalf' | 'fourQuarters' | 'all' | 'OT'

export const quarterRangeLabels: { value: quarterRangeVariations, label: string }[] = [
    { value: 'Q1', label: '1st Q.' },
    { value: 'Q2', label: '2nd Q.' },
    { value: 'firstHalf', label: 'First Half' },
    { value: 'Q3', label: '3rd Q.' },
    { value: 'Q4', label: '4th Q.' },
    { value: 'secondHalf', label: 'Second Half' },
    { value: 'fourQuarters', label: '4 Quarters' },
    { value: 'all', label: 'All' },
    { value: 'OT', label: 'Over Time' },
]
