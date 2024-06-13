import {configureStore} from "@reduxjs/toolkit"
import {apiSlice} from "./slices/apiSlice"
import authSliceReducer from "./slices/authSlice.js"

export const store = configureStore({
    reducer: {
        [apiSlice.reducerPath]: apiSlice.reducer,
        auth: authSliceReducer
    },
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware().concat(apiSlice.middleware),
    devTools: import.meta.env.VITE_ENV !== "production"
})