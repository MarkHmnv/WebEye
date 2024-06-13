import {createSlice} from "@reduxjs/toolkit";
import {apiSlice} from "./apiSlice.js";
import {LOGIN_URL, REGISTER_URL} from "../../util/constants.js";
import {parseJwt} from "../../util/jwt.js";

const getItemOrNull = (key) => {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
}

const initialState = {
    accessToken: getItemOrNull("accessToken"),
    refreshToken: getItemOrNull("refreshToken"),
    username: getItemOrNull("username")
}

const authSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {
        setCredentials: (state, action) => {
            const {access_token, refresh_token} = action.payload
            state.username = parseJwt(access_token).name
            state.accessToken = access_token
            state.refreshToken = refresh_token
            localStorage.setItem("accessToken", JSON.stringify(state.accessToken))
            localStorage.setItem("refreshToken", JSON.stringify(state.refreshToken))
            localStorage.setItem("username", JSON.stringify(state.username))
        },
        removeCredentials: (state) => {
            state.accessToken = null
            state.refreshToken = null
            state.username = null
            localStorage.removeItem("accessToken")
            localStorage.removeItem("refreshToken")
            localStorage.removeItem("username")
        },
        updateName: (state, action) => {
            state.username = action.payload
            localStorage.setItem("username", JSON.stringify(state.username))
        }
    }
})

export const authApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        register: builder.mutation({
            query: (registerRequest) => ({
                url: REGISTER_URL,
                method: "POST",
                body: registerRequest
            })
        }),
        login: builder.mutation({
            query: (loginRequest) => ({
                url: LOGIN_URL,
                method: "POST",
                body: loginRequest
            })
        }),
    })
})

export const {setCredentials, removeCredentials, updateName} = authSlice.actions

export const {useRegisterMutation, useLoginMutation} = authApiSlice
export default authSlice.reducer