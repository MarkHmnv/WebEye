import {apiSlice} from "./apiSlice.js"
import {MONITORING_URL} from "../../util/constants.js"

export const monitorSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getAllMonitors: builder.query({
            query: () => MONITORING_URL,
        }),
        createMonitor: builder.mutation({
            query: (monitor) => ({
                url: MONITORING_URL,
                method: 'POST',
                body: monitor
            })
        }),
        deleteMonitor: builder.mutation({
            query: (id) => ({
                url: `${MONITORING_URL}/${id}`,
                method: 'DELETE',
            })
        }),
    }),
})

export const {
    useGetAllMonitorsQuery,
    useCreateMonitorMutation,
    useDeleteMonitorMutation
} = monitorSlice