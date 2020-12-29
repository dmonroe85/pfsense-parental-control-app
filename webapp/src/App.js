import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';
import AppTable from './AppTable'

import Button from '@material-ui/core/Button';

// API
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

    console.log("Requesting Override Config")
    axios.get(host + '/get_config')
      .then(r => setOverrideConfig(r.data))
      .catch(e => console.log(e))
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
          console.log("Writing Config payload:")
          console.log(overrideConfig)
          axios.put(host + '/set_config', overrideConfig)
            .then(r => alert("Successfully pushed new config"))
            .catch(e => console.log(e))
        }}
      >
        SUBMIT
      </Button>
    </div>
  );
}
