export type quarterRangeVariations = 'Q1' | 'Q2' | 'firstHalf' | 'Q3' | 'Q4' | 'secondHalf' | 'fourQuarters' | 'all' | 'OT'

export const quarterRangeLabels: { value: quarterRangeVariations, title: string }[] = [
    { value: 'Q1', title: '1st Q.' },
    { value: 'Q2', title: '2nd Q.' },
    { value: 'firstHalf', title: 'First Half' },
    { value: 'Q3', title: '3rd Q.' },
    { value: 'Q4', title: '4th Q.' },
    { value: 'secondHalf', title: 'Second Half' },
    { value: 'fourQuarters', title: '4 Quarters' },
    { value: 'all', title: 'All' },
    { value: 'OT', title: 'Over Time' },
]
