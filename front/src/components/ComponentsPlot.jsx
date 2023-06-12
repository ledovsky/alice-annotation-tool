import { useEffect } from 'react';
import Plotly from 'plotly.js';


function ComponentsPlot (props) {

  useEffect(() => {
    let data = props.data;
    let layout = props.layout;
    if (data) {
      Plotly.newPlot('components-plot', data, layout, {displayModeBar: false});
    }
  }, [props.data]);

  return (
    <div id="components-plot"></div>
  )
}

export default ComponentsPlot;