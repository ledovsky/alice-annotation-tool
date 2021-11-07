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
          {/* <form className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
            <div className="flex">
              <p className="font-bold">Select IC classes</p>
            </div>
            <CheckboxField name="flag_brain" onChange={props.onChange} checked={props.annotation.flag_brain}>Brain</CheckboxField>
            <CheckboxField name="flag_mu" onChange={props.onChange} checked={props.annotation.flag_mu}>Mu rhythm</CheckboxField>
            <CheckboxField name="flag_alpha" onChange={props.onChange} checked={props.annotation.flag_alpha}>Alpha rhythm</CheckboxField>
            <CheckboxField name="flag_eyes" onChange={props.onChange} checked={props.annotation.flag_eyes}>Eyes</CheckboxField>
            <CheckboxField name="flag_eyes_h" onChange={props.onChange} checked={props.annotation.flag_eyes_h}>Eyes Horizontal</CheckboxField>
            <CheckboxField name="flag_eyes_v" onChange={props.onChange} checked={props.annotation.flag_eyes_v}>Eyes Vertical</CheckboxField>
            <CheckboxField name="flag_muscles" onChange={props.onChange} checked={props.annotation.flag_muscles}>Muscles</CheckboxField>
            <CheckboxField name="flag_heart" onChange={props.onChange} checked={props.annotation.flag_heart}>Heart</CheckboxField>
            <CheckboxField name="flag_ch_noise" onChange={props.onChange} checked={props.annotation.flag_ch_noise}>Channel noise</CheckboxField>
            <CheckboxField name="flag_line_noise" onChange={props.onChange} checked={props.annotation.flag_line_noise}>Line noise</CheckboxField>
            <CheckboxField name="flag_other" onChange={props.onChange} checked={props.annotation.flag_other}>Other</CheckboxField>
            <CheckboxField name="flag_uncertain" onChange={props.onChange} checked={props.annotation.flag_uncertain}>Uncertain</CheckboxField>
            <div className="flex mt-6 w-full">
              <label className="block w-full">
                <span>Comments</span>
                <textarea className="block w-full mt-2" onChange={props.onCommentFieldChange} defaultValue={props.annotation.comment} />
              </label>
            </div>
            <div className="flex mt-6">
              <Button onClick={props.onSubmit}>Save</Button>
            </div>
          </form> */}
        </div>
        <div className="w-full">
          <div className="flex">
            <div className="w-full px-6 max-w-md">
              <p className="text-center font-bold">Topomap of the component</p>
              { props.ic.images ?
                <img src={props.ic.images.img_topomap} alt=""/> : <div></div>
              }
            </div>
            <div className="w-full px-6 max-w-md">
              <p className="text-center font-bold">Spectrum</p>
              { props.ic.images ?
                <img src={props.ic.images.img_spectrum} alt=""/> : <div></div>
              }
            </div>
            <div className="w-full px-6 max-w-md">
              <p className="text-center font-bold">Epochs image</p>
              { props.ic.images ?
                <img src={props.ic.images.img_epochs_image} alt=""/> : <div></div>
              }
            </div>
          </div>
          <div className="flex">
            <div className="w-full p-6">
                <p className="text-center font-bold mb-3">Components plot</p>
                { props.ic.images && props.ic.images.img_sources_plot ?
                  // <Plot 
                  //   data={props.ic.images.img_sources_plot.data}
                  //   layout={props.ic.images.img_sources_plot.layout}
                  //   style={{width: "100%"}}
                  //   useResizeHandler={true}
                  //   config={{displayModeBar: false}}
                  // /> : <div></div>
                  <ComponentsPlot
                    data={props.ic.images.img_sources_plot.data}
                    layout={props.ic.images.img_sources_plot.layout}
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