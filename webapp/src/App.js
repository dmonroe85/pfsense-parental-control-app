import React, { useState, useEffect } from 'react';
import './App.css';
import AWS from 'aws-sdk';
import axios from 'axios';
import AppTable from './AppTable'

import Button from '@material-ui/core/Button';


// APIs
AWS.config.region = 'us-east-1'; // Region
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: process.env.REACT_APP_IDENTITY_POOL_ID
});

const lambda = new AWS.Lambda();

const pullParams = {
  FunctionName : process.env.REACT_APP_GET_FUNCTION_NAME,
  InvocationType : 'RequestResponse',
  LogType : 'None'
};

const pushParams = (payload) => {
  return {
    FunctionName : process.env.REACT_APP_SET_FUNCTION_NAME,
    InvocationType : 'RequestResponse',
    LogType : 'None',
    Payload: JSON.stringify(payload)
  }
}

const host = process.env.REACT_APP_API_HOST

// App Component
export default function App() {
  const [overrideConfig, setOverrideConfig] = useState({});
  const [blocked, setBlocked] = useState([]);

  // Run Once
  useEffect(() => {
    console.log("Requesting PFSense Blocklist")
    axios.get(host + '/get_blocked')
      .then(r => setBlocked(r.data))
      .catch(e => console.log(e))

    console.log("Invoking Lambda")
    lambda.invoke(pullParams, function(err, data) {
      if (err) {
        console.log(err);
      } else {
        setOverrideConfig(JSON.parse(JSON.parse(data.Payload)));
      }
    });
  }, [])

  const appProps = { overrideConfig, setOverrideConfig, blocked };

  return (
    <div>
      After you make changes, wait one minute and refresh to see updates.
      <AppTable {...appProps} />
      <Button
        variant="contained"
        color="secondary"
        onClick={() => {
          console.log("Invoking Lambda with payload:")
          console.log(overrideConfig)
          lambda.invoke(pushParams(overrideConfig), function(err, data) {
            if (err) {
              console.log(err);
            } else {
              alert("Successfully pushed new config");
            }
          });
        }}
      >
        SUBMIT
      </Button>
    </div>
  );
}
