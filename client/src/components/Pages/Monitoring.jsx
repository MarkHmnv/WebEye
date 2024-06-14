import {useEffect, useState} from 'react'
import {
    Container,
    TextField,
    Button,
    List,
    ListItem,
    ListItemText,
    IconButton,
    Typography,
    Grid,
    CircularProgress
} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import {
    useCreateMonitorMutation,
    useDeleteMonitorMutation,
    useGetAllMonitorsQuery
} from "../../redux/slices/monitorSlice.js"
import {toastError} from "../../util/toastError.js"
import {toast} from "react-toastify";

const Monitoring = () => {
    const {data: monitors, isLoading: isLoadingMonitors} = useGetAllMonitorsQuery()
    const [createMonitor, {isLoading: isCreating}] = useCreateMonitorMutation()
    const [deleteMonitor, {isLoading: isDeleting}] = useDeleteMonitorMutation()
    const [url, setUrl] = useState('')
    const [intervalMinutes, setIntervalMinutes] = useState('1')
    const [urls, setUrls] = useState([])

    const urlPattern = /^(https?:\/\/)(www\.)?([a-zA-Z0-9-]+(\.[a-zA-Z]{2,})+)(:\d{1,5})?(\/\S*)?$/

    useEffect(() => {
        if (monitors) {
            setUrls(monitors)
        }
    }, [monitors])

    const handleAddLink = async () => {
        if (!intervalMinutes || intervalMinutes < 1 && intervalMinutes > 90) {
            toast.error("Time frequency must be between 1 and 90 minutes")
            return
        }

        if (!url || !urlPattern.test(url)) {
            toast.error("Invalid URL")
            return
        }

        try {
            const newMonitor = await createMonitor({url: url, interval_minutes: intervalMinutes}).unwrap()
            setUrls([...urls, newMonitor])
            setUrl('')
            toast.success("Link added successfully")
        } catch (e) {
            toastError(e)
        }
    }

    const handleDeleteLink = async (id) => {
        try {
            await deleteMonitor(id).unwrap()
            setUrls(urls.filter((link) => link.id !== id))
            toast.success("Link deleted successfully")
        } catch (e) {
            toastError(e)
        }
    }

    return (
        <Container>
            <Typography variant="h4" gutterBottom>
                Websites to monitor
            </Typography>
            <Grid container spacing={2} alignItems="center">
                <Grid item xs={10}>
                    <TextField
                        label="Link"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        fullWidth
                    />
                </Grid>
                <Grid item xs={2}>
                    <TextField
                        label="Frequency (min)"
                        value={intervalMinutes}
                        onChange={(e) => setIntervalMinutes(e.target.value)}
                        type="number"
                        inputProps={{min: 1, max: 90}}
                        fullWidth
                    />
                </Grid>
            </Grid>
            <Button
                variant="contained"
                color="primary"
                onClick={handleAddLink}
                fullWidth
                style={{marginTop: '16px'}}
            >
                Add Link
            </Button>
            <List>
                {
                    isLoadingMonitors || isCreating || isDeleting ? <CircularProgress/> :
                        urls.map((item) => (
                            <ListItem
                                key={item.id}
                                secondaryAction={
                                    <IconButton edge="end" aria-label="delete"
                                                onClick={() => handleDeleteLink(item.id)}>
                                        <DeleteIcon/>
                                    </IconButton>
                                }
                            >
                                <ListItemText
                                    primary={item.url}
                                    secondary={`Frequency: ${item.interval_minutes} minute(s)`}
                                />
                            </ListItem>
                        ))
                }
            </List>
        </Container>
    )
}

export default Monitoring
