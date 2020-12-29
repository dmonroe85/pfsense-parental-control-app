import React from 'react';

import { makeStyles } from '@material-ui/core/styles';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import ActionButton from './ActionButton';
import DateSelector from './DateSelector';

const ALLOWED_COLOR = '#66ffff'
const BLOCKED_COLOR = '#ffbbbb'

const useStyles = makeStyles({
  table: {
    // minWidth: 850,
  },
});

export default function AppTable(props) {

  var rows = [];
  for (var name in props.overrideConfig) { if (props.overrideConfig.hasOwnProperty(name)) {
    const isBlocked = (props.blocked !== undefined) && props.blocked.includes(name)
    rows.push({
      name,
      ...props.overrideConfig[name],
      isBlocked
    })
  } }

  return (
    <TableContainer component={Paper}>
        <Table className={useStyles().table} aria-label="simple table">
          <TableHead style={{backgroundColor: 'lightgrey'}}>
            <TableRow>
              <TableCell>Biscuit</TableCell>
              <TableCell align="left">Action</TableCell>
              <TableCell align="left">Start Date</TableCell>
              <TableCell align="left">End Date</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.map((row) => {
              const nameColor = row.isBlocked ? BLOCKED_COLOR : ALLOWED_COLOR;
              const nameStyle = { backgroundColor: nameColor };

              return (
                <TableRow key={row.name}>
                  <TableCell component="th" scope="row" style={nameStyle}>
                    {row.name} 
                  </TableCell>
                  <TableCell align="left">
                    <ActionButton {...props} row={row} />
                  </TableCell>
                  <TableCell align="left">
                    <DateSelector {...props} row={row} field={'startDate'} />
                  </TableCell>
                  <TableCell align="left">
                    <DateSelector {...props} row={row} field={'endDate'} />
                  </TableCell>
                </TableRow>
              )
            })}
          </TableBody>
        </Table>
      </TableContainer>
  )
}