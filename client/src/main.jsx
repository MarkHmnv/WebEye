import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import {CssBaseline, ThemeProvider} from "@mui/material";
import theme from "./util/theme.js";
import {BrowserRouter} from "react-router-dom";
import Header from "./components/shared/Header.jsx";
import Copyright from "./components/shared/Copyright.jsx";
import {Provider} from "react-redux";
import {store} from "./redux/store.js";
import {ToastContainer} from "react-toastify";
import 'react-toastify/dist/ReactToastify.css';

ReactDOM.createRoot(document.getElementById('root')).render(
    <React.StrictMode>
        <Provider store={store}>
            <ThemeProvider theme={theme}>
                <BrowserRouter>
                    <CssBaseline/>
                    <Header/>
                    <ToastContainer/>
                    <App/>
                    <Copyright/>
                </BrowserRouter>
            </ThemeProvider>
        </Provider>
    </React.StrictMode>,
)
