import React, {useState} from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';
import ButtonLink from "./ButtonLink.jsx";
import {HOME, PROFILE, SIGNIN, MONITORING} from "../../util/routes.js";
import {useDispatch, useSelector} from "react-redux";
import Button from "@mui/material/Button";
import {removeCredentials} from "../../redux/slices/authSlice.js";
import Link from "./Link.jsx";

const Header = () => {
    const dispatch = useDispatch();
    const username = useSelector(state => state.auth.username);
    const [drawerOpen, setDrawerOpen] = useState(false);

    const toggleDrawer = (open) => (event) => {
        if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
            return;
        }
        setDrawerOpen(open);
    };

    const handleLogout = () => {
        dispatch(removeCredentials());
    };

    const list = () => (
        <Box
            sx={{width: 250}}
            role="presentation"
            onClick={toggleDrawer(false)}
            onKeyDown={toggleDrawer(false)}
        >
            <List>
                <ListItem button component={Link} href={HOME}>
                    <ListItemText primary="Home"/>
                </ListItem>
                <ListItem button component={Link} href={PROFILE}>
                    <ListItemText primary="Profile"/>
                </ListItem>
                <ListItem button component={Link} href={MONITORING}>
                    <ListItemText primary="Monitoring"/>
                </ListItem>
            </List>
            <Divider/>
            {username
                ? <ListItem button onClick={handleLogout}>
                    <ListItemText primary="Log out"/>
                </ListItem>
                : <ListItem button component={Link} href={SIGNIN}>
                    <ListItemText primary="Sign in"/>
                </ListItem>
            }
        </Box>
    );

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
                        onClick={toggleDrawer(true)}
                    >
                        <MenuIcon/>
                    </IconButton>
                    <Typography variant="h6" component="div" sx={{flexGrow: 1}}>
                        <Link color="inherit" sx={{textDecoration: 'none'}} href={HOME}>WebEye</Link>
                    </Typography>
                    {username
                        ? <Button color="inherit" onClick={handleLogout}>Log out</Button>
                        : <ButtonLink color="inherit" href={SIGNIN}>Sign in</ButtonLink>
                    }
                </Toolbar>
            </AppBar>
            <Drawer
                anchor="left"
                open={drawerOpen}
                onClose={toggleDrawer(false)}
            >
                {list()}
            </Drawer>
        </Box>
    );
}

export default Header;
