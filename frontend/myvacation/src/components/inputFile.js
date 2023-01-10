import { useRef, useState } from "react";
import { useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from '@mui/material/Button';

const FileInput = ({ label, onChange }) => {
  const ref = useRef();
  const theme = useTheme();
  //const classes = useStyles();
  const [attachment, setAttachment] = useState(null);

  const handleChange = (event) => {
    const files = Array.from(event.target.files);
    const [file] = files;
    setAttachment(file);
  };

  return (
    <Box
      position="relative"
      height={98}
      borderBottom={4}
    >
      <Box position="absolute" top={0} bottom={0} left={0} right={0} mx={2}>
        <TextField
          variant="standard"
          InputProps={{ disableUnderline: true }}
          margin="normal"
          fullWidth
          disabled
          label={label}
          value={attachment?.name || ""}
        />
      </Box>
      <Button
        component="label"
        style={{width: "100%",
            height: "100%",
            overflow: "hidden"}}
        onKeyDown={(e) => e.keyCode === 32 && ref.current?.click()}
      >
        <input
          ref={ref}
          type="file"
          accept="image/*"
          multiple
          hidden
          id="images"
          onChange={handleChange}
        />
      </Button>
    </Box>
  );
};

//const useStyles = makeStyles((theme) => ({
//  field: {
//    "& .MuiFormLabel-root.Mui-disabled": {
//      color: theme.palette.text.secondary
//    }
//  },
//  button: {
//    width: "100%",
//    height: "100%",
//    overflow: "hidden"
//  }
//}));

export default FileInput;
