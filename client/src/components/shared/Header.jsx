import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import IconButton from '@mui/material/IconButton'
import MenuIcon from '@mui/icons-material/Menu'
import ButtonLink from "./ButtonLink.jsx";
import {PROFILE, SIGNIN} from "../../util/routes.js";
import {useDispatch, useSelector} from "react-redux";
import Button from "@mui/material/Button";
import {removeCredentials} from "../../redux/slices/authSlice.js";

const Header = () => {
    const dispatch = useDispatch()
    const username = useSelector(state => state.auth.username)

    const handleLogout = () => {
        dispatch(removeCredentials())
    }

    return (
        <Box sx={{flexGrow: 1}} mb={8}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton
                        size="large"
                        edge="start"
                        color="inherit"
                        aria-label="menu"
                        sx={{mr: 2}}
                    >
                        <MenuIcon/>
                    </IconButton>
                    <Typography variant="h6" component="div" sx={{flexGrow: 1}}>
                        WebEye
                    </Typography>
                    {username
                        ? <Button color="inherit" onClick={handleLogout}>Log out</Button>
                        : <ButtonLink color="inherit" href={SIGNIN}>Sign in</ButtonLink>
                    }
                </Toolbar>
            </AppBar>
        </Box>
    )
}

export default Header