import { DateTimePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
import DateFnsUtils from '@date-io/date-fns';

export default function DateSelector(props) {
  return (
    <MuiPickersUtilsProvider utils={DateFnsUtils}>
      <DateTimePicker
        variant="dialog"
        showTodayButton={true}
        value={props.row[props.field]}
        onChange={(newDate) => {
          const newConfig = { ...props.overrideConfig };
          const newNameConfig = { ...newConfig[props.row.name] };
          
          newNameConfig[props.field] = newDate.getTime();
          
          newConfig[props.row.name] = newNameConfig;
          props.setOverrideConfig(newConfig);
        }}
      />
    </MuiPickersUtilsProvider>
  )
}