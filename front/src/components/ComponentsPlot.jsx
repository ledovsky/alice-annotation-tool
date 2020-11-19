import { useEffect } from 'react';
import Plotly from 'plotly.js';


function ComponentsPlot (props) {

  useEffect(() => {
    let data = props.data;
    let layout = props.layout;
    Plotly.newPlot('components-plot', data, layout, {displayModeBar: false});
  }, []);

  return (
    <div id="components-plot"></div>
  )
}

export default ComponentsPlot;