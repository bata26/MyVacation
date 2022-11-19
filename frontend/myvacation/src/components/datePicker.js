import * as React from 'react';

import TextField from '@mui/material/TextField';
import { LocalizationProvider } from '@mui/x-date-pickers-pro';
import { AdapterDayjs } from '@mui/x-date-pickers-pro/AdapterDayjs';
import { StaticDateRangePicker } from '@mui/x-date-pickers-pro/StaticDateRangePicker';

import Box from '@mui/material/Box';

export default function DateRangePicker({startDate , endDate}) {
  const [value, setValue] = React.useState([null, null]);
  console.log(startDate);
  console.log(endDate);
  const dateRange = [startDate , endDate]

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <StaticDateRangePicker
        disabled
        displayStaticWrapperAs="desktop"
        value={dateRange}
        onChange={(newValue) => {
          setValue(newValue);
        }}
        renderInput={(startProps, endProps) => (
          <React.Fragment>
            <TextField {...startProps} />
            <Box sx={{ mx: 2 }}> to </Box>
            <TextField {...endProps} />
          </React.Fragment>
        )}
      />
    </LocalizationProvider>
  );
}