import Avatar from '@mui/material/Avatar'
import Button from '@mui/material/Button'
import CssBaseline from '@mui/material/CssBaseline'
import TextField from '@mui/material/TextField'
import Grid from '@mui/material/Grid'
import Box from '@mui/material/Box'
import LockOutlinedIcon from '@mui/icons-material/LockOutlined'
import Typography from '@mui/material/Typography'
import Container from '@mui/material/Container'
import {PROFILE, SIGNIN} from "../../util/routes.js";
import Link from "../shared/Link.jsx";
import {useEffect} from "react";
import {useDispatch, useSelector} from "react-redux";
import {useLocation, useNavigate} from "react-router-dom";
import {setCredentials, useRegisterMutation} from "../../redux/slices/authSlice.js";
import {toastError} from "../../util/toastError.js";

const SignUp = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const {search} = useLocation();
    const [register, {isLoading}] = useRegisterMutation()
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
                name: data.get('firstName') + " " + data.get('lastName'),
                email: data.get('email'),
                password: data.get('password'),
            }
            const res = await register(request).unwrap()
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
                    Sign up
                </Typography>
                <Box component="form" noValidate onSubmit={handleSubmit} sx={{mt: 3}}>
                    <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                autoComplete="given-name"
                                name="firstName"
                                required
                                fullWidth
                                id="firstName"
                                label="First Name"
                                autoFocus
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                required
                                fullWidth
                                id="lastName"
                                label="Last Name"
                                name="lastName"
                                autoComplete="family-name"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                id="email"
                                label="Email Address"
                                name="email"
                                autoComplete="email"
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                required
                                fullWidth
                                name="password"
                                label="Password"
                                type="password"
                                id="password"
                                autoComplete="new-password"
                            />
                        </Grid>
                    </Grid>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{mt: 3, mb: 2}}
                        disabled={isLoading}
                    >
                        {isLoading ? "Loading..." : "Sign Up"}
                    </Button>
                    <Grid container justifyContent="flex-end">
                        <Grid item>
                            <Link href={SIGNIN} variant="body2">
                                Already have an account? Sign in
                            </Link>
                        </Grid>
                    </Grid>
                </Box>
            </Box>
        </Container>
    )
}

export default SignUp