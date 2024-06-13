import {apiSlice} from "./apiSlice.js"
import {PROFILE_URL} from "../../util/constants.js"

export const userSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getUserProfile: builder.query({
            query: () => PROFILE_URL,
        }),
        updateUserProfile: builder.mutation({
            query: (updatedUser) => ({
                url: PROFILE_URL,
                method: 'PATCH',
                body: updatedUser
            })
        }),
        deleteUserProfile: builder.mutation({
            query: () => ({
                url: PROFILE_URL,
                method: 'DELETE',
            })
        }),
    }),
})

export const {
    useGetUserProfileQuery,
    useUpdateUserProfileMutation,
    useDeleteUserProfileMutation
} = userSlice