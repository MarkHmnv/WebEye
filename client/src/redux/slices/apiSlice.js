import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react"
import {BASE_URL, REFRESH_TOKEN_URL} from "../../util/constants"
import {setCredentials, removeCredentials} from "./authSlice.js"

const baseQuery = fetchBaseQuery({
    baseUrl: BASE_URL,
    prepareHeaders: (headers, {getState}) => {
        const token = getState().auth.accessToken
        if (token) {
            headers.set('Authorization', `Bearer ${token}`)
        }
        return headers
    },
})

let refreshPromise = null

const baseQueryWithReauth = async (args, api, extraOptions) => {
    let result = await baseQuery(args, api, extraOptions)
    const refreshToken = api.getState().auth.refreshToken

    if (result.error && result.error.status === 401 && refreshToken) {
        refreshPromise = (async () => {
            const refreshResult = await baseQuery(
                {
                    url: REFRESH_TOKEN_URL,
                    method: 'POST',
                    body: {refresh_token: refreshToken},
                },
                api,
                extraOptions,
            )

            if (refreshResult.data) {
                api.dispatch(setCredentials(refreshResult.data))
            } else {
                api.dispatch(removeCredentials())
            }

            return refreshResult.data
        })()

        await refreshPromise

        result = await baseQuery(args, api, extraOptions)
    }

    return result
}

export const apiSlice = createApi({
    baseQuery: baseQueryWithReauth,
    tagTypes: ["User", "WebsiteMonitor"],
    endpoints: () => ({}),
})
