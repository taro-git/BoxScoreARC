import { type BoxScoreTableData, type BoxScore, type PlayerOnBoxScore, BoxScoreColumnKeys } from "../types/BoxScore"

export const updateBoxScoreData = (boxScoreTableData: BoxScoreTableData, boxScore: BoxScore, startRange: number, endRange: number): { boxScoreTableData: BoxScoreTableData, homeStats: number[], awayStats: number[] } => {
    if (startRange > endRange) {
        throw new Error("invalid game clock range, start > end")
    }
    let homeStats = new Array(BoxScoreColumnKeys.slice(1).length).fill(0)
    let awayStats = new Array(BoxScoreColumnKeys.slice(1).length).fill(0)
    for (const player of boxScore.homePlayers) {
        const stats = updatePlayerBoxScore(player, startRange, endRange)
        boxScoreTableData[player.playerId] = stats
        homeStats = homeStats.map((num, i) => num + stats[i])
    }
    for (const player of boxScore.awayPlayers) {
        const stats = updatePlayerBoxScore(player, startRange, endRange)
        boxScoreTableData[player.playerId] = stats
        awayStats = awayStats.map((num, i) => num + stats[i])
    }
    return { boxScoreTableData: boxScoreTableData, homeStats: updateForTeamStats(homeStats).slice(1), awayStats: updateForTeamStats(awayStats).slice(1) }
}

const updatePlayerBoxScore = (player: PlayerOnBoxScore, startRange: number, endRange: number) => {
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
        return calcShootingPercentageAdd(new Array(boxScoreRaw[0].length - 2).fill(0))
    } else {
        return calcShootingPercentageAdd(endBoxScore.map((v, i) => Math.round((v - startBoxScore[i]) * 10) / 10))
    }
}

const calcShootingPercentageAdd = (boxScoreRow: number[]) => {
    let fgper = 0
    let threeper = 0
    let ftper = 0
    if (boxScoreRow[7] !== 0) {
        fgper = Math.round((boxScoreRow[6] / boxScoreRow[7]) * 100 * 10) / 10
    }
    if (boxScoreRow[9] !== 0) {
        threeper = Math.round((boxScoreRow[8] / boxScoreRow[9]) * 100 * 10) / 10
    }
    if (boxScoreRow[11] !== 0) {
        ftper = Math.round((boxScoreRow[10] / boxScoreRow[11]) * 100 * 10) / 10
    }
    const result = boxScoreRow
    result.splice(8, 0, fgper)
    result.splice(11, 0, threeper)
    result.splice(14, 0, ftper)
    return result
}

const updateForTeamStats = (boxScoreRow: number[]) => {
    const result = boxScoreRow
    if (boxScoreRow[7] !== 0) {
        result[8] = Math.round((boxScoreRow[6] / boxScoreRow[7]) * 100 * 10) / 10
    }
    if (boxScoreRow[10] !== 0) {
        result[11] = Math.round((boxScoreRow[9] / boxScoreRow[10]) * 100 * 10) / 10
    }
    if (boxScoreRow[13] !== 0) {
        result[14] = Math.round((boxScoreRow[12] / boxScoreRow[13]) * 100 * 10) / 10
    }
    result[20] = Math.round(boxScoreRow[20] / 5)
    return result
}

