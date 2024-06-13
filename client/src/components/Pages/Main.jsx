import React from 'react'
import { Container, Typography, Box } from '@mui/material'
import {SIGNIN} from "../../util/routes.js";
import ButtonLink from "../shared/ButtonLink.jsx";

const Main = () => {
  return (
    <Container maxWidth="md">
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        textAlign="center"
      >
        <Typography variant="h3" component="h1" gutterBottom>
          Welcome to the WebEye
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom>
          Stay Updated with Your Favorite Websites
        </Typography>
        <Typography variant="body1" paragraph>
          Our notification system allows you to add sites to a tracking system and be notified when a site has changed.
          The system will periodically check for changes. If any changes occur, you will be notified via email.
        </Typography>
        <Typography variant="body1" paragraph>
          To get started, please log in to your account.
        </Typography>
        <ButtonLink variant="contained" color="primary" href={SIGNIN}>
          Sign In
        </ButtonLink>
      </Box>
    </Container>
  )
}

export default Main
