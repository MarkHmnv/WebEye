import {Route, Routes} from "react-router-dom";
import {HOME, MONITORING, PROFILE, SIGNIN, SIGNUP} from "./util/routes.js";
import Main from "./components/Pages/Main.jsx";
import SignUp from "./components/Pages/SignUp.jsx";
import SignIn from "./components/Pages/SignIn.jsx";
import {PrivateRoutes} from "./privateRoutes.jsx";
import Profile from "./components/Pages/Profile.jsx";
import Monitoring from "./components/Pages/Monitoring.jsx";

const App = () => {
    return (
        <Routes>
            <Route path={HOME} element={<Main/>}/>
            <Route path={SIGNUP} element={<SignUp/>}/>
            <Route path={SIGNIN} element={<SignIn/>}/>

            <Route element={<PrivateRoutes/>}>
                <Route path={PROFILE} element={<Profile/>}/>
                <Route path={MONITORING} element={<Monitoring/>}/>
            </Route>
        </Routes>
    )
}

export default App
