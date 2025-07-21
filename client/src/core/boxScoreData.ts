import { BOX_SCORE_COLUMN_KEYS, type BoxScoreData, type BoxScoreRawData } from "../types/BoxScore"

export const updateBoxScoreData = (boxScoreData: BoxScoreData, boxScoreRawData: BoxScoreRawData, startRange: number, endRange: number): BoxScoreData => {
    if (startRange > endRange) {
        throw new Error("invalid game clock range, start > end")
    }
    for (const [player_id_str, box_score_raw] of Object.entries(boxScoreRawData)) {
        const player_id = parseInt(player_id_str, 10)
        let start_box_score: number[] | null = null
        let end_box_score: number[] | null = null
        for (let i = 0; i < box_score_raw.length; i++) {
            const [time, box_score] = box_score_raw[i]
            if (time >= startRange) {
                if (!start_box_score) {
                    if (i == 0) {
                        start_box_score = new Array(BOX_SCORE_COLUMN_KEYS.length - 1).fill(0)
                    } else {
                        start_box_score = box_score_raw[i - 1][1]
                    }
                }
                if (time <= endRange) {
                    if (i == 0) {
                        end_box_score = new Array(BOX_SCORE_COLUMN_KEYS.length - 1).fill(0)
                    } else {
                        end_box_score = box_score
                    }
                } else {
                    break
                }
            }
        }
        if (!start_box_score || !end_box_score) {
            boxScoreData[player_id] = convertPlayTimeToMin(calcShootingPercentage(new Array(BOX_SCORE_COLUMN_KEYS.length - 1).fill(0)))
        } else {
            boxScoreData[player_id] = convertPlayTimeToMin(calcShootingPercentage(end_box_score.map((v, i) => v - start_box_score[i])))
        }
    }
    return boxScoreData
}

const calcShootingPercentage = (boxScoraRow: number[]) => {
    let result = boxScoraRow
    if (result.length < 15) {
        throw new Error("invalid box score data row")
    }

    if (boxScoraRow[7] !== 0) {
        result[8] = Math.round((boxScoraRow[6] / boxScoraRow[7]) * 100 * 10) / 10
    } else {
        result[8] = 0
    }

    if (boxScoraRow[10] !== 0) {
        result[11] = Math.round((boxScoraRow[9] / boxScoraRow[10]) * 100 * 10) / 10
    } else {
        result[11] = 0
    }

    if (boxScoraRow[13] !== 0) {
        result[14] = Math.round((boxScoraRow[12] / boxScoraRow[13]) * 100 * 10) / 10
    } else {
        result[14] = 0
    }
    return result
}

const convertPlayTimeToMin = (boxScoraRow: number[]) => {
    let result = boxScoraRow
    result[0] = Math.round(boxScoraRow[0] / 60 * 10) / 10
    return result
}