import React from 'react';
import Button from '@material-ui/core/Button';

const ALLOWED = 'ALLOWED';
const BLOCKED = 'BLOCKED';

function getButtonStyle(row) {
  switch(row.action) {
    case ALLOWED:
      return { text: ALLOWED, buttonType: "primary" };
    case BLOCKED:
      return { text: BLOCKED, buttonType: "secondary" };
    default:
      return { text: "UNDEFINED", buttonType: "default" };
  }
}

export default function ActionButton(props) {

  const buttonStyle = getButtonStyle(props.row);

  return (
    <Button
      variant="outlined"
      color={buttonStyle.buttonType}
      onClick={() => {
        const newConfig = { ...props.overrideConfig };
        const newNameConfig = { ...newConfig[props.row.name] };

        switch(props.row.action) {
          case ALLOWED:
            newNameConfig['action'] = BLOCKED;
            break;
          default:
            newNameConfig['action'] = ALLOWED;
            break;
        }

        newConfig[props.row.name] = newNameConfig;

        props.setOverrideConfig(newConfig);
      }}
    >
      {buttonStyle.text}
    </Button>
  )
}