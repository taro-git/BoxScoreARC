import axios, { AxiosError } from 'axios'
import { REST_API_BASE_URL } from '../appEnv'

export class BackendApi {
    protected path: string = '/'

    protected setPath(path: string) {
        let collectedPath = path
        if (!path.endsWith('/')) {
            collectedPath = path + '/'
        }
        if (!collectedPath.startsWith('/')) {
            collectedPath = '/' + collectedPath
        }
        this.path = collectedPath
    }

    protected async get(params?: object, isValid?: (responseData: any) => boolean) {
        const responseData = (await axios.get(REST_API_BASE_URL + this.path, { params })).data
        if (isValid) {
            if (isValid(responseData)) {
                return responseData
            } else {
                throw new AxiosError('validation error: response from backend server is invalid')
            }
        } else {
            return responseData
        }
    }

    protected async post(data?: object) {
        return (await axios.post(REST_API_BASE_URL + this.path, data ?? {})).data
    }

    protected async delete(params?: object) {
        return (await axios.delete(REST_API_BASE_URL + this.path, { params })).data
    }
}
