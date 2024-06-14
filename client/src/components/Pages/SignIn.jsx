import Avatar from '@mui/material/Avatar'
import Button from '@mui/material/Button'
import CssBaseline from '@mui/material/CssBaseline'
import TextField from '@mui/material/TextField'
import Grid from '@mui/material/Grid'
import Box from '@mui/material/Box'
import LockOutlinedIcon from '@mui/icons-material/LockOutlined'
import Typography from '@mui/material/Typography'
import Container from '@mui/material/Container'
import Link from "../shared/Link.jsx";
import {PROFILE, SIGNUP} from "../../util/routes.js";
import {useDispatch, useSelector} from "react-redux";
import {useLocation, useNavigate} from "react-router-dom";
import {setCredentials, useLoginMutation} from "../../redux/slices/authSlice.js";
import {useEffect} from "react";
import {toastError} from "../../util/toastError.js";

const SignIn = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const {search} = useLocation();
    const [login, {isLoading}] = useLoginMutation()
    const accessToken = useSelector(state => state.auth.accessToken);
    const searchParams = new URLSearchParams(search);
    const redirect = searchParams.get("redirect") || PROFILE;

    useEffect(() => {
        if (accessToken) {
            navigate(redirect);
        }
    }, [accessToken, redirect, navigate]);

    const handleSubmit = async (event) => {
        event.preventDefault()
        try {
            const data = new FormData(event.currentTarget)
            const request = {
                email: data.get('email'),
                password: data.get('password'),
            }
            const res = await login(request).unwrap()
            dispatch(setCredentials(res))
            navigate(redirect)
        } catch (e) {
            toastError(e)
        }
    }

    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline/>
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Avatar sx={{m: 1, bgcolor: 'secondary.main'}}>
                    <LockOutlinedIcon/>
                </Avatar>
                <Typography component="h1" variant="h5">
                    Sign in
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate sx={{mt: 1}}>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="email"
                        label="Email Address"
                        name="email"
                        autoComplete="email"
                        autoFocus
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        id="password"
                        autoComplete="current-password"
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{mt: 3, mb: 2}}
                        disabled={isLoading}
                    >
                        {isLoading ? "Loading..." : "Sign In"}
                    </Button>
                    <Grid container justifyContent="flex-end">
                        <Grid item>
                            <Link href={SIGNUP} variant="body2">
                                Don't have an account? Sign Up
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </Box>
        </Container>
    )
}

export default SignIn