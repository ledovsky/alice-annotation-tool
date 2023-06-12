import { React } from 'react';
import AnnotationBar from './AnnotationBar';
import Button from '../common/Button';
import Spinner from '../common/Spinner';
import ComponentsPlot from './ComponentsPlot';
import AnnotationForm from './AnnotationForm';
import AnnotationFormV2 from './AnnotationFormV2';


function ComponentAnnotation( props ) {
  return (
    <div>
      <AnnotationBar ic={props.ic} dataset={props.dataset} subject={props.subject} state="annotation"/>
      <div className="mt-6 ml-6" hidden={!props.loading}>
        <Spinner/>
      </div>
      {/* Hidden property did not work for flex => used JSX if */}
      { !props.loading ? 
        <div className="mx-6 mt-6 flex">
        <div className="w-full max-w-sm">
        { props.dataset.annotation_version === "v1" ? 
        <AnnotationForm onChange={props.onChange} onSubmit={props.onSubmit} 
         annotation={props.annotation} loggedIn={props.loggedIn} />
        : <AnnotationFormV2 onSubmit={props.onSubmit} annotation={props.annotation} 
           handleCheck={props.handleCheck} loggedIn={props.loggedIn}/>
        }
        </div>
        <div className="w-full">
          <div className="flex">
            <div className="w-full px-6 max-w-md">
              <p className="text-center font-bold">Topomap of the component</p>
              { props.ic.x ?
                <img 
                  src={
                    process.env.REACT_APP_MEDIA_URL 
                    ? process.env.REACT_APP_MEDIA_URL + props.ic.x.topomap_url : 
                    props.ic.x.topomap_url} 
                  alt=""/> : <div></div>
              }
            </div>
            <div className="w-full px-6 max-w-md">
              <p className="text-center font-bold">Spectrum</p>
              { props.ic.x ?
                <img 
                  src={
                    process.env.REACT_APP_MEDIA_URL 
                    ? process.env.REACT_APP_MEDIA_URL + props.ic.x.spectrum_url : 
                    props.ic.x.spectrum_url} 
                  alt=""/> : <div></div>
              }
            </div>
            <div className="w-full px-6 max-w-md">
              <p className="text-center font-bold">Epochs image</p>
              { props.ic.x ?
                <img 
                  src={
                    process.env.REACT_APP_MEDIA_URL 
                    ? process.env.REACT_APP_MEDIA_URL + props.ic.x.epochs_image_url : 
                    props.ic.x.epochs_image_url} 
                  alt=""/> : <div></div>
              }
            </div>
          </div>
          <div className="flex">
            <div className="w-full p-6">
                <p className="text-center font-bold mb-3">Components plot</p>
                { props.componentsPlotObj ?
                  <ComponentsPlot
                    data={props.componentsPlotObj.data}
                    layout={props.componentsPlotObj.layout}
                  /> : <div></div>
                }
          </div>
        </div>

        </div>

      </div>
      : null 
      }
</div>

  )
}

export default ComponentAnnotation;