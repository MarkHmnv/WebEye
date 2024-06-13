import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from "./Link.jsx";

const Copyright = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 2,
        textAlign: 'center',
        position: 'fixed',
        bottom: 0,
        width: '100%',
        backgroundColor: 'transparent',
      }}
    >
      <Typography variant="body2" color="text.secondary">
        {'Copyright © '}
        <Link color="inherit" href="/">
          WebEye
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
    </Box>
  );
};

export default Copyright;
