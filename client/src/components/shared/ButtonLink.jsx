import { Button } from "@mui/material"
import { Link as ReactRouterLink } from "react-router-dom"

const ButtonLink = props => {
  return (
    <Button {...props} component={ReactRouterLink} to={props.href ?? "#"} />
  )
}

export default ButtonLink