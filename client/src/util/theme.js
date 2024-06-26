import {createTheme} from '@mui/material/styles'
import {red} from '@mui/material/colors'

const theme = createTheme({
    palette: {
        mode: 'dark',
        primary: {
            main: '#556cd6',
        },
        secondary: {
            main: '#ef5c5c',
        },
        error: {
            main: red.A400,
        },
    },
})

export default theme