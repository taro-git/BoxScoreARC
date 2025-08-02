import { type BoxScoreTableData, type BoxScore } from "../types/BoxScore"

export const updateBoxScoreData = (boxScoreTableData: BoxScoreTableData, boxScore: BoxScore, startRange: number, endRange: number): BoxScoreTableData => {
    if (startRange > endRange) {
        throw new Error("invalid game clock range, start > end")
    }
    for (const player of [...boxScore.homePlayers, ...boxScore.awayPlayers]) {
        const playerId = player.playerId
        const boxScoreRaw = player.boxScoreData
        let startBoxScore: number[] | null = null
        let endBoxScore: number[] | null = null
        let lastTime = 0
        let boxScoreDataAtLastSec = new Array(boxScoreRaw[0].length - 2).fill(0)
        for (let i = 0; i < boxScoreRaw.length; i++) {
            const time = boxScoreRaw[i][0]
            const boxScoreData = boxScoreRaw[i].slice(2) as number[]
            if (i != 0 && lastTime != time) {
                boxScoreDataAtLastSec = boxScoreRaw[i - 1].slice(2) as number[]
            }
            if (time >= startRange) {
                if (!startBoxScore) {
                    if (i == 0) {
                        startBoxScore = new Array(boxScoreData.length).fill(0)
                    } else {
                        startBoxScore = boxScoreDataAtLastSec
                    }
                }
                if (time <= endRange) {
                    if (i == 0) {
                        endBoxScore = new Array(boxScoreData.length).fill(0)
                    } else {
                        endBoxScore = boxScoreData
                    }
                } else {
                    break
                }
            }
            lastTime = time
        }
        if (!startBoxScore || !endBoxScore) {
            boxScoreTableData[playerId] = calcShootingPercentage(new Array(boxScoreRaw[0].length - 2).fill(0))
        } else {
            boxScoreTableData[playerId] = calcShootingPercentage(endBoxScore.map((v, i) => Math.round((v - startBoxScore[i]) * 10) / 10))
        }
    }
    return boxScoreTableData
}

const calcShootingPercentage = (boxScoraRow: number[]) => {
    let fgper = 0
    let threeper = 0
    let ftper = 0
    if (boxScoraRow[7] !== 0) {
        fgper = Math.round((boxScoraRow[6] / boxScoraRow[7]) * 100 * 10) / 10
    }
    if (boxScoraRow[9] !== 0) {
        threeper = Math.round((boxScoraRow[8] / boxScoraRow[9]) * 100 * 10) / 10
    }
    if (boxScoraRow[11] !== 0) {
        ftper = Math.round((boxScoraRow[10] / boxScoraRow[11]) * 100 * 10) / 10
    }
    const result = boxScoraRow
    result.splice(8, 0, fgper)
    result.splice(11, 0, threeper)
    result.splice(14, 0, ftper)
    return result
}
