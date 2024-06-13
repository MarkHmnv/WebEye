import React, { useEffect, useState } from 'react'
import { Container, TextField, Button, Box, Typography } from '@mui/material'
import {
    useDeleteUserProfileMutation,
    useGetUserProfileQuery,
    useUpdateUserProfileMutation
} from "../../redux/slices/userSlice.js"
import { useDispatch } from "react-redux"
import { removeCredentials, updateName } from "../../redux/slices/authSlice.js"
import { toastError } from "../../util/toastError.js"
import { toast } from "react-toastify"
import AlertDialog from "../shared/AlertDialog.jsx";

const Profile = () => {
    const dispatch = useDispatch()
    const { data: profile, isLoading } = useGetUserProfileQuery()
    const [updateUserProfile, { isLoading: isUpdating }] = useUpdateUserProfileMutation()
    const [deleteUserProfile, { isLoading: isDeleting }] = useDeleteUserProfileMutation()
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [dialogOpen, setDialogOpen] = useState(false)

    useEffect(() => {
        if (profile) {
            setName(profile.name)
            setEmail(profile.email)
        }
    }, [profile])

    const handleUpdateProfile = async (event) => {
        event.preventDefault()
        try {
            await updateUserProfile({ name, email }).unwrap()
            dispatch(updateName(name))
            toast.success("Profile updated successfully")
        } catch (e) {
            toastError(e)
        }
    }

    const handleDeleteProfile = async () => {
        try {
            await deleteUserProfile().unwrap()
            dispatch(removeCredentials())
            toast.success("Profile deleted successfully")
        } catch (e) {
            toastError(e)
        }
    }

    const handleDialogClose = () => {
        setDialogOpen(false)
    }

    const handleDialogConfirm = async () => {
        await handleDeleteProfile()
        setDialogOpen(false)
    }

    return (
        <Container maxWidth="sm" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <Typography variant="h4" component="h1" gutterBottom align="center">
                User Profile
            </Typography>
            <Box
                component="form"
                onSubmit={handleUpdateProfile}
                sx={{ display: 'flex', flexDirection: 'column', gap: 2, width: '100%' }}
            >
                <TextField
                    label="Name"
                    variant="outlined"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    fullWidth
                />
                <TextField
                    label="Email"
                    variant="outlined"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    fullWidth
                />
                <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    disabled={isUpdating || isLoading}
                >
                    {isUpdating || isLoading ? "Loading..." : "Update"}
                </Button>
                <Button
                    variant="contained"
                    color="error"
                    disabled={isDeleting || isLoading}
                    onClick={() => setDialogOpen(true)}
                >
                    {isDeleting || isLoading ? "Loading..." : "Delete"}
                </Button>
            </Box>
            <AlertDialog
                open={dialogOpen}
                handleClose={handleDialogClose}
                handleConfirm={handleDialogConfirm}
                title="Confirm Delete"
                message="Are you sure you want to delete your account?"
            />
        </Container>
    )
}

export default Profile
