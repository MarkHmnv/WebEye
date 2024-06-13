import {useSelector} from "react-redux";
import {Navigate, Outlet} from "react-router-dom";
import {SIGNIN} from "./util/routes.js";

export const PrivateRoutes = () => {
    const accessToken = useSelector(state => state.auth.accessToken)
    return accessToken ? <Outlet/> : <Navigate to={SIGNIN}/>
}